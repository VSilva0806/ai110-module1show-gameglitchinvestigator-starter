# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- The purpose in this game is to guess a number within a certain range.
- Several bugs I found included: misleading hints, unstable secret number, innacurate attempt count, improper boundaries.
- I used Claude AI to help me fix the boundaries based on difficulty and asked it to assist me in outputting accurate hints. I also was able to stabilize the secret number so it holds for the duration of a game.

## 📸 Demo

- Test run of the game:
- ![alt text](<Screenshot 2026-03-15 at 10.02.03 PM.jpg>)

Some edge case tests:
- ![alt text](<Screenshot 2026-03-15 at 10.16.24 PM.jpg>)

## 🚀 Stretch Features

Upgraded User Interface:
- ![alt text](<Screenshot 2026-03-15 at 10.24.06 PM.jpg>)

The agent implemented a guess history that showed the player's previous guesses in each game to let the player visualize how close their score was to the target. The agent also added a hot/cold meter to give make the UI more lively and engaging.
