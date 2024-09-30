import os
import pandas as pd
import re
import streamlit as st
from time import gmtime, strftime

import mlflow
#from nirmatai_sdk.core import NirmatAI

# Set page configuration
st.set_page_config(
    page_title="NirmatAI Submission System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create directory for uploaded files
if not os.path.exists("uploaded_files"):
    os.makedirs("uploaded_files")

# Add custom CSS for animated background and styling
def local_css(css_text):
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)

custom_css = """
/* Smooth animated wave background in lilac tones for main container */
body {
    background: linear-gradient(120deg, #fff2cc, #fffcdc);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

input[type="text"], input[type="password"] {
    background-color: #F0F0F5;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    margin-bottom: 10px;
    width: 100%;
    box-sizing: border-box;
}

input[type="text"]:focus, input[type="password"]:focus {
    outline: none;
    background-color: #e8e8f0;
}

div.stFileUploader {
    background-color: #F7F7FA;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

div.stDataFrame {
    border-radius: 15px;
    background-color: #fff;
    padding: 10px;
    margin-bottom: 20px;
}

h1, h2, h3 {
    font-family: 'Arial', sans-serif;
    color: #235371;
    text-shadow: 1px 1px 2px #333;
    margin-bottom: 20px;
}

.download-link {
    color: #4CAF50;
    font-size: 14px;
}

button {
    background-color: #1e4863 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
}

button:hover {
    background-color: #45a049 !important;
}
"""

local_css(custom_css)

# Title of the app
st.title("NirmatAI Submission System")

# Submission status
submission_open = True  # This can be dynamically set based on your backend logic

if submission_open:
    st.success("✅ The system is available to accept submissions.")
else:
    st.error("🚫 The system is not available to accept submissions.")

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''

# User authentication (placeholder for real authentication)
def login():
    st.session_state['logged_in'] = True
    st.session_state['username'] = st.session_state['input_username']
    st.rerun()  # Rerun to update the UI

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    # Clear file uploader states
    st.session_state['docs_upload'] = None
    st.session_state['req_upload'] = None
    st.session_state['uploaded_docs'] = []
    st.session_state['requirements_df'] = None
    st.session_state['requirements_file_name'] = None
    st.rerun()  # Rerun to update the UI

# Sidebar content
st.sidebar.header("User Authentication")

if not st.session_state['logged_in']:
    st.sidebar.text_input("Enter your username", key='input_username', help="This will be used for submission tracking.")
    if st.sidebar.button("Login"):
        username = st.session_state.get('input_username', '')
        if username:
            # Check if username is at least 8 characters using regex
            if re.fullmatch(r'.{8,}', username):
                # Placeholder authentication logic
                login()
            else:
                st.sidebar.error("Username must be at least 8 characters long.")
                st.stop()
        else:
            st.sidebar.error("Please enter your username")
            st.stop()
    else:
        st.warning("You need to log in to submit documents.")
        st.stop()
else:
    st.sidebar.success(f"Logged in as {st.session_state['username']}")
    # Explanation about the system
    st.sidebar.markdown("""
    ### About the System
    - This platform allows you to submit documents and requirements for review.
    - For more information, visit the [CERTX website](https://www.certx.com).
    """)
    if st.sidebar.button("Logout"):
        logout()

# Main app tabs
tab1, tab2, tab3 = st.tabs(["📂 Document Upload", "📑 Requirement Upload", "📋 Review & Process"])

