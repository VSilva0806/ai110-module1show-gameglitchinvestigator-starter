import random
import streamlit as st
from logic_utils import (
    calculate_closeness,
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
    get_hot_cold_hint
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    # FIX: Reset game when difficulty changes
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0  # FIX: Reset on difficulty change
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_details = []
    st.session_state.best_guess = None

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "guess_details" not in st.session_state:
    st.session_state.guess_details = []

if "best_guess" not in st.session_state:
    st.session_state.best_guess = None

if "high_scores" not in st.session_state:
    st.session_state.high_scores = {"Easy": None, "Normal": None, "Hard": None}

if "game_history" not in st.session_state:
    st.session_state.game_history = []

st.sidebar.divider()
st.sidebar.subheader("🏆 Guess History")

best_guess_won = (
    st.session_state.best_guess
    and st.session_state.best_guess["outcome"] == "Win"
)
if best_guess_won:
    st.sidebar.success(
        f"✨ **WINNER!** Secret: {st.session_state.secret}\n\n"
        f"Best Guess: {st.session_state.best_guess['guess']}\n"
        f"Off by: {st.session_state.best_guess['closeness']}"
    )
elif st.session_state.best_guess:
    st.sidebar.info(
        f"🎯 **Best Guess:** {st.session_state.best_guess['guess']}\n\n"
        f"Off by: {st.session_state.best_guess['closeness']} units"
    )

if st.session_state.guess_details:
    st.sidebar.write("**All Guesses:**")
    for record in st.session_state.guess_details:
        closeness = record["closeness"]
        if closeness <= 5:
            distance_emoji = "🔥"
        elif closeness <= 15:
            distance_emoji = "🌡️"
        else:
            distance_emoji = "❄️"
        st.sidebar.caption(
            f"{distance_emoji} #{record['attempt']}: {record['guess']} "
            f"(off by {record['closeness']}) - {record['outcome']}"
        )

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.guess_details = []
    st.session_state.best_guess = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)
        # Removed dangerous comparison logic that converted secret to
        # string, causing wrong hints

        closeness = calculate_closeness(guess_int, st.session_state.secret)
        guess_record = {
            "guess": guess_int,
            "closeness": closeness,
            "outcome": outcome,
            "attempt": st.session_state.attempts
        }
        st.session_state.guess_details.append(guess_record)

        is_better_guess = (
            st.session_state.best_guess is None
            or closeness < st.session_state.best_guess["closeness"]
        )
        if is_better_guess:
            st.session_state.best_guess = guess_record

        if show_hint:
            st.warning(message)

            # Display Hot/Cold emoji hint
            hot_cold_hint = get_hot_cold_hint(closeness)
            st.info(f"**Temperature:** {hot_cold_hint} (Off by {closeness} units)")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
