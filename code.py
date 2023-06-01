import pandas as pd
import streamlit as st
import random
import requests

# GPT API endpoint
API_ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"
# Set your OpenAI API key here
API_KEY = "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"

airbnb = pd.read_csv("https://raw.githubusercontent.com/dev7796/data101_tutorial/main/files/dataset/airbnb.csv")

# Define a function to generate questions based on the template
def generate_questions(num_questions):
    questions = []
    for i in range(num_questions):
        agg = random.choice(['min', 'max', 'mean'])
        attr = random.choice(['price'])
        cat_attrs = random.sample(list(airbnb.select_dtypes(include=['object']).columns), random.randint(1, 3))
        conditions = []
        for cat_attr in cat_attrs:
            value = random.choice(airbnb[cat_attr].unique())
            conditions.append(f"{cat_attr}='{value}'")
        query = " and ".join(conditions)
        question = f"What is the {agg} {attr} when {query}"
        questions.append(question)
    return questions

# Function to make API request to GPT API
def ask_gpt(prompt, question_type):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 200 if question_type == "Concept question" else 50
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Error: Failed to generate answer. Please try again."

# Streamlit app code
st.title("Airbnb Questions Generator")
num_questions = st.number_input("Enter the number of questions to generate", min_value=1, max_value=1000, value=10)
if st.button("Generate"):
    questions = generate_questions(num_questions)
    st.write("Generated questions:")
    st.write(questions)
    # write questions to a CSV file
    df = pd.DataFrame(questions, columns=["Question"])
    df.to_csv("airbnb_questions.csv", index=False)
    st.dataframe(pd.read_csv("airbnb_questions.csv"))

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(index=False, header=False).encode('utf-8'),
        file_name='output.csv',
        mime='text/csv',
    )

st.subheader("Ask GPT")
question_type = st.selectbox("Question Type", ["Coding question", "Concept question"])
prompt = ""
if question_type == "Coding question":
    prompt += "Write R code for "
if question_type == "Concept question":
    prompt += "Limit your answer to 200 words. "

user_question = st.text_area("Type your question here", height=100)
if st.button("Ask"):
    prompt += user_question
    answer = ask_gpt(prompt, question_type)
    st.subheader("Answer:")
    st.write(answer)
