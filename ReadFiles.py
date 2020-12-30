import os
import fitz


def listFiles(path):
    files = []
    for file in os.listdir(path):
        files.append(path + file)

    return files


def readPdf(pdf):
    result = ""
    pdf_read = fitz.open(pdf)
    for i in range(pdf_read.pageCount):
        page = pdf_read.loadPage(i)
        page = page.getText("text")
        result += page
    pdf_read.close()
    return result


# ["files/doc_names"]
def readMultiplePdfFiles(list_files):
    result = []
    for file in list_files:
        result.append(readPdf(file))

    return result


def readFiles(path):
    list_files = listFiles(path)
    return readMultiplePdfFiles(list_files)