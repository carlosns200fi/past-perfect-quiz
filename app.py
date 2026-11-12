import random
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Past Perfect Quiz", page_icon="📝")

QUESTIONS = [
    {"q": "By the time we arrived, the movie ____ already started.",
     "options": ["has", "had", "have", "was"], "answer": "had"},
    {"q": "She ____ her homework before she went out.",
     "options": ["had finished", "has finished", "finished", "was finishing"], "answer": "had finished"},
    {"q": "They ____ never seen snow before they visited Canada.",
     "options": ["have", "has", "had", "were"], "answer": "had"},
    {"q": "I was tired because I ____ all night.",
     "options": ["worked", "had worked", "have worked", "was work"], "answer": "had worked"},
    {"q": "When the teacher came in, the students ____ already left.",
     "options": ["had", "have", "has", "were"], "answer": "had"},
    {"q": "He ____ the keys, so he couldn't open the door.",
     "options": ["lost", "has lost", "had lost", "was losing"], "answer": "had lost"},
    {"q": "____ you eaten before you went to the party?",
     "options": ["Have", "Did", "Had", "Were"], "answer": "Had"},
    {"q": "We ____ to the station, but the train had already left.",
     "options": ["had got", "got", "have got", "were get"], "answer": "got"},
    {"q": "After she ____ the book, she returned it to the library.",
     "options": ["had read", "has read", "reads", "was reading"], "answer": "had read"},
    {"q": "My brother ____ not studied, so he failed the exam.",
     "options": ["has", "have", "had", "did"], "answer": "had"},
]

st.title("📝 Past Perfect Quiz")
st.write("Complete each sentence with the correct option.")

col1, col2 = st.columns(2)
group = col1.selectbox("Group", [f"Group {i}" for i in range(1, 8)])
name = col2.text_input("Your name")

# Each group sees the questions in a different (but fixed) order
order = list(range(len(QUESTIONS)))
random.Random(group).shuffle(order)

answers = {}
with st.form("quiz"):
    for n, idx in enumerate(order, start=1):
        item = QUESTIONS[idx]
        answers[idx] = st.radio(
            f"{n}. {item['q']}", item["options"], index=None, key=f"{group}-{idx}"
        )
    submitted = st.form_submit_button("Submit")

if submitted:
    if not name.strip():
        st.warning("Please write your name.")
    elif any(a is None for a in answers.values()):
        st.warning("Please answer all the questions.")
    else:
        score = sum(answers[i] == QUESTIONS[i]["answer"] for i in order)
        total = len(QUESTIONS)
        st.success(f"{name}, your score: {score}/{total}")
        if score == total:
            st.balloons()

        rows = []
        for n, i in enumerate(order, start=1):
            ok = answers[i] == QUESTIONS[i]["answer"]
            rows.append({
                "Group": group, "Student": name, "Question": n,
                "Sentence": QUESTIONS[i]["q"], "Your answer": answers[i],
                "Correct answer": QUESTIONS[i]["answer"],
                "Result": "✅" if ok else "❌",
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            if not ok:
                st.error(f"{n}. Correct answer: **{QUESTIONS[i]['answer']}**")

        df = pd.DataFrame(rows)
        st.download_button(
            "Download results (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            file_name=f"{group}_{name}_results.csv".replace(" ", "_"),
            mime="text/csv",
        )
