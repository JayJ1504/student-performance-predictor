import streamlit as st
import pandas as pd
import joblib
import os

# Load trained model
model_path = os.path.abspath('model/student_pass_predictor.pkl')

# Debugging output
print("🔍 Current Working Directory:", os.getcwd())
print("📁 Model Absolute Path:", model_path)
print("✅ File Exists?:", os.path.exists(model_path))

# Attempt to load model
model = joblib.load(model_path)



# Title
st.title("🎓 Student Performance Predictor")

# Sidebar Input
st.sidebar.header("Enter Student Details")

gender = st.sidebar.selectbox("Gender", ["male", "female"])
ethnicity = st.sidebar.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
parent_edu = st.sidebar.selectbox("Parental Level of Education", [
    "some high school", "high school", "some college", 
    "associate's degree", "bachelor's degree", "master's degree"
])
lunch = st.sidebar.selectbox("Lunch Type", ["standard", "free/reduced"])
test_prep = st.sidebar.selectbox("Test Preparation Course", ["none", "completed"])

math_score = st.sidebar.slider("Math Score", 0, 100, 50)
reading_score = st.sidebar.slider("Reading Score", 0, 100, 50)
writing_score = st.sidebar.slider("Writing Score", 0, 100, 50)

# Create average score
avg_score = (math_score + reading_score + writing_score) / 3

# Encode categorical values manually
def encode_features():
    gender_val = 1 if gender == "male" else 0
    ethnicity_val = {"group A": 0, "group B": 1, "group C": 2, "group D": 3, "group E": 4}[ethnicity]
    parent_val = {
        "some high school": 5, "high school": 3, "some college": 4,
        "associate's degree": 0, "bachelor's degree": 1, "master's degree": 2
    }[parent_edu]
    lunch_val = 0 if lunch == "free/reduced" else 1
    test_val = 1 if test_prep == "completed" else 0

    return pd.DataFrame([{
        'gender': gender_val,
        'race/ethnicity': ethnicity_val,
        'parental level of education': parent_val,
        'lunch': lunch_val,
        'test preparation course': test_val
    }])

# Prediction
if st.button("Predict Performance"):
    input_df = encode_features()
    prediction = model.predict(input_df)[0]
    
    result = "🎉 Pass" if prediction == 1 else "❌ Fail"
    st.subheader(f"Prediction: {result}")
    st.write(f"📊 Average Exam Score: `{avg_score:.2f}`")