with tab1:
    st.header("Upload Your Documents")
    st.write("You can upload multiple files at once (PDF, DOCX, TXT).")

    uploaded_docs = st.file_uploader(
        "Choose files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="docs_upload"
    )

    # Initialize session state for uploaded documents
    if 'uploaded_docs' not in st.session_state:
        st.session_state['uploaded_docs'] = []
    else:
        # If no files are uploaded or all files are removed
        if not uploaded_docs:
            st.session_state['uploaded_docs'] = []

    def save_uploaded_file(uploadedfile):
        user_folder = os.path.join("uploaded_files", st.session_state['username'], 'documents')
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        with open(os.path.join(user_folder, uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer())

    if uploaded_docs:
        # Process and save uploaded files
        for uploaded_file in uploaded_docs:
            save_uploaded_file(uploaded_file)
            # Store file info in session state
            if uploaded_file not in st.session_state['uploaded_docs']:
                st.session_state['uploaded_docs'].append(uploaded_file)
        st.success(f"✅ All {len(uploaded_docs)} file(s) have been uploaded successfully.")

    # Display list of uploaded files
    if st.session_state['uploaded_docs']:
        st.subheader("Uploaded Files")
        file_types = {"pdf": "📄 PDF Files", "docx": "📃 DOCX Files", "txt": "📝 TXT Files"}
        files_by_type = {}
        for file_type in file_types.keys():
            files_by_type[file_type] = [f for f in st.session_state['uploaded_docs'] if f.name.endswith(file_type)]

        for file_type, files in files_by_type.items():
            st.markdown(f"### {file_types[file_type]}")
            if files:
                for file in files:
                    st.write(f"- {file.name}")
            else:
                st.write("No files uploaded.")
    else:
        st.info("No documents uploaded yet.")

    # Submit Data button for Tab 1
    if st.button("Submit Documents"):
        if st.session_state['uploaded_docs']:
            # Placeholder for submission logic
            st.success("🎉 Your documents have been submitted successfully!")
        else:
            st.error("❌ You did not upload any documents.")

with tab2:
    st.header("Upload Your Requirements (Excel files only)")
    st.write("The uploaded Excel file **must** contain the following columns:")
    required_columns = [
        "Requirement Title",
        "Requirement",
        "Requirement ID",
        "Potential Means of Compliance",
        "Label"
    ]
    st.markdown("\n".join([f"- **{col}**" for col in required_columns]))

    # Provide a mockup example to the user for requirements
    st.header("Mockup Example for Requirements")
    mockup_data = {
        "Requirement Title": ["Legal responsibility", "Certification Agreement", "Management of Impartiality"],
        "Requirement": ["Req 1", "Req 2", "Req 3"],
        "Requirement ID": ["5.1.1", "5.1.2", "5.1.3"],
        "Potential Means of Compliance": ["MoC 1", "MoC 2", "MoC 3"],
        "Label": ["full-compliance", "major non-conformity", "minor non-conformity"]
    }
    mockup_df = pd.DataFrame(mockup_data)
    st.dataframe(mockup_df.style.set_properties(**{'text-align': 'left'}))

    st.warning("❗ If these columns are not available, the file upload will be rejected.")

    uploaded_requirements = st.file_uploader(
        "Choose an Excel file",
        type=["xlsx"],
        help="Only Excel files (.xlsx) are accepted.",
        key="req_upload"
    )

    # Initialize session state for requirements
    if 'requirements_df' not in st.session_state:
        st.session_state['requirements_df'] = None
        st.session_state['requirements_file_name'] = None
    else:
        # If no file is uploaded or the file is removed
        if not uploaded_requirements:
            st.session_state['requirements_df'] = None
            st.session_state['requirements_file_name'] = None

    requirements_valid = False  # Flag to check if requirements are valid

    if uploaded_requirements is not None:
        try:
            # Load the data
            requirements_df = pd.read_excel(uploaded_requirements)

            # Check if all required columns are in the uploaded file
            if all(col in requirements_df.columns for col in required_columns):
                #st.subheader("🔍 Uploaded Requirements")
                #st.dataframe(requirements_df)
                st.success("✅ Requirements format is correct.")
                requirements_valid = True  # Set flag to True
                # Save the uploaded file
                def save_requirements_file(uploadedfile):
                    user_folder = os.path.join("uploaded_files", st.session_state['username'], 'requirements')
                    if not os.path.exists(user_folder):
                        os.makedirs(user_folder)
                    with open(os.path.join(user_folder, uploadedfile.name), "wb") as f:
                        f.write(uploadedfile.getbuffer())

                save_requirements_file(uploaded_requirements)
                # Store requirements in session state
                st.session_state['requirements_df'] = requirements_df
                st.session_state['requirements_file_name'] = uploaded_requirements.name
            else:
                missing_columns = [col for col in required_columns if col not in requirements_df.columns]
                st.error(f"❌ Incorrect format! The following columns are missing: {', '.join(missing_columns)}")
                requirements_valid = False  # Set flag to False

        except Exception as e:
            st.error(f"⚠️ Error processing the file: {e}")
            requirements_valid = False  # Set flag to False

    # Display uploaded requirements if available
    if st.session_state['requirements_df'] is not None:
        st.subheader("Uploaded Requirements")
        st.write(f"**File Name:** {st.session_state['requirements_file_name']}")
        st.dataframe(st.session_state['requirements_df'])
    else:
        st.info("No requirements uploaded yet.")

    # Submit Data button for Tab 2
    if st.button("Submit Requirements"):
        if st.session_state['requirements_df'] is not None and requirements_valid:
            # Placeholder for submission logic
            st.success("🎉 Your requirements have been submitted successfully!")
        else:
            st.error("❌ You did not upload any valid requirements.")

with tab3:
    st.header("Review & Process Submissions")

    if not st.session_state['uploaded_docs'] or st.session_state['requirements_df'] is None:
        st.info("No submissions to display. Please upload documents and requirements first.")
    else:
        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded Documents")
            if st.session_state['uploaded_docs']:
                for doc in st.session_state['uploaded_docs']:
                    st.write(f"- {doc.name}")
            else:
                st.write("No documents uploaded.")

        with col2:
            st.subheader("Uploaded Requirements")
            if st.session_state['requirements_df'] is not None:
                st.write(f"**File Name:** {st.session_state['requirements_file_name']}")
                st.dataframe(st.session_state['requirements_df'].iloc[:, :5])
            else:
                st.write("No requirements uploaded.")

        # Process Requirements Button
        if st.button("Process Requirements"):
            """
            mlflow.set_experiment(f"NirmatAI Testing - {st.session_state['username']}")
            start_time = strftime("%c")
            with mlflow.start_run(run_name= f"{st.session_state['username']}-{start_time}"):
                demo = NirmatAI(base_url= "http://localhost:8000/", verbose=1)
                user_folder = os.path.join("uploaded_files", st.session_state['username'], 'documents')
                demo.ingest(directory= user_folder)
                requirement_file = os.path.join("uploaded_files", 
                    st.session_state['username'], 
                    'requirements',
                    st.session_state['requirements_file_name']
                )
                demo.load_requirements(reqs_file=requirement_file)
                nirmatAI_result = demo.process_requirements()

                demo.save_results(nirmatAI_result, f"data/results/{st.session_state['username']}-results.html", attach_reqs= True)

                demo.delete_all_documents()
                st.success("NirmatAI test has been concluded")
            """
            # Placeholder for processing logic
            requirement_file = os.path.join("uploaded_files", 
                    st.session_state['username'], 
                    'requirements',
                    st.session_state['requirements_file_name']
                )
            st.write(f"Requirement File Path: {requirement_file}")
            start_time = strftime("%c")
            st.write(f"{st.session_state['username']}, {start_time}")
            st.success("Documents and Process Requirements have been sent to NirmatAI")

