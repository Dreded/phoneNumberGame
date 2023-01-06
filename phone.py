#!/bin/python
import random
import os
import getch

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

number = [5,5,5,5,5,5,5,5,5,5]
name = 'Bob Loblaws'
attempts = 4
difficulty = 9

def getMissing(random_count, missingNums = None):
    
    rand = []
    i = 0
    while i < random_count:
        _rand = random.randint(0,9)
        while _rand in rand:
            _rand = random.randint(0,9)
        rand.append(_rand)
        i += 1
    rand.sort()

    return rand

def getPhoneNumber(rand):

    phoneNumber = ''
    i = 0
    for num in number:
        if i in rand:
            phoneNumber += '_'
        else:
            phoneNumber += str(num)
        i+=1
        if i == 3 or i == 6:
            phoneNumber += '-'
    
    return phoneNumber

def printLevelMessage(level):
    msg = ''
    if level == 1:
        msg += f"We are missing {level} digits"
    else:
        msg += f'Now we are Missing {level} digits'
    msg += ' of Mom\'s Phone Number.'
    print(msg)

lose = False
while difficulty < 10:
    difficulty += 1
    missingNums = getMissing(difficulty)
    msg = ''
    while len(missingNums) > 0 and lose == False:
        clearScreen()
        printLevelMessage(difficulty)
        print(getPhoneNumber(missingNums))
        if msg != '':
            print(msg)
        print('What is the FIRST missing Digit?')
        while True:
            key = getch.getch()
            if int(key) == number[missingNums[0]]:
                missingNums.pop(0)
                break

            else:
                attempts -= 1
                if attempts != 0:
                    msg = f'Try again! {attempts} attempt(s) left.'
                else:
                    lose = True
                break
    
clearScreen()
if lose:
    msg = 'You Lose!'
else:
    msg = f'Correct {name} Phone Number is: {getPhoneNumber([-1])}'
print(msg)
