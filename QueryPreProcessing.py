import string
import nltk
from nltk.corpus import stopwords


def checkSyntax(query):
    size = len(query)
    if query[0] == "'" and query[size - 1] == "'":
        return True
    elif query[0] == '"' and query[size - 1] == '"':
        return True
    else:
        return False


def removePunc(query):
    return query.translate(
        str.maketrans(string.punctuation, " " * len(string.punctuation))
    )


def tokenization(query):
    return nltk.word_tokenize(query)


def normalize(list_query):
    result = []
    stop_words = stopwords.words("english")
    for i in range(len(list_query)):
        token = list_query[i]
        token = token.lower()
        if token not in stop_words and token.isalpha():
            result.append(token)
    return result


def prepareQuery(query):
    if checkSyntax(query):
        query = query[1 : len(query) - 1]
        query = removePunc(query)
        query = tokenization(query)
        query = normalize(query)
        return query
    else:
        return False