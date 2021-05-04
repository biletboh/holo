import re
import pandas as pd
import nltk
import requests

from tokenize_uk import tokenize_words
from uk_stemmer import UkStemmer


nltk.download("punkt")
stemmer = UkStemmer()


CONCEPTS = "колаборація, співпраця, нацисти, допомога, євреї, порятунок, жертви, голодомор, польський, табір, смерть, концентраційний"


def clean_text(text):
    text = re.sub(r"""['’"`�]""", "", text)
    text = re.sub(r"""([0-9])([\u0400-\u04FF]|[A-z])""", r"\1 \2", text)
    text = re.sub(r"""([\u0400-\u04FF]|[A-z])([0-9])""", r"\1 \2", text)
    text = re.sub(r"""[\-.,:+*/_]""", " ", text)
    return text


def ua_tokenize(text):
    text = clean_text(text)
    response = requests.post(
        "http://localhost:8080/lemmatize/", json={"text": text}
    ).json()
    lemmatized = response["lemmatizedSentences"]
    word_list = []
    for lemma in lemmatized:
        tokens = tokenize_words(lemma)
        for token in tokens:
            stemmed = stemmer.stem_word(token)
            word_list.append(stemmed)
    return word_list


def word_frequency(text, concept):
    words: list[str] = ua_tokenize(text.lower())
    fd = nltk.FreqDist(words)
    return fd[concept]


def read_data(sheet_name):
    data = pd.read_excel("data/articles.xlsx", sheet_name=sheet_name)
    return data


def process_data():
    data = read_data("Історична правда")
    data.dropna(how="all", axis=1, inplace=True)
    concepts = ua_tokenize(CONCEPTS)
    for concept in concepts:
        data[concept] = data["Текст"].apply(word_frequency, args=(concept,))
    data.to_excel(
        "data/result.xlsx", sheet_name="Історична правда", index=False
    )


if __name__ == "__main__":
    process_data()
