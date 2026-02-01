import streamlit as st
import requests

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
# This is the URL of your "Engine" on the cloud
API_URL = "https://machine-learning-deployment-74qf.onrender.com/predict"

# Set the page title and icon
st.set_page_config(page_title="Voter Prediction App", page_icon="🗳️")

# ------------------------------------------------------------------
# UI LAYOUT
# ------------------------------------------------------------------
st.title("🗳️ Voter Prediction AI")
st.write("Enter the details below to check if the person is likely to vote.")

# Create two columns for a nicer layout
col1, col2 = st.columns(2)

with col1:
    st.header("📍 Location")
    # Default values set to Bangalore coordinates (from your successful test)
    latitude = st.number_input("Latitude", value=12.9716, format="%.4f")
    longitude = st.number_input("Longitude", value=77.5946, format="%.4f")

with col2:
    st.header("👤 Identity")
    # A dropdown menu is much easier than typing 0s and 1s!
    gender = st.selectbox("Select Gender", ["Male", "Female", "Polygender"])

# ------------------------------------------------------------------
# LOGIC: CONVERT INPUTS TO DATA
# ------------------------------------------------------------------
# The model expects "One-Hot Encoding" (0s and 1s).
# We interpret the dropdown selection here.
gender_female = 0
gender_male = 0
gender_poly = 0

if gender == "Male":
    gender_male = 1
elif gender == "Female":
    gender_female = 1
elif gender == "Polygender":
    gender_poly = 1

# ------------------------------------------------------------------
# SEND DATA TO SERVER
# ------------------------------------------------------------------
if st.button("🚀 Predict Result", type="primary"):
    
    # Create the dictionary EXACTLY how the server wants it (Order matters!)
    # Based on your successful test: Location First, then Gender (Alphabetical)
    input_data = {
        "latitude": latitude,
        "longitude": longitude,
        "gender_Female": gender_female,
        "gender_Male": gender_male,
        "gender_Polygender": gender_poly
    }

    # Show a spinner while waiting for the cloud
    with st.spinner("Connecting to the AI Model..."):
        try:
            # Send the POST request
            response = requests.post(API_URL, json=input_data)

            if response.status_code == 200:
                # Get the answer
                prediction = response.json()['prediction']
                
                st.success("Analysis Complete!")
                
                # Display the result big and bold
                if prediction == 1:
                    st.metric(label="Prediction", value="Positive (1)", delta="Likely to Vote")
                else:
                    st.metric(label="Prediction", value="Negative (0)", delta="Unlikely to Vote", delta_color="inverse")
            else:
                st.error("Server Error!")
                st.code(response.text)

        except Exception as e:
            st.error(f"Connection Failed! Is your internet working? \nError: {e}")