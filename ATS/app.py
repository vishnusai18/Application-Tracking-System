import streamlit as st
import PyPDF2 as pdf
from io import StringIO
import pdfplumber
import time
import google.generativeai as genai
from openai import AzureOpenAI
import streamlit.components.v1 as components

genai.configure(api_key="YOUR-GEMINI-API-KEY")
gmodel = genai.GenerativeModel("gemini-2.0-flash")

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
}


# gemini-1.5-flash

st.set_page_config(page_title="AI1R-ALL IN ONE RESUME",page_icon=":page_with_curl:",layout="wide",menu_items={
   "report a bug":"mailto:vishnupuma18@gmail.com", 
})
st.title("Application Tracking System")

st.write("AI based model to check your ATS score.")

st.info("Your All in One Resume Tool based on LLM's")


# adsense_code = """

# <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3268803798026176"
#      crossorigin="anonymous"></script>

# """
# components.html(adsense_code)


if "model" not in st.session_state:
    st.session_state.model = "GEMINI"

with st.sidebar:
    st.success("We are currently using open source models, but you can paste your open ai api key if you want to use GPT Models")

    openai = st.toggle(label="Open AI/ Azure Open AI",)


    if openai:
        api_key = st.text_input(label="Open AI API Key",type="password")
        deployment_name = st.text_input(label="Model Name/ Deployment")
        api_endpoint = st.text_input(label="api base or endpoint")
        api_version = st.text_input(label="enter your model version")

        if st.button("Update Model"):
            if api_key:
                if deployment_name:
                    if api_endpoint:
                        if api_version:
                            st.success("Updated model configuration to selected open ai")
                            st.session_state.model = "AZUREOPENAI"
                        else:
                            st.error("Mention model version")

                    else:
                        st.error("mention api endpoint")
                else:
                    st.error("mention model deployment name")
            else:
                st.error("Mention api key")

    if st.button(label="Update my Resume"):
        st.write("This feature will release in the next update.....")

    st.info("I appreciate your feedback of the website or AI response",icon=":material/reviews:",)
    sentiment_mapping = ["Bad", "Not Satisfied", "No Opinion", "Satisfied", "Good"]
    selected = st.feedback("faces",)
    if selected is not None:
        st.markdown(f"You selected **{sentiment_mapping[selected]}**.")
        st.write("Thanks for your feedback.....")
        if (sentiment_mapping[selected]=="Bad") or (sentiment_mapping[selected]=="Not Satisfied"):
            feedbacks = st.text_input("can you let us know what made u felt bad")
            if feedbacks:
                st.warning("Will check you response and improve the system accordingly")
        if (sentiment_mapping[selected]=="Satisfied") or (sentiment_mapping[selected]=="Good"):
            st.success("Pleasure, helping you out.....")

jd_type = st.selectbox(label="job-description",options=['job description text','image'])


def extract_data(feed):
    data = ""
    with pdfplumber.open(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            data+=(p.extract_text_simple())
    return data

print("after resume upload",st.session_state.model)
def azureopenaiinstance(input_prompt):

    client = AzureOpenAI(  
        azure_endpoint=api_endpoint,  
        api_version=api_version, 
        api_key=api_key
        )

    response = client.chat.completions.create(
    model=deployment_name, # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a skilled in giving recommendations"},
        {"role": "user", "content": input_prompt},
    ]
    )
    return (response.choices[0].message.content)

def llm_answer(df,jd,model):

    input_prompt = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
    your task is to evaluate the resume against the provided job description.give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
    resume : {df}
    job description:{jd}

    """.format(df=df,jd=jd)

    if model=="GEMINI":
        response = gmodel.generate_content(input_prompt)
        print(response.text)
        return (response.text)
    
    if model=="AZUREOPENAI":
        t = azureopenaiinstance(input_prompt)
        return t


def summarize(df,model):

    input_prompt = """
    You are a skilled resume summarizer, where you read the resume and summarize it in a simple and direct concise summary of the key skills and experiences.
    resume : {df}
    """.format(df=df)

    if model=="GEMINI":
        response = gmodel.generate_content(input_prompt)
        print(response.text)
        return (response.text)
    
    if model=="AZUREOPENAI":

        t = azureopenaiinstance(input_prompt)
        return t

def recommend(df,model):

    input_prompt = """
    You are a skilled in giving recommendations, where you read the resume,summarize and understand it. Now give job or position recommendations to the user based on your understandings and its % matching with particular job position.
    In the output response give only job positions and % match and justify each with one simple line.
    resume : {df}
    """.format(df=df)

    if model=="GEMINI":
        response = gmodel.generate_content(input_prompt)
        print(response.text)

        return (response.text)
    
    if model=="AZUREOPENAI":

        t = azureopenaiinstance(input_prompt)
        return t

if jd_type=='image':
    st.write("This feature will be available in next update.....")
    jd = ""
if jd_type=='job description text':
    jd = st.text_input(label='You can paste the job description from Linkedin or other job portals,')
    st.info("Please press enter after you paste JD.")
    if jd:
        st.success('Saved your jd to the session.')

resume = st.file_uploader(label='Your Resume in PDF format',type='pdf')
if resume is not None:

    df = extract_data(resume)

st.write("ATS Summary.....")

c1,c2,c3 = st.columns(3)

with c1:
    try:
        if st.button(label="Find ATS Summary"):
            with st.status("Running Your ATS Score..."):
                st.write("Scanning your resume...")
                time.sleep(2)
                st.write("Evaluating with job description by llm")
                gem_out = (llm_answer(df,jd,st.session_state.model))
                st.write("calculation and text generation...")
            st.write(gem_out)
    except Exception:
        st.warning("Please check all your inputs.")
with c2:
    try:    
        if st.button(label="Summarize Resume"):
            with st.status("Resume summarization"):
                st.write("Scanning your resume...")
                time.sleep(2)
                st.write("Summarizing by llm")
                gem_sum_out = (summarize(df,st.session_state.model))
                st.write("text generation...")
                time.sleep(1)
            st.write(gem_sum_out)
    except Exception:
        st.warning("Please check all your inputs.")
with c3:
    try:
        if st.button(label="Recommend Job Positions"):
            with st.status("Activating Recommendation System"):
                st.write("Scanning your resume...")
                time.sleep(2)
                st.write("Identifying the Job Positions")
                gem_rec_out = (recommend(df,st.session_state.model))
                st.write("text generation...")
                time.sleep(1)
            print("after llm",st.session_state.model)
            st.write(gem_rec_out)
    except Exception:
        st.warning("Please check all your inputs.")
