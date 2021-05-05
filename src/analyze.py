import pandas as pd
import nltk

from tokenizers import ua_tokenizer, pl_tokenizer


nltk.download("punkt")


CONCEPTS_UA = "колаборація, співпраця, нацисти, допомога, євреї, порятунок, жертви, голодомор, польський, табір, смерть, концентраційний"

CONCEPTS_PL = "antysemicki, holocaust"


def word_frequency(text, concept, language):
    if language == "pl":
        words: list[str] = pl_tokenizer(text)
    else:
        words: list[str] = ua_tokenizer(text)

    fd = nltk.FreqDist(words)
    return fd[concept]


def get_concepts(language):
    if language == "pl":
        concepts = pl_tokenizer(CONCEPTS_PL)
    else:
        concepts = ua_tokenizer(CONCEPTS_UA)
    return concepts


def gather_statistics(path, language):
    data = pd.read_csv(path)
    data.dropna(how="all", axis=1, inplace=True)

    concepts = get_concepts(language)

    for concept in concepts:
        data[concept] = data["Текст"].apply(
            word_frequency, args=(concept, language)
        )

    data.to_csv(
        "data/statistics.csv",
        index=False,
    )


def aggregate_statistics(language):
    data = pd.read_csv("data/statistics.csv")
    concepts = get_concepts(language)
    columns = ["Рік"] + concepts
    timeline = data[columns].groupby("Рік").sum()
    timeline.to_csv(
        "data/timeline_statistics.csv",
    )
