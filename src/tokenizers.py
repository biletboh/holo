import nltk
import re
import requests

from stempel import StempelStemmer
from tokenize_uk import tokenize_words
from uk_stemmer import UkStemmer


ua_stemmer = UkStemmer()
pl_stemmer = StempelStemmer.default()


def clean_text(text):
    text = re.sub(r"""['’"`�]""", "", text)
    text = re.sub(r"""([0-9])([\u0400-\u04FF]|[A-z])""", r"\1 \2", text)
    text = re.sub(r"""([\u0400-\u04FF]|[A-z])([0-9])""", r"\1 \2", text)
    text = re.sub(r"""[\-.,:+*/_]""", " ", text)
    return text


def ua_tokenizer(text):
    text = clean_text(text.lower())
    response = requests.post(
        "http://localhost:8080/lemmatize/", json={"text": text}
    ).json()
    lemmatized = response["lemmatizedSentences"]
    word_list = []
    for lemma in lemmatized:
        tokens = tokenize_words(lemma)
        for token in tokens:
            stemmed = ua_stemmer.stem_word(token)
            if stemmed not in word_list:
                word_list.append(stemmed)
    return word_list


def pl_tokenizer(text):
    text = clean_text(text.lower())

    word_list = []
    tokens = nltk.word_tokenize(text)
    for token in tokens:
        stemmed = pl_stemmer.stem(token)
        if stemmed not in word_list:
            word_list.append(stemmed)

    return word_list
