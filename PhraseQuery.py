import json
import math

Dictionary = {}


def skip(index, sqrt, size):
    result = index + sqrt
    if result < size:
        return result
    return index


# time complixity = size(ls1) + size(ls2)
def match(ls1, ls2):
    n = len(ls1)
    m = len(ls2)
    result = []
    i = 0
    j = 0
    skip_i = None
    skip_j = None
    sqrt_i = int(round(math.sqrt(n)))  # 3
    sqrt_j = int(round(math.sqrt(m)))  # 3
    while i < n and j < m:
        if ls2[j] - ls1[i] == 1:
            result.append(ls2[j])
            i += 1
            j += 1
        elif ls2[j] - ls1[i] > 1:  # ls1[i] < ls2[j]:
            skip_i = skip(i, sqrt_i, n)
            if ls2[j] - ls1[skip_i] == 1:
                i = skip_i
            else:
                while i < n and ls2[j] - ls1[i] > 1:  # ls1[i] < ls2[j]:
                    i += 1
        else:
            skip_j = skip(j, sqrt_j, m)
            # print(skip_j)
            if ls2[skip_j] - ls1[i] == 1:  # ls2[skip_j] == ls1[i]:
                j = skip_j
            else:
                while j < m and ls2[j] - ls1[i] < 1:  # ls2[j] < ls1[i]:
                    j += 1

    return result


# { 'key': [values]}, ['key': [pos_id]]
# { 'doc_id' : [pos_id] }, { 'doc_id' : [pos_id] }
# time comlixity = size(dic1) (size(dic1[key] + size(dic2[key]))
def mergeTwoDictionaries(dic1, dic2):
    # for each key in dic1 exist in dic2, add dic1 values to dic2 vlues
    # print("dic1: ", dic1)
    # print("dic2: ", dic2)
    result = {}
    for key in dic1:
        if key in dic2:
            # print("key ", key)
            temp = match(dic1[key], dic2[key])
            if len(temp) == 0:
                result.pop(key, None)
            else:
                result[key] = temp

    return result


# get matched Doc_id in one dictionary for all terms in query
# time = -> terms ((size(dic1) (size(dic1[key] + size(dic2[key])))
def searchForQuery(list_query):
    query_dic = Dictionary[list_query[0]]
    for token in list_query[1:]:
        query_dic = mergeTwoDictionaries(query_dic, Dictionary[token])
    return query_dic


def phraseQuery(dictionary, list_query):
    try:
        global Dictionary
        Dictionary = dictionary
        return searchForQuery(list_query)
    except:
        return {}


# print(
#     run(
#         {
#             "ahmed": {"1": [2], "2": [1]},
#             "hesham": {"1": [3], "2": [2]},
#         },
#         ["ahmed", "hesham"],
#     )
# )