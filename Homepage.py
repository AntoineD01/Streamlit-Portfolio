import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random


st.title("🏠 Home")
st.write("Welcome to My Portfolio!")
st.write("Hello! I'm Antoine Dupont, a data scientist with a passion for AI, machine learning, and data visualization. "
         "I have experience in developing data-driven solutions and enjoy working on projects that turn data into insights.")


st.write("#### The button feature")

if 'activity' not in st.session_state:
    st.session_state.activity = None

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

questions = [
    {
        "question": "What is the capital of Japan?",
        "options": ["Tokyo", "Seoul", "Beijing"],
        "answer": "Tokyo"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter"],
        "answer": "Mars"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean"],
        "answer": "Pacific Ocean"
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Gold", "Silver"],
        "answer": "Oxygen"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "Mark Twain", "William Shakespeare"],
        "answer": "William Shakespeare"
    },
]

random_activities = ['Drawing', 'Quizz', 'Fun Fact']

def click_button():
    st.session_state.activity = random.choice(random_activities)

def click_submit(selected_answer):
    if selected_answer == questions[st.session_state.question_index]["answer"]:
        st.session_state.score += 1
        st.success("Correct!")
    else:
        st.error(f"Wrong! The correct answer is: {questions[st.session_state.question_index]['answer']}")
    st.session_state.question_index += 1
    
def click_new_quiz():
    st.session_state.question_index = 0
    st.session_state.score = 0


st.button("Next funny activity !", on_click=click_button)

st.write("---")

if st.session_state.activity:
    if st.session_state.activity == 'Drawing':
        st.write("## Let's draw something!")
        # Drawing tool

        drawing_mode = st.selectbox(
            "Drawing tool:",
            ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
        )
        stroke_width = st.slider("Stroke width: ", 1, 25, 3)
        if drawing_mode == "point":
            point_display_radius = st.slider("Point display radius: ", 1, 25, 3)
        stroke_color = st.color_picker("Stroke color hex: ")
        bg_color = st.color_picker("Background color hex: ", "#eee")

        # Create a canvas component
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            height=150,
            drawing_mode=drawing_mode,
            point_display_radius=point_display_radius if drawing_mode == "point" else 0,
            display_toolbar=st.sidebar.checkbox("Display toolbar", True),
            key="full_app",
        )
    elif st.session_state.activity == 'Quizz':
        st.header("Test Your Knowledge!")
        
        if st.session_state.question_index < len(questions):
            current_question = questions[st.session_state.question_index]
            selected_answer = st.radio(current_question["question"], current_question["options"])
            st.button("Next question", on_click=click_submit, args=(selected_answer,))
        else:
            st.write(f"Quiz finished! Your score: {st.session_state.score}/{len(questions)}")
            st.button("Restart Quiz", on_click = click_new_quiz)
        
        

    elif st.session_state.activity == 'Fun Fact':
        st.write("Learn Something Fun")
        fun_facts = [
                "I’m a huge fan of chess and often play online.",
                "I love hiking and exploring nature trails.",
                "I’ve worked on over 10 different data science projects."
            ]    
        st.write(random.choice(fun_facts))
else:
    st.write("Click the button to see a fun activity!")