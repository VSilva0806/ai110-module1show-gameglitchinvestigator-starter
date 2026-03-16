# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game did not run well as it gave me misleading hints based on my guesses. The hints would point me in the wrong direction and depending on the difficulty, the secret number would be out of bounds.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  One of the bugs I noticed was that the hints were inconsistent. Every time I guessed a number, the hint would specify that the secret number was lower, and then the game told me the number was higher than my first guess, and vice versa. Another bug I noticed was the guessing range and secret range was 1-100 on all the difficulties when it should have been different among each difficulty.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? I used Claude for this project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). 
The AI suggested I removed unnecessary and dangerous return statements in the check_guess function that caused incorrect hints. I verified the result by testing the game after the fix and saw that I was able to guess the number solely based on the hints.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The AI suggested that I remove a conditional that caused errors in how the hints were outputted and as I did, the error kept occuring. I inspected the code and found the real error and asked the AI to remove it. I tested the new code again with the AI's test cases and it passed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? 
I tested it throughly using edge cases in the game and in the given test file. 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
One of the tests I ran was testing the hinting mechanism. I tried variuous pairs of input numbers, and each time, the hints were valid.
- Did AI help you design or understand any tests? How?
AI helped me design the tests. I specifically asked it to refer a particular bug it fixed each time and generated random test cases for those.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
In the original app, the secret number kept changing because the random.randint() function was called outside streamlit's session block. So everytime something was interacted with, streamlit would reactivate the function causing a brand new secret number.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns can be seen as a recipe that gets cooked everytime you touch something. Session states can be thought of as memory preservation, so if something gets interacted with, nothing resets and everything preserves itself.
- What change did you make that finally gave the game a stable secret number?
The fix was to add a function that checks if the secret number already existed in the session before generating a new one.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  One habit from this project I want to reuse in future projects is guiding and focusing the AI on one particular problem at a time instead of simply typing in "Here's all the code, fix this".
- What is one thing you would do differently next time you work with AI on a coding task?
I would have it refer to a specific file where an issue is located so it does not have to scan everything everytime.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI generated code is not always perfect although it may look like it. Although it may do a lot of heavy-lifting for us, we still hold the responsibility to test the code thoroughly and validate it.

AI Comparison: 
I asked Claude and ChatGPT to help me fix the secret number/guessing range for each of the difficulties. Claude gave me a more readable and simple fix while ChatGPT gave me a more complicated code block to use. Claude was also better at explaining it in simple terms.