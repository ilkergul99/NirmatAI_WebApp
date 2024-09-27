import streamlit as st
import pandas as pd

# Add custom CSS for background animation and input styling
st.markdown("""
    <style>
    /* Smooth animated wave background in lilac tones */
    body {
        background: linear-gradient(120deg, #d9a7c7, #fffcdc);
        animation: gradient 5s ease infinite;
        height: 100vh;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stTextInput > div > input {
        background-color: #F0F0F5;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .stTextInput > div > input:focus {
        background-color: #e8e8f0;
        box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
    }

    .stFileUploader {
        background-color: #F7F7FA;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .stTable {
        border-radius: 15px;
        background-color: #fff;
        padding: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Style for header text */
    h1 {
        font-family: 'Arial', sans-serif;
        color: #4CAF50;
        text-shadow: 1px 1px 2px #333;
    }

    /* Animation for file upload progress */
    .stProgress {
        animation: growProgressBar 2s ease-out;
    }

    @keyframes growProgressBar {
        from { width: 0%; }
        to { width: 100%; }
    }

    </style>
""", unsafe_allow_html=True)

# Title of the app with a stylish header
st.markdown("<h1 style='text-align: center;'>NirmatAI Submission System</h1>", unsafe_allow_html=True)

# Check if the system is available to accept submissions (mockup)
submission_open = True  # This can be dynamically set based on your backend logic

if submission_open:
    st.success("✅ The system is available to accept submissions.")
else:
    st.error("🚫 The system is not available to accept submissions.")

# User credentials
username = st.text_input("Enter your username", help="This will be used for submission tracking.")
if username:
    st.success(f"Welcome, {username}! 🎉")

# File upload section for documents
st.subheader("📂 Upload your documents (PDFs, DOCXs, Plain Text)")
uploaded_docs = st.file_uploader(
    "Choose files", 
    type=["pdf", "docx", "txt"], 
    accept_multiple_files=True,
    key="docs_upload"
)

# Show upload progress if files are being uploaded
if uploaded_docs:
    total_files = len(uploaded_docs)
    st.write(f"🗂 {total_files} file(s) selected.")
    
    # Initialize progress bar
    progress_bar = st.progress(0)
    
    for i, doc in enumerate(uploaded_docs):
        # Simulate file upload by showing the file name
        st.write(f"⬆ Uploading {doc.name}...")

        # Update progress bar
        progress = int(((i + 1) / total_files) * 100)
        progress_bar.progress(progress)

        # Simulate file processing
        st.write(f"📦 {i + 1}/{total_files} files uploaded.")

    # Once all files are uploaded, display a success message
    st.success(f"✅ All {total_files} file(s) have been uploaded successfully.")

# File upload section for requirements
st.subheader("📑 Upload your requirements (Excel files only)")
st.write("The uploaded Excel file **must** contain the following columns:")
st.markdown("""
- **Requirement Title**
- **Requirement**
- **Requirement ID**
- **Potential Means of Compliance**
- **Label**
""")
st.warning("❗ If these columns are not available, the file upload will be rejected.")

uploaded_requirements = st.file_uploader(
    "Choose an Excel file", 
    type=["xlsx"],
    help="Only Excel files (.xlsx) are accepted.",
    key="req_upload"
)

# Provide a mockup example to the user for requirements
st.subheader("📝 Mockup Example for Requirements")
mockup_data = {
    "Requirement Title": ["Legal responsibility", "Certification Agreement", "Management of Impartiality"],
    "Requirement": ["Req 1", "Req 2", "Req 3"],
    "Requirement ID": ["5.1.1", "5.1.2", "5.1.3"],
    "Potential Means of Compliance": ["MoC 1", "MoC 2", "MoC 3"],
    "Label": ["full-compliance", "major non-conformity", "minor non-conformity"]
}
mockup_df = pd.DataFrame(mockup_data)
st.table(mockup_df)

# If the user uploads the requirements, show them in a table after checking format
if uploaded_requirements is not None:
    try:
        # Ensure it's an Excel file and load the data
        requirements_df = pd.read_excel(uploaded_requirements)

        # Force correct format for the requirements
        required_columns = ["Requirement Title", "Requirement", "Requirement ID", "Potential Means of Compliance", "Label"]

        # Check if all required columns are in the uploaded file
        if all(col in requirements_df.columns for col in required_columns):
            st.subheader("🔍 Uploaded Requirements")
            st.table(requirements_df)
            st.success("✅ Requirements format is correct.")
        else:
            missing_columns = [col for col in required_columns if col not in requirements_df.columns]
            st.error(f"❌ Incorrect format! The following columns are missing: {', '.join(missing_columns)}")

    except Exception as e:
        st.error(f"⚠️ Error processing the file: {e}")

