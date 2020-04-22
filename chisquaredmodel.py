import json
import os.path
from textcleaner import TextCleaner


def create_data():
    with open("data/news/articles.OLD.json", "r") as file:
        articles = json.load(file)
    data = {'articles': {}, 'words': {}, 'totalxy': 0}
    for article in articles:
        words = TextCleaner.count_english_noun_verb(articles[article])
        if len(words) <= 0:
            continue

        # Initialize the user's fields
        data['articles'][article] = {}
        data['articles'][article]['words'] = words
        data['articles'][article]['totaly'] = 0

        # Update the totals for each word the user has
        for word in words:
            data['articles'][article]['totaly'] += words[word]
            if word not in data['words']:
                data['words'][word] = {}
            if 'totalx' not in data['words'][word]:
                data['words'][word]['totalx'] = words[word]
            else:
                data['words'][word]['totalx'] += words[word]

    return data


def compute_table_total():
    # Reset the model's total
    model['totalxy'] = 0

    # Make sure the total is the same for both x and y axis of the model
    word_total = 0
    article_total = 0
    for article in model['articles']:
        article_total += model['articles'][article]['totaly']
    for word in model['words']:
        word_total += model['words'][word]['totalx']
    print(f"User Total: {article_total}\nvs.\nWord Total: {word_total}")

    # If they are the same...
    if article_total == word_total:
        model['totalxy'] = article_total


def add_article(article, text):
    # If the person is not in the model...
    words = TextCleaner.count_english_noun_verb(text)
    if article not in model['articles']:
        # print("They were not in the table")

        # Add the person to the model
        model['articles'][article] = {}
        model['articles'][article]['totaly'] = 0

        # Update the totals in the table for words and the new user (totalx, totaly)
        update_table_totals(article, words)
    # If the user is not in the model...
    else:
        # print("They were in the table")

        # If the user does not have the exact same data as before...
        if set(words.keys()) != set(model['articles'][article]['words'].keys()) or set(
                words.values()) != set(model['articles'][article]['words'].values()):
            # print("They had different values from the ones in the table")

            # Subtract their previous values...
            for word in model['articles'][article]['words']:
                model['words'][word]['totalx'] -= model['articles'][article]['words'][word]
                model['totalxy'] -= model['articles'][article]['words'][word]

            # And add their new values
            update_table_totals(article, words)
    save_model()


def update_table_totals(article, words):
    # Reset the user's data to 0 and their words to their frequency count
    model['articles'][article]['words'] = words
    model['articles'][article]['totaly'] = 0

    # Update the totals for each word the user has
    for word in words:
        model['articles'][article]['totaly'] += words[word]
        if word not in model['words']:
            model['words'][word] = {}
        if 'totalx' not in model['words'][word]:
            model['words'][word]['totalx'] = words[word]
        else:
            model['words'][word]['totalx'] += words[word]


def calculate_article(article, text):
    # If the person is in the model
    if article in model['articles']:

        words = TextCleaner.count_english_noun_verb(text)

        # Set up needed variables
        person_prob = float(float(model['articles'][article]['totaly']) / float(model['totalxy']))
        grand_total = model['totalxy']
        interests = {}

        # For each word, calculate its Chi-Squared Contribution
        for word in words:
            word_prob = float(float(model['words'][word]['totalx']) / float(model['totalxy']))

            expected = word_prob * person_prob * grand_total
            observed = model['articles'][article]['words'][word]

            # CSC = ( (observed - expected) ^ 2 ) / expected
            csc = ((float(observed) - float(expected)) ** 2) / expected
            interests[word] = csc

        # Add the interests to the user object and print the interests
        save_model()
        return interests
    else:
        add_article(article, text)
        calculate_article(article, text)


def save_model():
    with open('data/chiSqModel.OLD.json', 'w') as file:
        json.dump(model, file)


def open_model():
    if not os.path.exists('data/chiSqModel.OLD.json'):
        data = create_data()
    else:
        with open('data/chiSqModel.OLD.json', 'r') as file:
            data = json.load(file)
    return data


if __name__ == "__main__":
    model = open_model()
    # model = create_data()
    compute_table_total()
    save_model()
else:
    model = open_model()
    compute_table_total()
