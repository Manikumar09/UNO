import streamlit as st
import random

# Initialize game state
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
    st.session_state.cpu_score = 0
    st.session_state.cards = ['Red 1', 'Blue 2', 'Green 3', 'Yellow 4', 'Wild +4']
    st.session_state.player_card = None
    st.session_state.cpu_card = None

# Function to simulate card drawing
def draw_card():
    return random.choice(st.session_state.cards)

# Function to simulate a CPU turn (simple random selection)
def cpu_turn():
    return random.choice(st.session_state.cards)

# Title of the game
st.title("UNO Game - Streamlit Version")

# Display instructions
st.write("""
    Welcome to the UNO game simulation! Here you can draw cards and play against a simple AI opponent.
    - **Draw Card**: Draw a random card from the deck.
    - **Play Card**: Play the card you drew.
    - The game keeps track of your score and the CPU's score.
""")

# Display the current scores
st.subheader(f"Your Score: {st.session_state.player_score}")
st.subheader(f"CPU Score: {st.session_state.cpu_score}")

# Draw a card button for the player
if st.button("Draw Card"):
    st.session_state.player_card = draw_card()
    st.write(f"You drew: {st.session_state.player_card}")

# Play card button
if st.button("Play Card"):
    if st.session_state.player_card is None:
        st.warning("You need to draw a card first!")
    else:
        # CPU draws a card and plays
        st.session_state.cpu_card = cpu_turn()
        st.write(f"CPU drew: {st.session_state.cpu_card}")
        
        # Simple rule: if you draw a 'Wild +4', you gain a point, and if CPU draws it, it loses a point
        if 'Wild +4' in st.session_state.player_card:
            st.session_state.player_score += 1
            st.write("You gained a point!")
        elif 'Wild +4' in st.session_state.cpu_card:
            st.session_state.cpu_score -= 1
            st.write("CPU loses a point!")
        
        # Reset cards after play
        st.session_state.player_card = None
        st.session_state.cpu_card = None

# Reset game button
if st.button("Reset Game"):
    st.session_state.player_score = 0
    st.session_state.cpu_score = 0
    st.session_state.player_card = None
    st.session_state.cpu_card = None
    st.write("Game has been reset!")

# Game over condition
if st.session_state.player_score >= 5:
    st.write("You win!")
    st.button("Play Again?")
elif st.session_state.cpu_score >= 5:
    st.write("CPU wins!")
    st.button("Play Again?")
