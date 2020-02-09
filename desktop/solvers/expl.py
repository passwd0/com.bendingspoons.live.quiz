import google_api as google
from colorama import Fore, Style
import json
import sys
import re
import copy
import requests


def main(question, answers):
    f = open('toignore', 'r')
    raw = f.read()
    f.close()
    toIgnore = raw.split('\n')

    # SET FLAG
    if "NON" in question:
        NON = True
    else:
        NON = False

    # REMOVE WORDS
    question = re.sub('[,:?;!\.\(\)]', '', question)
    apice = False
    buf = []
    for word in question.split():
        if word[0] == "'":
            apice = True
        if apice:
            buf.append(word)
        if  not apice and (word[0].isupper() and question.index(word) != 0 and word != "NON") or word.isdigit():
            buf.append(word)
        if word[-1:] == "'" and apice:
            apice = False

    tmp = ' '.join(buf)
    if "'" in tmp:
        question = tmp
    else:
        question  = ' '.join([word for word in question.split() if word.lower() not in toIgnore])

    # GOOGLE
    results = google.search(question, answers)

    # counterTot / counterPar / tot
    compareList = ['counterTot', 'counterPar', 'tot']
    compare = 'counterPar'
    if results[max(results, key=(lambda key: results[key]['counterTot']))]['counterTot'] >= 3:
        compare = 'counterTot'
    else:
        if results[max(results, key=(lambda key: results[key]['counterPar']))]['counterPar'] >= 10:
            compare = 'counterPar'
        else:
            if results[max(results, key=(lambda key: results[key]['tot']))]['tot'] != 0:
                compare = 'tot'

    print(f'{Fore.LIGHTBLUE_EX}{compare}{Style.RESET_ALL}')

    # switcher
    myanswer = copy.deepcopy(results)
    for c in range(len(compareList)):  # nel caso ci siano 2 results uguali
        # ordino secondo il compare
        resultsSorted = sorted(myanswer, key=(lambda key: myanswer[key][compare]))
        if not NON:
            resultsSorted = resultsSorted[::-1]

        # elimino i dati che non combaciano con il primo elemento
        if myanswer[resultsSorted[0]][compare] != myanswer[resultsSorted[1]][compare]:
            if len(myanswer) > 2:
                myanswer.pop(resultsSorted[2])
            if len(myanswer) > 1:
                myanswer.pop(resultsSorted[1])
            break
        else:
            if len(myanswer) > 2 and myanswer[resultsSorted[1]][compare] != myanswer[resultsSorted[2]][compare]:
                myanswer.pop(resultsSorted[2])
            compare = compareList[(compareList.index(compare)+1)%len(compareList)]  # switch 

    myanswer = sorted(myanswer)[0]

    # print
    print(f'[!] results: {Fore.YELLOW}{results}{Style.RESET_ALL}')
    tot = sum(results[key][compare] for key in results)

    stats = list()
    for a in results:
        perc = round(results[a][compare]*100/tot, 2)
        if NON:
            perc = 100 - perc
        color = 'green' if a==myanswer else 'red'
        obj = {'answer': a, 'perc':str(perc), 'color': color }
        stats.append(obj)

    try:
        r = requests.post('http://liveanswer.me:3900/update', json=stats)
    except:
        print("info: liveanswer.me:3900/update failed to connect")

    # return correct index
    index = list(results.keys()).index(myanswer)
    print(index)    # deve rimanere l'ultimo output di questo programma (per ./expl)
    return index, myanswer    #for who import this script


if __name__ == '__main__':
    if len(sys.argv) == 2:
        data = json.loads(sys.argv[1])
        question = data['question']
        answers  = data['answers']
    else:
        print(f"python {sys.argv[0]} <json>")
        exit(0)

    main(question, answers)
