from nltk.corpus import stopwords
import nltk
import string

# input
# [[file1], [file2], [file3]]
def removePunc(files):
    for i in range(len(files)):
        files[i] = files[i].translate(
            str.maketrans(string.punctuation, " " * len(string.punctuation))
        )
    return files


# input
# [[file1], [file2], [file3]]
def tokenization(files):
    for i in range(len(files)):
        files[i] = nltk.word_tokenize(files[i])
    return files


# input
# [[term1,term2,term3]]
def givePositions(files):
    i = 0
    j = 0
    pos = 0
    for i in range(len(files)):
        for j in range(len(files[i])):
            if len(files[i][j]) != 0:
                pos += 1
            files[i][j] = [files[i][j], pos]
        pos = 0
    return files


# input
# [[token1,token2,token3]]
def normalize(files):
    stop_words = stopwords.words("english")
    for i in range(len(files)):
        for j in range(len(files[i])):
            token = files[i][j]
            token = token.lower()
            if token not in stop_words and token.isalpha():
                files[i][j] = token
            else:
                files[i][j] = ""
    return files


# input
# [[[term1, pos],[term1, pos],[term1, pos],[term1, pos],[term1, pos]]]
# output
# [[term1, doc_id, pos],[term2, doc_id, pos],[term3, doc_id, pos]
def flatten(files_ids, files):
    result = []
    doc_id = 0
    for i in range(len(files)):
        for j in range(len(files[i])):
            if len(files[i][j][0]) != 0:
                files[i][j] = [files[i][j][0], files_ids[doc_id], files[i][j][1]]
                result.append(files[i][j])
        doc_id += 1
    return result


def preProcessing(files_ids, files):
    files = removePunc(files)
    files = tokenization(files)
    files = normalize(files)
    files = givePositions(files)
    files = flatten(files_ids, files)
    return files
