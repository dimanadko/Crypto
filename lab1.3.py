import random
import pandas as pd
import numpy as np
from scipy.stats import chisquare
import math

# Write a code to attack some simple substitution cipher.
# To reduce the complexity of this one we will use only uppercase letters, so the keyspace is only 26!
# To get this one right automatically you will probably need to use some sort of genetic algorithm
# (which worked the best last year), simulated annealing or gradient descent.
# Seriously, write it right now, you will need it to decipher the next one as well.
# Bear in mind, there⁛ѐзs no spaces. https://docs.google.com/document/d/1AWywcUIMoGr_cjOMaqjqeSyAyzK93icQE4W-6bDELfQ

from mycrypto import AlphabetUpper

input = 'EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPVYWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQESPBLWPCSVRVWFLHLWFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYULEMQTLPPLUGUYOLWDTVSQETHQEKLPVPVSMTLEUPQEPCYAMEWWYTYWDLUULTCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUMQBQVMQCYAHUYKEKTCASLFPYFLMVHQLUPQLHULIVYASHEUEDUEHQBVTTPQLVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCPYFVIVFLPQLOLSSEDLVWHEUPSKCPQLWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGULXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGVWFEBECPYASLQVDQLUYUFLUGULXALWMCSPEPVSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPOEDVMETBYUFBVTTPENLPYPQLWLRPTEKLWZYCKVPTCSTESQPQULLGYAUMEHVPETFWMEHVPETBZMEHVPETB'

ALPHABET_START = 65

POPULATION_SIZE = 500
GENERATIONS_COUNT = 1000пше 
TOURNAMENT_WINNER_PERCENTAGE = 0.2
TOURNAMENT_PARENT_PERCENTAGE = 0.3
TOURNAMENT_WINNER_PROBABILITY = 0.95
MUTATION_CHILDREN_PERCENTAGE = 0.2
# TOURNAMENTS_AMOUNT = 60
TOURNAMENTS_AMOUNT = 2
ALPHABET = individual = [chr(i) for i in range(65, 91)]

engTrigrams = pd.read_csv('english_trigrams.csv', index_col='trigram')['frequency'].divide(100)

# print(engTrigrams)

def randBitList():
    key1 = []
    for i in range(len(ALPHABET)):
        key1.append(random.randint(0, 1))

    return (key1)

def listDiff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def chunkify(lst,n):
    return [lst[i::n] for i in range(n)]

def decryptSubstitution(input, key):
    result = ''.join([chr(key.index(letter)+ALPHABET_START) for letter in input])
    return result

def generateIndividual():
    individual = [chr(i) for i in range(65, 91)]
    random.shuffle(individual)
    # print(individual)
    return individual

def getTrigrams(text):
    result = pd.Series(dtype=int, index=engTrigrams.index.copy())
    result.values[:]=0
    # print(result)
    point1 = 0;
    point2 = 3;
    while point2<=len(text):
        if text[point1:point2] in result:
            result[text[point1:point2]] +=1
        else:
            result[text[point1:point2]] = 1
        point1 += 1
        point2 += 1
    sumTrigrams = sum(result.values)
    normResult = result.divide(other=sumTrigrams)
    return normResult

def scoreIndividual(individual):
    dechiferedText = decryptSubstitution(input, individual)
    curTrigrams = getTrigrams(dechiferedText)
    # print(curTrigrams)
    result = fitness(curTrigrams, engTrigrams)
    # print("result{}".format(result))
    return result, dechiferedText

def fitness(curTrigrams, engTrigrams):
    # print(engTrigrams.apply(math.log2))
    result = curTrigrams.multiply(engTrigrams.apply(math.log2)).sum()
    if result != result:
        print('********')
    return result

def getParticipant(participants):
    randomNumber = random.random()
    index = 1
    coef = TOURNAMENT_WINNER_PROBABILITY
    while randomNumber > coef:
        coef += TOURNAMENT_WINNER_PROBABILITY*(1-TOURNAMENT_WINNER_PROBABILITY)**index
        index +=1
    return index if index < len(participants) else participants[len(participants)-1]


def getWinner(tournamentParticipants):
    tournamentParticipants = [''.join(part) for part in tournamentParticipants]
    fitnessList = pd.Series(
        [scoreIndividual(participant) for participant in tournamentParticipants],
        index=tournamentParticipants
    ).sort_values(ascending=False)
    partId = getParticipant(fitnessList)
    print(fitnessList.values[partId])
    return fitnessList.keys()[partId]

def cureChild(defectChild):
    alphabet = [chr(i) for i in range(65, 91)]
    random.shuffle(alphabet)

    charOptions = listDiff(alphabet, defectChild)
    for geneInt in range(len(defectChild)):
        if(defectChild[geneInt] in defectChild[:geneInt]):
            defectChild[geneInt] = charOptions.pop();


def getChild(aParent, bParent):
    crossOverPoint = round(random.random()*len(aParent));
    aPart = aParent[0:crossOverPoint]
    bPart = bParent[crossOverPoint:]
    aPart2 = aParent[crossOverPoint:]
    bPart2 = bParent[0:crossOverPoint]
    defectChild = aPart+bPart
    defectChild2 = bPart2+aPart2
    cureChild(defectChild)
    cureChild(defectChild2)
    return defectChild, defectChild2


