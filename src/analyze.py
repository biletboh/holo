import pandas as pd
import nltk


nltk.download("punkt")


word_bag = [
    "колаборація",
    "співпраця з нацистами",
    "допомога євреям",
    "порятунок жертв",
    "Голодомор",
    "польські табори смерті",
    "концентраційні",
]


def word_frequency(text, term):
    words: list[str] = nltk.word_tokenize(text.lower())
    fd = nltk.FreqDist(words)
    return fd[term]


def read_data(sheet_name):
    data = pd.read_excel("data/articles.xlsx", sheet_name=sheet_name)
    return data


def prepare_data():
    data = read_data("Історична правда")
    data.dropna(how="all", axis=1, inplace=True)
    for term in word_bag:
        data[term] = data["Текст"].apply(word_frequency, args=(term,))
    data.to_excel(
        "data/result.xlsx", sheet_name="Історична правда", index=False
    )


if __name__ == "__main__":
    prepare_data()
