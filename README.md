# Ollama Rephrase

Use a local LLM to rephrase anki cards for you so you can learn the content
instead of just memorizing the question



https://github.com/user-attachments/assets/ccba24b1-9a7d-4065-84d2-713ac3cf7cba



## The Problem
If you've used spaced repetition tools or flash cards long enough, you've
probably found yourself being able to answer the question on the card just
by reading the first two words. This is bad. This means you memorized the 
question and when you review the card, you're not really thinking about the
content and promoting learning, you're just regurgitating the pattern you
memorized. 

## Our Solution
One way to avoid memorizing the question is to change the question every
time you answer it. This would be very tedious to do yourself, but it's 
trivial for even the smallest large language models. This Anki add-on uses
a small LLM running locally via Ollama to slightly alter the wording of the
question on each card once you answer them. The original question on the 
card is still preserved and can be viewed in browse mode. 

## How To Use
By default, ollama-rephrase looks for an ollama server running on the
default ollama port on localhost and attempts to connect to it and pass a 
prompt to llama3.1:8b. The host, port, and model are all configurable from
within anki's add-on configuration menu. For more info on setting up Ollama,
see [ollama/ollama](https://github.com/ollama/ollama).

## Roadmap
- [] save rephrased question to another field so it's only shown when 
plugin is active (e.g. don't show rephrased questions on mobile)
- [] button for reverting a card back to its original wording
- [] button for rephrasing a card on-demand
- [] mark a rephrasing as bad (to avoid in the future)
- [] tag to never rephrase card
- [] disable/enable plugin
- [] avoid rephrasing certain important words or phrases (marked in bold?)