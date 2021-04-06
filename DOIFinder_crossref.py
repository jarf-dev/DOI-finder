import sys
import os
import csv
from datetime import datetime

from unidecode import unidecode
import string

import pandas as pd

from difflib import SequenceMatcher

import requests

def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

def depuText(text):
    text=unidecode(text)
    text=text.translate(str.maketrans('','',string.punctuation))
    return text.lower()

# Función para mostrar una barra de progreso
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Imprime la nueva línea al terminar
    if iteration == total: 
        print()

def crossrefAPI(title):
    strURL = "https://api.crossref.org/works?query.bibliographic="
    r=requests.get(url=strURL+depuText(title))
    data=r.json()
    try:
        crDOI=data["message"]["items"][0]["DOI"]
        crURL=data["message"]["items"][0]["URL"]
        crTitle=data["message"]["items"][0]["title"][0]
        crSimi=similar(depuText(title),depuText(crTitle))
    except:
        crDOI=crURL=crTitle="hay problemas con el texto del título"
        crSimi=0.0
    return crDOI,crURL,crTitle,crSimi

filePath=os.getcwd()+"\\"
fileName=str(sys.argv[1])
fileInput=filePath+fileName

try:
    if os.path.exists(fileInput):
        datalist=pd.read_excel(fileInput)
        titleList=datalist.iloc[:,0]
        limitList=len(titleList)
        timeStamp=str(datetime.now().timestamp())
        fileOutput=timeStamp[-6:].replace(".","")+fileName[:fileName.find('.')].upper()+'.csv'
        
        with open(fileOutput, 'w', newline='',encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["TituloOriginal", "CrossRefDOI","CrossRefURL", "CrossRefTitulo","CrossRefSimilaridad"])
            # inicializa la barra de progreso
            printProgressBar(0, limitList, prefix = 'Progreso:', suffix = 'Completado', length = 50)

            for i,title in enumerate(titleList):
                crDOI,crURL,crTitle,crSimi = crossrefAPI(title)
                writer.writerow([title, crDOI,crURL,crTitle,crSimi])

                # actualiza el progreso
                printProgressBar(i + 1, limitList, prefix = 'Progreso:', suffix = 'Completado', length = 50)
    else:
        print("***Hubo un problema con el archivo indicado. Verifique que éste existe y que tenga extensión '.xlsx'***")
        print("El archivo indicado fue: "+fileName)
except:
    print("***Hubo un problema con el archivo indicado. Verifique que éste existe y que tenga extensión '.xlsx'***")
    print("El archivo indicado fue: "+fileName)