import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle

# Page Configuration
st.set_page_config(page_title="AI-Driven Drug Discovery", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Navigation Bar */
        .nav-container {
            display: flex;
            justify-content: flex-end; /* Align items to the right */
            background-color: #003366;
            padding: 10px 20px;
            border-radius: 10px;
        }
        .nav-container a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
        }
        .nav-container a:hover {
            text-decoration: underline;
        }

        /* Title Section */
        .title-text {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #004080;
        }
        .subtext {
            text-align: center;
            font-size: 18px;
            color: #666;
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #333;
            padding: 10px;
            margin-top: 50px;
            border-top: 1px solid #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation Tabs
selected_page = st.radio("", ["Home", "About", "Contact"], horizontal=True)
st.markdown(
    """
    <style>
        div[role="radiogroup"] {
            display: flex;
            justify-content: flex-end; /* Aligns tabs to the right */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Home Section
if selected_page == "Home":
    st.markdown("<h1 class='title-text'>Welcome to AI Drug Discovery</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtext'>Revolutionizing Drug Discovery with AI</p>", unsafe_allow_html=True)

# About Section (How It Works)
elif selected_page == "About":
    st.image("how_it_works.png", caption="AI-Powered Drug Discovery Benefits", use_container_width=True)
    st.markdown("<h2>How It Works</h2>", unsafe_allow_html=True)
    st.write("Our AI-powered system analyzes molecular structures, predicts bioactivity, and accelerates drug discovery.")

# Contact Section (Footer)
elif selected_page == "Contact":
    st.markdown(
        """
        <div class="footer">
            <p>Developed as part of a research project on AI-driven drug discovery.</p>
            <p>Contact: <a href="mailto:omsantoshsongire23@gmail.com?subject=Inquiry" target="_blank">omsantoshsongire23@gmail.com</a></p>
            <p>© 2025 AI Drug Discovery Project. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Title Section
st.markdown('<h1 class="title-text">AI-Powered Drug Discovery</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Welcome to our AI-driven drug discovery platform!</p>', unsafe_allow_html=True)

# Display Logo if Exists
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)

# How It Works Section
st.markdown(
    """
    <style>
        .how-it-works {
            font-size: 24px; /* Increased font size for title */
            font-weight: bold;
            color: #003366; /* Dark blue color */
            margin-top: 20px;
        }
        .how-it-works-text {
            font-size: 18px;
            color: #444;
            line-height: 1.6; /* Improved readability */
        }
    </style>
    
    <h2 class="how-it-works">🔬 How It Works:</h2>
    <p class="how-it-works-text">
        Our AI-driven platform revolutionizes drug discovery by analyzing molecular structures and predicting bioactivity.
        <br><br>
        <b>1. Upload Your Data:</b> Provide a dataset (.csv or .txt) containing molecular structures.
        <br>
        <b>2. AI Analysis:</b> The AI model processes your data and predicts potential drug candidates based on bioactivity scores.
        <br>
        <b>3. Get Results:</b> Download the processed results and gain actionable insights into drug discovery.
    </p>
    """,
    unsafe_allow_html=True,
)

if os.path.exists("how_it_works.png"):
    st.image("how_it_works.png", caption="AI-Powered Drug Discovery Benefits", use_container_width=True)

st.markdown(
    """
    <style>
        .why-use-this {
            font-size: 22px; /* Increase font size */
            font-weight: bold;
            color: #003366; /* Dark blue color */
            margin-top: 20px;
        }
        .why-use-text {
            font-size: 18px;
            color: #444;
            line-height: 1.6; /* Improve spacing */
        }
    </style>
    
    <hr>
    <h2 class="why-use-this">🚀 Why Use This?</h2>
    <ul class="why-use-text">
        <li><b>Fast & Automated:</b> No need for manual calculations.</li>
        <li><b>Accurate Predictions:</b> Uses ML-trained models for bioactivity analysis.</li>
        <li><b>User-Friendly:</b> Simple file upload, real-time results.</li>
    </ul>
    """,
    unsafe_allow_html=True,
)

# Molecular descriptor calculator (PaDEL-Descriptor)
def desc_calc():
    if not os.path.exists("./PaDEL-Descriptor/PaDEL-Descriptor.jar"):
        st.error("Error: PaDEL-Descriptor software is missing!")
        return
    
    bashCommand = ["java", "-Xms2G", "-Xmx2G", "-Djava.awt.headless=true", "-jar", 
                   "D:/bioactivity-prediction-app-main/PaDEL-Descriptor/PaDEL-Descriptor.jar",
                   "-removesalt", "-standardizenitro", "-fingerprints", 
                   "-descriptortypes", 
                   "D:/bioactivity-prediction-app-main/PaDEL-Descriptor/PubchemFingerprinter.xml",
                   "-dir", "D:/bioactivity-prediction-app-main/", 
                   "-file", "D:/bioactivity-prediction-app-main/descriptors_output.csv"]
    
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    
    if os.path.exists("molecule.smi"):
        os.remove("molecule.smi")

# File download function
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Load ML Model
model_path = "acetylcholinesterase_model.pkl"
if os.path.exists(model_path):
    with open(model_path, "rb") as file:
        model = pickle.load(file)
else:
    st.error("Error: Model file not found! Please upload the trained model.")
    st.stop()

# Sidebar for File Upload (Supports .txt and .csv)
with st.sidebar:
    st.header("🔬 Upload Your Molecular Data")
    uploaded_file = st.file_uploader("Upload CSV or TXT", type=["csv", "txt"])
    st.markdown("**Example Format:**\n- `SMILES Molecule_ID` format\n- Supported file types: `.csv`, `.txt`", unsafe_allow_html=True)

if uploaded_file is not None:
    # Determine file type
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "csv":
        data = pd.read_csv(uploaded_file)
    elif file_extension == "txt":
        data = pd.read_table(uploaded_file, sep=" ", header=None)
        data.columns = ["SMILES", "Molecule_Name"]
    else:
        st.error("Unsupported file format! Please upload a .csv or .txt file.")
        st.stop()

    st.subheader("Uploaded Data")
    st.dataframe(data)
    st.write(f"Uploaded data shape: {data.shape}")

    # Convert input to molecule format for PaDEL
    data.to_csv("molecule.smi", sep='\t', header=False, index=False)

    with st.spinner("Calculating molecular descriptors..."):
        desc_calc()

    # Read in calculated descriptors and display them
    if os.path.exists("descriptors_output.csv"):
        st.subheader("Calculated Molecular Descriptors")
        desc = pd.read_csv("descriptors_output.csv")
        st.dataframe(desc)
    else:
        st.error("Error: Descriptor calculation failed. Check PaDEL setup.")
        st.stop()

    # Read descriptor list used in previously built model
    if os.path.exists("descriptor_list.csv"):
        Xlist = list(pd.read_csv("descriptor_list.csv").columns)
        
        missing_cols = [col for col in Xlist if col not in desc.columns]
        if missing_cols:
            st.error(f"Error: The following required descriptors are missing: {missing_cols}")
            st.stop()

        desc_subset = desc[Xlist]
        desc_subset = desc_subset.dropna()

        st.subheader("Subset of Descriptors from Model")
        st.dataframe(desc_subset)
        st.write(f"Descriptors shape before model prediction: {desc_subset.shape}")
    else:
        st.error("Error: Descriptor list file missing!")
        st.stop()

    # Make predictions
    predictions = model.predict(desc_subset)

    if len(predictions) != len(desc_subset):
        st.error(f"Error: Model returned {len(predictions)} predictions for {len(desc_subset)} descriptors!")
        st.stop()

    data = data.iloc[:len(predictions)]
    data["Predicted Bioactivity (pIC50)"] = predictions

    # Display summary before showing the full table
    st.subheader("Prediction Summary")
    st.write(f"**Total Molecules Processed:** {len(data)}")
    st.write(f"**Average Predicted Bioactivity (pIC50):** {data['Predicted Bioactivity (pIC50)'].mean():.2f}")

    # Display detailed results
    st.subheader("🔬 Detailed Prediction Results")
    st.dataframe(data)



    # Download Predictions
    csv = data.to_csv(index=False)
    st.download_button("Download Predictions", csv, "predictions.csv", "text/csv")
else:
    st.info("Upload a CSV or TXT file to start predictions.")

# Footer Section
# Footer Section
st.markdown(
    """
    <div class="footer">
        <p>Developed as part of a research project on AI-driven drug discovery.</p>
        <p>Contact: 
            <a href="https://mail.google.com/mail/?view=cm&fs=1&to=omsantoshsongire23@gmail.com" target="_blank">
                omsantoshsongire23@gmail.com
            </a>
        </p>
        <p>© 2025 AI Drug Discovery Project. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True,
)