def getChildren(parents, childrenAmount):
    parents.iloc[np.random.permutation(len(parents))]
    children = []
    for index in range(int((childrenAmount)/2)):
        if(index*2 >= childrenAmount - childrenAmount*MUTATION_CHILDREN_PERCENTAGE):
            childA, childB = mutate(
                parents[index*2 % len(parents)],
                parents[(index*2-1) % len(parents)]
            )
            children.append(childA);
            children.append(childB);
        else:
            childA, childB = getChild(
                parents[index*2 % len(parents)],
                parents[(index*2-1) % len(parents)]
            )
            children.append(childA);
            children.append(childB);
    return children;

def mutate(parentA, parentB):
    bitList = randBitList()
    raw1 = [ parentA[index] if bitList[index] == 1 else None for index in range(len(bitList))]
    charOptions1 = listDiff(parentB, raw1)
    result1 = [ letter if letter else charOptions1.pop(0) for letter in raw1]
    raw2 = [ parentA[index] if bitList[index] != 1 else None for index in range(len(bitList))]
    charOptions2 = listDiff(parentA, raw2)
    result2 = [ letter if letter else charOptions2.pop(0) for letter in raw2]
    return result1, result2

def tournament(population, printResult):
    # print('len'+str(len(population)))
    # print(population)
    curPopulation = [''.join(part) for part in population]
    fitnessList = pd.Series(
        [scoreIndividual(participant) for participant in curPopulation],
        index=curPopulation
    ).sort_values(ascending=False)
    if(printResult):
        print('score:' + str(fitnessList[0][0]) + ',\nresult: ' + str(fitnessList[0][1]) + ',\nkey: '+fitnessList.index[0]+'\n-----------')
    winnersAmount = round(fitnessList.size*TOURNAMENT_WINNER_PERCENTAGE)
    parentsAmount = round(fitnessList.size*TOURNAMENT_PARENT_PERCENTAGE)
    childrenAmount = fitnessList.size-winnersAmount-parentsAmount;
    winners=pd.Series(fitnessList.index[0:winnersAmount].map(lambda el: list(el)))
    # @todo make parents random
    parentsFrom = fitnessList[winnersAmount:]
    randomArray = [i for i in range(parentsFrom.size)];
    random.shuffle(randomArray);
    parentsRaw = [fitnessList.index[winnersAmount:][randomArray[i]] for i in range(parentsAmount)]
    # parentMin = fitnessList[winnersAmount:].min();
    # parentMax = fitnessList[winnersAmount:].max();
    # parentSum = fitnessList[winnersAmount:].sum();
    # parentsFrom = fitnessList[winnersAmount:]
    # parentsRaw = []
    # for i in range(parentsAmount):
    #     randomValue = random.random()*(parentMax[0]-parentMin[0])+parentMin[0]
    #     for fintessIndex in range(len(parentsFrom)):
    #         # print(randomValue)
    #         # print(parentsFrom[fintessIndex][0])
    #         # print(parentsFrom[fintessIndex+1][0])
    #         if(randomValue<=parentsFrom[fintessIndex][0] and randomValue>=parentsFrom[fintessIndex+1][0]):
    #             parentsRaw.append(parentsFrom.index[fintessIndex])
    #             # print('-----------')
    #             # print(parentsFrom[fintessIndex])
    #             break
    # print([list(el) for el in parentsRaw])
    parents=pd.Series([list(el) for el in parentsRaw])
    parents=winners.append(parents, ignore_index=True)
    # print('parents len: '+str(len(parents.append(parents, ignore_index=True))));
    # print('parents len2: '+str(len(parents)));
    children=getChildren(parents, childrenAmount);
    # tournamentLists = chunkify(population, TOURNAMENTS_AMOUNT)
    # print(tournamentLists)
    # for tournamentParticipants in tournamentLists:
    #     winner = getWinner(tournamentParticipants)
    #     winners.append(winner)
    # results[fitness(individ) for individ in population]
    # print(winners.to_list())
    return(parents.to_list()+children)

population = [generateIndividual() for i in range(POPULATION_SIZE)]

# population.append(list('EKMFLGDQVZNTOWYHXUSPAIBRCJ'))
# population.append(list('EGFSVOHTLZIMNWYKJQUPADBRCX'))
# a = generateIndividual();
# b = generateIndividual();
# c = generateIndividual();
# print(c);
# print(a)
# print(b)
# child = getChild(a, b);
#
# print(decryptSubstitution(input, list('EKMFLGDQVZNTOWYHXUSPAIBRCJ')));

# print(child);
# print(listDiff(ALPHABET, child));
# print(mutate(a, b))
# print(getChildren(pd.Series([a, b, c]), 4))
currentPopulation = tournament(population, True);
# print(currentPopulation)
for i in range(GENERATIONS_COUNT):
    # print(currentPopulation)
    currentPopulation = tournament(currentPopulation, True if i%10==0 else False)
# individual = generateIndividual()
# decryptSubstitution(input, individual)

# curTrigrams = getTrigrams('ANDING')

# print(chunkify([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 4))
# print(curTrigrams);
# print(fitness(curTrigrams, engTrigrams))