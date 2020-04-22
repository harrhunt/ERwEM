import json
import os


class NRCLexicon:
    data = {}
    if os.path.exists("data/emotion_lexicon.json"):
        with open("data/emotion_lexicon.json", "r") as file:
            data = json.load(file)
