import streamlit as st
import requests
import os
import sys

# ---------------------------------------------------------
# Project path
# ---------------------------------------------------------
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

from components.config import API_BASE_URL


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Skills Gap Analysis",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Skills Gap Analysis")

st.write(
    "Compare your resume skills with the requirements of a target role "
    "and identify missing skills."
)


# ---------------------------------------------------------
# Resume Text
# ---------------------------------------------------------
resume_text = st.text_area(
    "Paste your resume text",
    value=st.session_state.get("resume_text", ""),
    height=250,
    placeholder=(
        "Paste your complete resume text here..."
    )
)


# ---------------------------------------------------------
# Target Role
# ---------------------------------------------------------
target_role = st.text_input(
    "Target Role",
    value="AI/ML Engineer",
    placeholder="Example: AI/ML Engineer"
)


# ---------------------------------------------------------
# Analyze Button
# ---------------------------------------------------------
if st.button(
    "Analyze Skill Gap",
    type="primary"
):

    # Validate resume
    if not resume_text.strip():

        st.warning(
            "⚠️ Please provide your resume text."
        )

        st.stop()


    # Validate minimum length
    if len(resume_text.strip()) < 30:

        st.warning(
            "⚠️ Resume text must contain at least 30 characters."
        )

        st.stop()


    # -----------------------------------------------------
    # Send request to FastAPI
    # -----------------------------------------------------
    try:

        resp = requests.post(
            f"{API_BASE_URL}/recommendations/skill-gap",
            json={
                "resume_text": resume_text,
                "target_role": target_role
            },
            timeout=30
        )


        # -------------------------------------------------
        # Handle validation error
        # -------------------------------------------------
        if resp.status_code == 422:

            st.error(
                "❌ FastAPI validation error."
            )

            st.json(resp.json())

            st.stop()


        # -------------------------------------------------
        # Handle other HTTP errors
        # -------------------------------------------------
        resp.raise_for_status()


        # -------------------------------------------------
        # Read response
        # -------------------------------------------------
        result = resp.json()


        st.success(
            "✅ Skill gap analysis completed successfully."
        )


        # -------------------------------------------------
        # Display complete response
        # -------------------------------------------------
        st.subheader("📊 Skill Gap Result")

        st.json(result)


        # -------------------------------------------------
        # Try to display common fields
        # -------------------------------------------------

        if "missing_skills" in result:

            st.subheader("❌ Missing Skills")

            missing_skills = result["missing_skills"]

            if missing_skills:

                for skill in missing_skills:

                    st.markdown(
                        f"- {skill}"
                    )

            else:

                st.success(
                    "🎉 No major missing skills detected."
                )


        if "matched_skills" in result:

            st.subheader("✅ Matched Skills")

            matched_skills = result["matched_skills"]

            if matched_skills:

                for skill in matched_skills:

                    st.markdown(
                        f"- {skill}"
                    )


        if "recommendations" in result:

            st.subheader("💡 Recommendations")

            recommendations = result["recommendations"]

            if isinstance(
                recommendations,
                list
            ):

                for recommendation in recommendations:

                    st.markdown(
                        f"- {recommendation}"
                    )

            else:

                st.write(
                    recommendations
                )


    # -----------------------------------------------------
    # Connection error
    # -----------------------------------------------------
    except requests.exceptions.ConnectionError:

        st.error(
            f"❌ Cannot connect to FastAPI backend at "
            f"{API_BASE_URL}."
        )

        st.info(
            "Make sure the FastAPI server is running on port 8000."
        )


    # -----------------------------------------------------
    # Timeout
    # -----------------------------------------------------
    except requests.exceptions.Timeout:

        st.error(
            "⏱️ Backend request timed out. "
            "Please try again."
        )


    # -----------------------------------------------------
    # HTTP error
    # -----------------------------------------------------
    except requests.exceptions.HTTPError as e:

        st.error(
            f"❌ FastAPI returned an HTTP error: {e}"
        )

        try:

            st.json(resp.json())

        except Exception:

            st.text(resp.text)


    # -----------------------------------------------------
    # Other errors
    # -----------------------------------------------------
    except requests.exceptions.RequestException as e:

        st.error(
            f"❌ API request failed: {e}"
        )


    except Exception as e:

        st.error(
            f"❌ Unexpected error: {e}"
        )