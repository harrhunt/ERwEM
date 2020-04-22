import re
import json
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import corpus
from nltk import pos_tag


class TextCleaner:

    stop = stopwords.words("english")
    english = set(corpus.words.words())

    @staticmethod
    def letters(text, replace=" "):
        text = text.lower()
        return re.sub(r"[^a-zA-Z]+", replace, text)

    @classmethod
    def count_english_noun_verb(cls, text):
        words = pos_tag(word_tokenize(text))
        raw_data = {}
        for word in words:
            lower_word = word[0].lower()
            if lower_word not in cls.stop:
                if lower_word in cls.english and len(lower_word) > 2:
                    if "NN" in word[1] or "VB" in word[1]:
                        if lower_word not in raw_data:
                            raw_data[lower_word] = 1
                        else:
                            raw_data[lower_word] += 1
        return raw_data

    @staticmethod
    def exclude(text):
        if isinstance(text, str):
            text = text.split(" ")
        with open('data/words.json') as json_file:
            words = json.load(json_file)
        trimmed = []
        for string in text:
            if string in words:
                trimmed.append(string)
        return trimmed
