from aqt import mw
from aqt import gui_hooks
from aqt.operations import QueryOp

from anki.models import ModelManager

import requests
import json
from dataclasses import dataclass

# constants
# the prompt for the llm
PROMPT = """
Rephrase the following question. You must keep the same meaning and
intended answer, but you should change the wording and/or sentence
structure to make it slightly harder to recognize. If possible, try to keep
the wording of the question at the same level of complexity. For example, 
if the user asks a short question with common words, your rephrase should 
ideally also be a short question composed of common words. DO NOT RESPOND 
WITH ANYTHING EXCEPT THE REWORDED QUESTION. NO PRELUDE, NO RECAP OF WHAT 
YOU DID, NO EXPLANATION. JUST YOUR NEW QUESTION. The question is: 
"""
# the field on the card where we save the orginal question
STORAGE_NOTE = "_originalQuestion"


@dataclass
class Model:
    """represent the remote ai model we use to rephrase cards"""
    name: str
    domain: str
    port: str

    def get_endpoint(self):
        return "http://" + self.domain + ":" + self.port + "/api/generate"


def rephraseCardInBackground(_reviewer, card, _ease):
    # quickly grab the info we'll need
    config = mw.addonManager.getConfig(__name__)
    modelName = config['model']
    domain = config['domain']
    port = config['port']
    model = Model(modelName, domain, port)

    # start background thread
    op = QueryOp(
        parent=mw,
        op=lambda col: rephraseCard(card, model),
        success=lambda *args: None
    )
    op.run_in_background()
    return


def rephraseCard(card, model):

    notes = card.note()
    # if the card doesn't have an _originalQuestion field, we need to add it
    if STORAGE_NOTE not in notes:
        addStorageNote(card)
        notes = card.note()
    
    question = notes["Front"]
    
    # if the note type already has a space for the original question,
    # but it hasn't been set yet, set it now
    if notes[STORAGE_NOTE] == "":
        notes[STORAGE_NOTE] = question
        mw.col.update_note(notes) # save to the database
    
    # rephrase the orginal question to avoid snowballing question complexity
    question = notes[STORAGE_NOTE]
    
    # finally, replace the question with a rephrasing from our LLM
    rephrasing = rephrase(question, model)
    notes["Front"] = rephrasing
    mw.col.update_note(notes)
    return


def addStorageNote(card):
        """given a card without a field to store the original question,
        add such a field to the card's noteType"""
        notes = card.note()
        modelManager = mw.col.models
        noteType = notes.note_type()

        newField = modelManager.new_field(STORAGE_NOTE)
        modelManager.add_field(noteType, newField)
        modelManager.update_dict(noteType)
        card = mw.col.get_card(card.id)
        return


def rephrase(question, model):
    """connect to ollama and ask for a rephrasing of our question"""
    prompt = PROMPT + question

    data = {"model":model.name, "prompt":prompt, "stream":False}
    response = requests.post(model.get_endpoint(), data=json.dumps(data))

    rephrasing = response.json()["response"]

    return rephrasing


# hook to run our rephrase when a card is answered
gui_hooks.reviewer_did_answer_card.append(rephraseCardInBackground)