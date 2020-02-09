import sys
import json
from colorama import Fore, Style
import expl
import mcq

if len(sys.argv) != 2:
    print(f"python {sys.argv[0]} <log>")
    exit(1)

f = open(sys.argv[1], 'r')
raw = f.read()
f.close()
data = json.loads(raw)


nWin = 0
nWin1 = 0
for i in range(12):
    question, answers = data[30][1][23][i][7], data[30][1][23][i][9]
    print('[*] ' + question)

    index, myanswer = expl.main(question, answers)
    myanswer2 = mcq.answer(question, answers)
    print('myanswer2: ', myanswer2)

    # print
    correct = data[30][1][23][i][9][data[30][1][23][i][15]]
    if correct == myanswer:
        print(f'[!] correct: {Fore.GREEN}{correct}{Style.RESET_ALL}')
        nWin += 1
    elif correct == myanswer2:
        print(f'[!] correct: {Fore.YELLOW}{correct}{Style.RESET_ALL}')
        nWin1 += 1
    else:
        print(f'[!] correct: {Fore.RED}{correct}{Style.RESET_ALL}')
    print('-----------------------------------------------------------------------')

print(f"won: {nWin}\nloss: {12-nWin}")
print(f"won1: {nWin1}\nlossr1: {12-nWin1}")
