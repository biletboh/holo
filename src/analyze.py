import pandas as pd


def read_data(sheet_name):
    data = pd.read_excel("articles.xlsx", sheet_name=sheet_name, header=None)
    return data


if __name__ == "__main__":
    print(read_data("історична правда"))
