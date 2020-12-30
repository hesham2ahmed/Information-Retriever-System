from QueryPreProcessing import normalize
import math
import tabulate

query = []
table = {}


def calcTFWeight(tf):
    if tf > 0:
        return 1 + math.log(tf, 10)
    return 0


def calcIDF(n, df):
    return math.log(n / df, 10)


def calcTFIDF(tf_weight, idf):
    return tf_weight * idf


# [[term,tf, df, tf_weight, idf, tf_idf, length,normalize]]
def calcLength(ls):
    sum = ls[0][5] ** 2
    for row in ls[1:]:
        sum += row[5] ** 2

    return math.sqrt(sum)


# [[term,tf, df, tf_weight, idf, tf_idf, length,normalize]]
def calcNormalize(doc_length, ls):
    for row in ls:
        row.append(doc_length)
        if doc_length != 0:
            row.append(row[5] / doc_length)
        else:
            row.append(0)
    return ls


# [[term,tf, df, tf_weight, idf, tf_idf, length,normalize]]
def getTableForDoc(n, doc_id):
    result = []
    i = 0
    for term in query:
        df = 0
        tf = 0
        idf = 0
        tf_weight = 0
        tf_idf = 0
        if term in table:
            dic = table[term]
            if doc_id in dic:
                df = len(dic)
                tf = len(dic[doc_id])
                tf_weight = calcTFWeight(tf)
                idf = calcIDF(n, df)
                tf_idf = calcTFIDF(tf_weight, idf)
        result.append([query[i], tf, df, tf_weight, idf, tf_idf])
        i += 1

    doc_length = calcLength(result)
    result = calcNormalize(doc_length, result)

    return result


def getTableForQuery(n):
    result = []
    i = 0
    for token in query:
        tf = query.count(token)
        try:
            df = len(table[token])
            tf_weight = calcTFWeight(tf)
            idf = calcIDF(n, df)
            tf_idf = calcTFIDF(tf_weight, idf)
        except:
            df = 0
            tf_weight = 0
            idf = 0
            tf_idf = 0
        result.append([query[i], tf, df, tf_weight, idf, tf_idf])
        i += 1

    doc_length = calcLength(result)
    result = calcNormalize(doc_length, result)
    return result


def calcSimilarity(document_table, query_table):
    result = 0
    for i in range(len(query_table)):
        result += document_table[i][7] * query_table[i][7]
    return result


# [[term, tf, df, tf_weight, idf, tf_idf, length,normalize]]
def printTable(table):
    print(
        tabulate.tabulate(
            table,
            ["Term", "TF", "DF", "TF_Weight", "IDF", "TF_IDF", "Length", "Normalize"],
            tablefmt="pretty",
        )
    )


def run(files_ids, list_query, auxiliary_table, n):
    global query, table
    query = list_query
    table = auxiliary_table

    result_doc = {}
    for doc_id in files_ids:
        result_doc[doc_id] = getTableForDoc(n, doc_id)

    result_query = getTableForQuery(n)

    for key in result_doc:
        print("\n Doc:", key)
        printTable(result_doc[key])

    print("\n Query:")
    printTable(result_query)

    print("\n")
    for key, value in result_doc.items():
        print("Similarity of (", key, ", q ):", calcSimilarity(value, result_query))
    return


# run(
#     ["hesham", "software", "ff"],
#     {
#         "hesham": {"0": [1, 7, 3, 10, 20], "1": [1, 2, 3]},
#         "software": {"0": [2, 4], "2": [10]},
#         "Engineering": {"3": [1, 2, 3]},
#         "Engineer": {"4": [1, 2, 3]},
#     },
#     3,
# )
