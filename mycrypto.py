import plotly.express as px
import pandas as pd
import numpy as np
from collections import Counter
from scipy.stats import chisquare
import re

Alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
AlphabetUpper=[chr(i) for i in range(65, 91)]


def moveString(inputStr, step):
    newStr = inputStr[-step:]+inputStr[:-step]
    return newStr

def countCoincidance(str1, str2):
    count = 0
    # print(str(len(str1))+' '+str(len(str2)))
    for i in range(0, len(str1)):
        if(str1[i] == str2[i]):
            count +=1
    return count/len(str1)

def XorChars(a, b):
    return chr(ord(a) ^ b)

def calculateChiSquredToEnglish(inputText):
    text = re.sub("[^a-zA-Z]+", "", inputText)
    letters_frequency_list = [];
    counts = Counter(text);
    for letter in Alphabet:
        letters_frequency_list.append(counts[letter]/len(text)*100 if letter in counts else 0)
    print(letters_frequency_list)
    result = chisquare(letters_frequency_list,
              f_exp=[8.2, 1.5, 2.8, 4.3, 13, 2.2, 2, 6.1, 7, 0.15, 0.77, 4, 2.4, 6.7, 7.5, 1.9, 0.095, 6, 6.3, 9.1, 2.8,
                     0.98, 2.4, 0.15, 2, 0.074])
    print(result)
    return result.pvalue

def calculateMetricsForDifferentKeys(text):
    key_list = []
    char_list=[]
    chi_square_list = []
    for key in range(0, 255):
        key_list.append(key);
        char_list.append(chr(key))
        chi_square_list.append(calculateChiSquredToEnglish(''.join([XorChars(i, key) for i in text])))
    d = {'key': key_list, 'chi square metrics': chi_square_list, 'char': char_list}
    df = pd.DataFrame(d)
    # print(df)
    fig = px.bar(df, x="char", y='chi square metrics')
    fig.show()
    return char_list[chi_square_list.index(max(chi_square_list))]

def kasiski(input):
    shift_list = []
    coincidance_rate_list = []
    for i in range(1, len(input)):
        shift_list.append(i)
        shiftedString =  moveString(input, i)
        # print(shiftedString)
        coincidance_rate_list.append(countCoincidance(input, shiftedString))

    d = {'index': shift_list, 'coincidance_rate': coincidance_rate_list}
    df = pd.DataFrame(d)
    # print(df)
    fig = px.bar(df, x="index", y='coincidance_rate')
    fig.show()
    return shift_list, coincidance_rate_list