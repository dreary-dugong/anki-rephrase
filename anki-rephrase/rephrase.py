import ollama


PROMPT = """
Rephrase the following question. You must keep the same meaning and
intended answer, but you should change the wording and/or sentence
structure to make it slightly harder to recognize. DO NOT RESPOND WITH
ANYTHING EXCEPT THE REWORDED QUESTION. NO PRELUDE, NO RECAP OF WHAT YOU
DID, NO EXPLANATION. JUST YOUR NEW QUESTION. The question is: 
"""

def rephrase(model, question):
    message = PROMPT + question
    rephrasing = ollama.chat(model=model, messages=[
        {
            'role':'user',
            'content': PROMPT,
        }
    ])

    return rephrasing
