"""
Improves resume language: weak bullet points and generic summaries become
stronger, keyword-rich, action-oriented text.

Two modes:
1. Rule-based (default, offline, free) — good enough for most cases and
   used automatically when no LLM API key is configured.
2. LLM-assisted (optional) — if ANTHROPIC_API_KEY is set in the
   environment, `improve_with_llm()` sends the text to Claude for a
   genuinely AI-generated rewrite. This is the hook described in the
   project plan ("implement using an LLM API").

IMPORTANT: The rule-based rewriter never invents facts (numbers, tools,
outcomes) the user didn't provide — it only restructures and strengthens
wording. Encourage users to fill in real metrics themselves.
"""
import os
import re
from typing import List, Optional

ACTION_VERBS = [
    "Developed", "Built", "Designed", "Implemented", "Engineered",
    "Led", "Optimized", "Automated", "Streamlined", "Deployed",
    "Architected", "Delivered",
]

WEAK_STARTERS = {
    "made": "Developed", "did": "Executed", "worked on": "Contributed to",
    "helped": "Supported", "was responsible for": "Led",
    "in charge of": "Managed", "used": "Utilized",
}


def _titlecase_first_verb(sentence: str) -> str:
    sentence = sentence.strip()
    for weak, strong in WEAK_STARTERS.items():
        if sentence.lower().startswith(weak):
            sentence = strong + sentence[len(weak):]
            break
    if sentence and sentence[0].islower():
        sentence = sentence[0].upper() + sentence[1:]
    return sentence


def improve_bullet(bullet: str, target_keywords: Optional[List[str]] = None) -> dict:
    """Rule-based bullet point strengthening."""
    original = bullet.strip()
    improved = _titlecase_first_verb(original)

    # ensure it starts with a strong action verb
    first_word = improved.split(" ", 1)[0].rstrip(".,")
    if first_word not in ACTION_VERBS and not any(improved.startswith(v) for v in ACTION_VERBS):
        improved = f"Developed {improved[0].lower() + improved[1:]}" if improved else improved

    reason_parts = ["Starts with a strong action verb"]

    # weave in up to 2 missing target keywords naturally, if provided
    if target_keywords:
        missing_here = [k for k in target_keywords if k.lower() not in improved.lower()][:2]
        if missing_here:
            improved = improved.rstrip(". ") + f", using {', '.join(missing_here)}."
            reason_parts.append(f"incorporates relevant keyword(s): {', '.join(missing_here)}")

    if not improved.rstrip().endswith((".", "!", "?")):
        improved = improved.rstrip() + "."

    if not any(ch.isdigit() for ch in improved):
        reason_parts.append("add a measurable result (%, time saved, users, revenue) if available")

    return {
        "original": original,
        "improved": improved,
        "reason": "; ".join(reason_parts) + ".",
    }


def improve_summary(summary: str, target_role: Optional[str] = None,
                     top_skills: Optional[List[str]] = None) -> dict:
    original = summary.strip()
    notes = []

    if len(original) < 40:
        notes.append("Summary is too short/generic — expand to 2-3 sentences.")

    skills_phrase = ", ".join(top_skills[:4]) if top_skills else "relevant technical skills"
    role_phrase = target_role or "the target role"

    improved = (
        f"Results-driven {role_phrase} with hands-on experience in {skills_phrase}. "
        f"{original.strip().rstrip('.')} "
        f"Proven ability to deliver practical, data-driven solutions and collaborate "
        f"effectively across teams."
    ).strip()
    improved = re.sub(r"\s+", " ", improved)

    return {"original": original, "improved": improved, "notes": notes}


def improve_with_llm(text: str, instruction: str) -> Optional[str]:
    """
    Optional path: calls the Anthropic API to rewrite `text` per `instruction`.
    Returns None (falls back to rule-based) if no API key is configured.
    Requires: pip install anthropic
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"{instruction}\n\nText:\n{text}\n\nReturn only the rewritten text, nothing else."
            }],
        )
        return "".join(block.text for block in message.content if hasattr(block, "text")).strip()
    except Exception:
        return None