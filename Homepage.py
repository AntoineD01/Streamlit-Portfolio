import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random
import os


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

vote_file = "votes.txt"

if 'vote_counts' not in st.session_state:
    st.session_state.vote_counts = {}

    # Read existing votes from the file
    if os.path.exists(vote_file):
        with open(vote_file, "r") as f:
            for line in f:
                fruit, count = line.strip().split(':')
                st.session_state.vote_counts[fruit] = int(count)
    else:
        # Initialize the vote counts if the file doesn't exist
        fruits = ['Apple', 'Banana', 'Cherry', 'Date', 'Grapes']
        st.session_state.vote_counts = {fruit: 0 for fruit in fruits}

random_activities = ['Drawing', 'Quizz', 'Fun Fact', 'Fun Poll']

def click_button():
    last_activity = st.session_state.activity
    while True:
        new_activity = random.choice(random_activities)
        if new_activity != last_activity:
            st.session_state.activity = new_activity
            break


st.button("Next funny activity !", on_click=click_button)

st.write("---")

if st.session_state.activity:
    if st.session_state.activity == 'Drawing':
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
            key="full_app",
        )
    elif st.session_state.activity == 'Quizz':
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
        
        st.header("Test Your Knowledge!")
        
        if st.session_state.question_index < len(questions):
            current_question = questions[st.session_state.question_index]
            selected_answer = st.radio(current_question["question"], current_question["options"])
            st.button("Next question", on_click=click_submit, args=(selected_answer,))
        else:
            st.write(f"Quiz finished! Your score: {st.session_state.score}/{len(questions)}")
            st.button("Restart Quiz", on_click = click_new_quiz)
    
    elif st.session_state.activity == 'Fun Fact':
        st.write("### Did you know?")
        fun_facts = [
        "Octopuses have three hearts: two pump blood to the gills, while the third pumps it to the rest of the body.",
        "Bananas are berries: botanically speaking, bananas fit the definition of a berry, while strawberries do not.",
        "Honey never spoils: archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "A day on Venus is longer than a year: it takes Venus about 243 Earth days to rotate once on its axis but only about 225 Earth days to orbit the sun.",
        "Wombat poop is cube-shaped: this unique shape prevents their droppings from rolling away and marks their territory.",
        "The Eiffel Tower can be 15 cm taller in the summer: when the temperature rises, the iron expands, causing the tower to grow slightly.",
        "Turtles can breathe through their butts: some species of turtles can absorb oxygen through their cloaca, allowing them to stay underwater longer.",
        "Cows have best friends: research shows that cows are social animals and often have strong bonds with specific companions.",
        "The human nose can detect over 1 trillion scents: while it's commonly said we can only detect about 10,000 smells, recent research suggests the number is much higher.",
        "Dolphins have names for each other: they use unique whistles to identify and call out to one another, similar to how humans use names."
        ]
        st.write(random.choice(fun_facts))
        def click_fun_fact():
            st.write(random.choice(fun_facts))

        st.button("Next fun fact", on_click=click_fun_fact)

    elif st.session_state.activity == 'Fun Poll':
        st.header("Express Your Opinion!")
        
        if 'current_poll' not in st.session_state:
            st.session_state.current_poll = random.choice(['Fruit', 'City', 'Color', 'Animal'])

        def conduct_poll(poll_type):
            # Define options based on poll type
            if poll_type == 'Fruit':
                options = ['Apple', 'Banana', 'Cherry', 'Date', 'Grapes']
            elif poll_type == 'City':
                options = ['New York', 'Los Angeles', 'Chicago', 'Paris', 'Marseille']
            elif poll_type == 'Color':
                options = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']
            elif poll_type == 'Animal':
                options = ['Dog', 'Cat', 'Elephant', 'Tiger', 'Giraffe']
            else:
                return st.error("Invalid poll type!")

            # Initialize vote counts if not already done
            if 'vote_counts' not in st.session_state:
                st.session_state.vote_counts = {option: 0 for option in options}
            else:
                # Ensure all options are included in vote counts
                for option in options:
                    if option not in st.session_state.vote_counts:
                        st.session_state.vote_counts[option] = 0

            selected_option = st.radio(f"Which {poll_type.lower()} do you like the most?", options)

            if st.button("Vote"):
                # Update the vote count
                st.session_state.vote_counts[selected_option] += 1
                st.success(f"You voted for: {selected_option}!")

                # Write updated votes to the file
                with open(vote_file, "w") as f:
                    for option, count in st.session_state.vote_counts.items():
                        f.write(f"{option}:{count}\n")
                    
                # Display results for the specific poll type
                display_result(options)

            # Button to go to the next poll
            if st.button("Next Poll"):
                st.session_state.current_poll = random.choice(['Fruit', 'City', 'Color', 'Animal'])
                # Do not call rerun, simply let the streamlit script handle the new state

        def display_result(options):
            st.write("### Poll Results:")
            for option in options:
                count = st.session_state.vote_counts[option]
                st.write(f"{option}: {count} votes")

        # Conduct the selected poll
        conduct_poll(st.session_state.current_poll)


else:
    st.write("Click the button to see a fun activity!")