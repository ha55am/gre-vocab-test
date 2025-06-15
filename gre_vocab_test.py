import streamlit as st
import random
from gre_vocabulary import GRE_VOCABULARY

def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
    if 'questions' not in st.session_state:
        st.session_state.questions = []

def generate_question():
    # Get a random word from the vocabulary
    word = random.choice(list(GRE_VOCABULARY.keys()))
    correct_meaning = GRE_VOCABULARY[word]
    
    # Get three random incorrect meanings
    other_words = list(GRE_VOCABULARY.keys())
    other_words.remove(word)
    incorrect_meanings = [GRE_VOCABULARY[random.choice(other_words)] for _ in range(3)]
    
    # Combine all options and shuffle them
    options = [correct_meaning] + incorrect_meanings
    random.shuffle(options)
    
    return {
        'word': word,
        'options': options,
        'correct_answer': correct_meaning
    }

def main():
    st.title("GRE Vocabulary Test")
    
    initialize_session_state()
    
    if not st.session_state.test_started:
        st.write("Welcome to the GRE Vocabulary Test!")
        num_questions = st.number_input(
            "How many questions would you like to attempt?",
            min_value=1,
            max_value=len(GRE_VOCABULARY),
            value=10
        )
        
        if st.button("Start Test"):
            st.session_state.total_questions = num_questions
            st.session_state.test_started = True
            st.session_state.questions = [generate_question() for _ in range(num_questions)]
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.experimental_rerun()
    
    else:
        if st.session_state.current_question < st.session_state.total_questions:
            current_q = st.session_state.questions[st.session_state.current_question]
            
            st.write(f"Question {st.session_state.current_question + 1} of {st.session_state.total_questions}")
            st.write(f"What is the meaning of the word: **{current_q['word']}**")
            
            selected_option = st.radio(
                "Select the correct meaning:",
                current_q['options'],
                key=f"q_{st.session_state.current_question}"
            )
            
            if st.button("Submit"):
                if selected_option == current_q['correct_answer']:
                    st.session_state.score += 1
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! The correct meaning is: {current_q['correct_answer']}")
                
                st.session_state.current_question += 1
                st.experimental_rerun()
        
        else:
            st.write("Test completed!")
            st.write(f"Your score: {st.session_state.score} out of {st.session_state.total_questions}")
            st.write(f"Percentage: {(st.session_state.score/st.session_state.total_questions)*100:.2f}%")
            
            if st.button("Take another test"):
                st.session_state.test_started = False
                st.experimental_rerun()

if __name__ == "__main__":
    main() 