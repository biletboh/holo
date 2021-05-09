import pandas as pd
import nltk
import matplotlib.pyplot as plt

from tokenizers import ua_tokenizer, ua_tokenizer2, pl_tokenizer


nltk.download("punkt")


def word_frequency(text, concept, language):
    if language == "pl":
        words: list[str] = pl_tokenizer(text)
    else:
        words: list[str] = ua_tokenizer(text)

    fd = nltk.FreqDist(words)
    return fd[concept]


def get_concepts(language, words):
    if language == "pl":
        concepts = pl_tokenizer(words)
    else:
        concepts = ua_tokenizer(words)
    return concepts


def gather_statistics(file_name, language, words):
    data = pd.read_csv("data/" + file_name)
    data.dropna(how="all", axis=1, inplace=True)

    concepts = get_concepts(language, words)

    for concept in concepts:
        data[concept] = data["Текст"].apply(
            word_frequency, args=(concept, language)
        )

    data.to_csv(
        "data/statistics.csv",
        index=False,
    )


def find_most_common(file_name, language):
    data = pd.read_csv("data/" + file_name)
    data.dropna(how="all", axis=1, inplace=True)
    text = data["Текст"].sum(axis=0)

    if language == "pl":
        words: list[str] = pl_tokenizer(text)
    else:
        words: list[str] = ua_tokenizer2(text)

    fd = nltk.FreqDist(words)
    common = pd.DataFrame(fd.most_common(500))
    common.to_csv("data/most_common.csv")


def aggregate_statistics(file_name, language, words):
    data = pd.read_csv("data/statistics.csv")
    concepts = get_concepts(language, words)
    columns = ["Рік"] + concepts
    timeline = data[columns].groupby("Рік").sum()
    timeline.to_csv("data/timeline.csv")


def create_plot():
    data = pd.read_csv("data/timeline.csv")
    data.plot(x="Рік")
    plt.show()
