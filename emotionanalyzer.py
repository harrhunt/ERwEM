import json
import os
from nrclexicon import NRCLexicon


class EmotionAnalyzer:
    data = {}

    def __init__(self, name, text=None):
        self.path = "data/artefacts/" + name + "/"
        self.filename = name + ".json"
        self.name = name
        self.data["text"] = text
        self.mode_scale = {
            "locrian": -1,
            "phrygian": (-2 / 3),
            "aeolian": (-1 / 3),
            "dorian": 0,
            "mixolydian": (1 / 3),
            "ionian": (2 / 3),
            "lydian": 1
        }
        # self.__load()

    def analyze(self):
        self.data["emotions"] = {}
        for word in self.data["text"]:
            if word in NRCLexicon.data:
                for emotion in NRCLexicon.data[word]:
                    if emotion not in self.data["emotions"]:
                        self.data["emotions"][emotion] = NRCLexicon.data[word][emotion]
                    else:
                        self.data["emotions"][emotion] += NRCLexicon.data[word][emotion]
        self.__mode()
        self.__save()

    def print_data(self):
        posneg = self.data["emotions"]["Positive"] + self.data["emotions"]["Negative"]
        other = self.data["emotions"]["Anger"] + self.data["emotions"]["Anticipation"] + self.data["emotions"][
            "Disgust"] + self.data["emotions"]["Fear"] + self.data["emotions"]["Joy"] + self.data["emotions"][
                    "Sadness"] + self.data["emotions"]["Surprise"] + self.data["emotions"]["Trust"]
        for emotion in self.data["emotions"]:
            if emotion in "Positive" or emotion in "Negative":
                print(f"{emotion}: {round((self.data['emotions'][emotion] / posneg) * 100, 3)}")
            else:
                print(f"{emotion}: {round((self.data['emotions'][emotion] / other) * 100, 3)}")
        print(f"Musical Mode: {self.data['mode']}")

    def __mode(self):
        positive = self.data["emotions"]["Positive"]
        negative = self.data["emotions"]["Negative"]
        total = positive + negative
        if positive > negative:
            score = positive / total
        else:
            score = negative / total * -1
        closest = 1
        mode = "lydian"
        for key in self.mode_scale:
            distance = score - self.mode_scale[key]
            if abs(distance) < closest:
                closest = distance
                mode = key
        self.data["mode"] = mode

    def __save(self):
        if not os.path.exists(f"{self.path}"):
            os.makedirs(self.path)
        with open(f"{self.path}{self.filename}", "w") as file:
            json.dump(self.data, file)

    def __load(self):
        if os.path.exists(f"{self.path}{self.filename}"):
            with open(f"{self.path}{self.filename}", "r") as file:
                self.data = json.load(file)
