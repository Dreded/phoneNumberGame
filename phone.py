#!/bin/python
import random
import os
import getch
import yaml

phoneNumbers = [
    {'name': "Bob Loblaw"},{'number': '555-555-5555'},
    {'name': "Test"},{'number': '555-555-5555'},
]
attempts = 4
difficulty = 9


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fileExists(file):
    return os.path.exists(file)

def loadSecretsFile():
    secretsFileName = 'secrets.yml'

    if not fileExists(secretsFileName):
        print('No secrets file, using example data.')
        return

    global phoneNumbers
    with open(secretsFileName,'r') as f:
        secrets = yaml.safe_load(f)
        phoneNumbers = secrets['phoneNumbers']
    print(f"Loaded {len(phoneNumbers)} names/numbers")


def getMissing(random_count):
    
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

def getPhoneNumber(rand, number):

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

def printLevelMessage(level, name):
    msg = ''
    if level == 1:
        msg += f"We are missing {level} digits"
    else:
        msg += f'Now we are Missing {level} digits'
    msg += f' of {name}\'s Phone Number.'
    print(msg)

def game(name, number, attempts, difficulty):
    
    number = str(number)
    number = number.replace("-","")
    number = list(map(int,number))
    lose = False
    while difficulty < 10:
        difficulty += 1
        missingNums = getMissing(difficulty)
        msg = ''
        while len(missingNums) > 0 and lose == False:
            clearScreen()
            printLevelMessage(difficulty, name)
            print(getPhoneNumber(missingNums, number))
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
        msg = f'Correct {name}\'s Phone Number is: {getPhoneNumber([-1], number)}'
    print(msg)

loadSecretsFile()
for each in phoneNumbers:
    game(each['name'], each['number'], attempts, difficulty)