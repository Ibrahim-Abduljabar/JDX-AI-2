import streamlit as st
import os
from logsnag import LogSnag
from groq import Groq  

log_client = LogSnag(token=st.secrets["LOGSNAG_TOKEN"], project="jdx-ai")
log_client.track(channel="visits", event="New Visit")

st.set_page_config(page_title="JDX AI", layout="wide")

st.markdown("<h1 style='text-align: center;'>Job Description Generator — JDX AI</h1>", unsafe_allow_html=True)

def generate_jd(title, tasks, skills):
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return "⚠ Error: API key not found. Make sure to add GROQ_API_KEY inside Streamlit Cloud Secrets settings."

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        Write a professional job description for the job title: {title}
        Core Tasks/Responsibilities:
        {tasks}

        Required Skills:
        {skills}

        Write the description in a well-formatted and clear manner.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-120b",  
            temperature=0.3,
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"⚠ An error occurred while connecting to Groq: {str(e)}"


st.markdown("### Job Description No. 1")

title = st.text_input("Job Title", "", key="title")
tasks = st.text_area("Core Tasks", "", key="tasks")
skills = st.text_area("Required Skills", "", key="skills")

if st.button("Generate Job Description"):
    if title.strip() == "" or tasks.strip() == "" or skills.strip() == "":
        st.error("Please fill in all fields before generating.")
    else:
        with st.spinner("Generating job description..."):
            jd_text = generate_jd(title, tasks, skills)

        st.markdown("### Result:")
        
        st.text_area(
            label="Generated Description", 
            value=jd_text, 
            height=400, 
            key="result_area_1", 
            disabled=True, 
            label_visibility="collapsed"
        )

        st.info("If you want to save the description as a PDF, press Ctrl + P (or Cmd + P on Mac).")


if st.button("➕ Add Another Job Description"):
    st.markdown("### Job Description No. 2")

    new_title = st.text_input("Job Title (New)", "")
    new_tasks = st.text_area("Core Tasks (New)", "")
    new_skills = st.text_area("Required Skills (New)", "")

    if st.button("Generate New Job Description"):
        if new_title.strip() == "" or new_tasks.strip() == "" or new_skills.strip() == "":
            st.error("Please fill in all fields before generating.")
        else:
            with st.spinner("Generating new job description..."):
                jd_text2 = generate_jd(new_title, new_tasks, new_skills)

            st.markdown("### Result:")
            
            st.text_area(
                label="New Generated Description", 
                value=jd_text2, 
                height=400, 
                key="result_area_2", 
                disabled=True, 
                label_visibility="collapsed"
            )
