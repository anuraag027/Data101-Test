import pandas as pd
import streamlit as st
import random

airbnb = pd.read_csv("https://raw.githubusercontent.com/dev7796/data101_tutorial/main/files/dataset/airbnb.csv")

#Define a function to generate questions based on the template:

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
  data=df.to_csv(index=False).encode('utf-8'),#pd.read_csv("airbnb_questions.csv"),#df.to_csv("airbnb_questions.csv", index=False).encode('utf-8'),
  file_name='output.csv',
  mime='text/csv',
)
