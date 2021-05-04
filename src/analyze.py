import re
import pandas as pd
import nltk
import requests

from tokenize_uk import tokenize_words
from uk_stemmer import UkStemmer


nltk.download("punkt")
stemmer = UkStemmer()


CONCEPTS_UA = "колаборація, співпраця, нацисти, допомога, євреї, порятунок, жертви, голодомор, польський, табір, смерть, концентраційний"


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
            if stemmed not in word_list:
                word_list.append(stemmed)
    return word_list


def word_frequency(text, concept):
    words: list[str] = ua_tokenize(text.lower())
    fd = nltk.FreqDist(words)
    return fd[concept]


def gather_statistics():
    data = pd.read_excel("data/articles.csv")
    data.dropna(how="all", axis=1, inplace=True)
    concepts = ua_tokenize(CONCEPTS_UA)
    for concept in concepts:
        data[concept] = data["Текст"].apply(word_frequency, args=(concept,))
    data.to_excel(
        "data/articles_statistics.xlsx",
        sheet_name="Історична правда",
        index=False,
    )


def aggregate_statistics():
    data = pd.read_excel(
        "data/articles_statistics.xlsx", sheet_name="Історична правда"
    )
    columns = ["Рік"] + ua_tokenize(CONCEPTS_UA)
    timeline = data[columns].groupby("Рік").sum()
    timeline.to_excel(
        "data/timeline_statistics.xlsx",
        sheet_name="Історична правда",
    )
