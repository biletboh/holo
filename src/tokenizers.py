import nltk
import re
import requests

from stempel import StempelStemmer
from tokenize_uk import tokenize_words
from uk_stemmer import UkStemmer


ua_stemmer = UkStemmer()
pl_stemmer = StempelStemmer.default()

STOP_WORDS = [
    "у",
    "в",
    "як",
    "на",
    "і",
    "та",
    "з",
    "не",
    "що",
    "до",
    "бул",
    "про",
    "за",
    "а",
    "рок",
    "це",
    "так",
    "с",
    "для",
    "йог",
    "він",
    "вон",
    "й",
    "сам",
    "інш",
    "від",
    "є",
    "ал",
    "із",
    "під",
    "чи",
    "був",
    "також",
    "по",
    "том",
    "то",
    "їх",
    "одн",
    "ї",
    "ми",
    "и",
    "тог",
    "післ",
    "я",
    "кол",
    "лиш",
    "те",
    "аб",
    "р",
    "сво",
    "прот",
    "б",
    "де",
    "навіт",
    "мал",
    "цьог",
    "вже",
    "однак",
    "більш",
    "хоч",
    "стал",
    "хто",
    "можн",
    "щоб",
    "ж",
    "буд",
    "тут",
    "зі",
    "ці",
    "між",
    "все",
    "них",
    "тільк",
    "зокрем",
    "якщ",
    "наш",
    "їхн",
    "тод",
    "щод",
    "жодн",
    "перед",
    "серед",
    "тих",
    "о",
    "цьом",
    "всі",
    "ні",
    "через",
    "бо",
    "цих",
    "ті",
    "своїх",
    "мож",
    "деяк",
    "соб",
    "ним",
    "нас",
    "себ",
    "ця",
    "всіх",
    "адж",
    "цієї",
    "при",
    "цю",
    "би",
    "нам",
    "йом",
    "ніж",
    "цим",
]


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


def ua_tokenizer2(text):
    text = clean_text(text.lower())

    word_list = []
    tokens = nltk.word_tokenize(text)
    for token in tokens:
        if token.isalpha():
            stemmed = ua_stemmer.stem_word(token)
            if stemmed not in STOP_WORDS:
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
