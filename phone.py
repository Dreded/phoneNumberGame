#!/bin/python
import random
import os
import getch
import yaml

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fileExists(file):
    return os.path.exists(file)

def loadSecretsFile():
    secretsFileName = 'secrets.yml'

    if not fileExists(secretsFileName):
        print('No secrets file, using example data.')
        secretsFileName = 'secrets.yml.example'

    global phoneNumbers
    with open(secretsFileName,'r') as f:
        secrets = yaml.safe_load(f)
        phoneNumbers = secrets['phoneNumbers']
    print(f"Loaded {len(phoneNumbers)} names/numbers")

def menuSelect(numbers):
    msg = ''
    while True:
        i = 0
        clearScreen()
        print(msg, end='')
        print('Please choose the number to memorize.')
        for person in numbers:
            print(f"\t{i+1}) {person['name']}") 
            i+=1
        selection = getch.getch()
        try:
            selection = int(selection)
        except ValueError:
            selection = -1
        if not type(selection) == type(1):
            msg = f'Error: Please enter a number from below.\n'
            continue
        if not selection <= len(numbers) or selection < 1:
            msg = f'Error: Please enter a number from 1-{len(numbers)}\n'
            continue
        return numbers[selection-1]


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

def cleanNumber(number):
    number = str(number)
    number = number.replace("-","")
    number = number.replace(" ","")
    number = number.replace("(","")
    number = number.replace(")","")
    if len(number) < 10 or len(number) > 10:
        clearScreen()
        print('ERROR: The Phone Number must be 10 digits.')
        print(f'Loaded: {number} which is {len(number)} digits')
        os._exit(1)
    number = list(map(int,number))
    return number

def printLevelMessage(level, name):
    msg = ''
    if level == 1:
        msg += f"We are missing {level} digits"
    else:
        msg += f'Now we are Missing {level} digits'
    msg += f' of {name}\'s Phone Number.'
    print(msg)

def game(name, number, attempts = 4, difficulty = 0):
    
    number = cleanNumber(number)
    lose = False
    while difficulty < 10:
        difficulty += 1
        missingNums = getMissing(difficulty)
        msg = ''
        while len(missingNums) > 0 and lose == False:
            clearScreen()
            printLevelMessage(difficulty, name)
            print(getPhoneNumber(missingNums, number))
            print(msg, end='')
            msg = ''

            print('What is the FIRST missing Digit?')
            while True:
                key = getch.getch()
                try:
                    if int(key) == number[missingNums[0]]:
                        missingNums.pop(0)
                        break
                except ValueError:
                    msg = 'ERROR: Please enter a digit from 0-9.\n'
                    break

                else:
                    attempts -= 1
                    if attempts != 0:
                        msg = f'Try again! {attempts} attempt(s) left.\n'
                    else:
                        lose = True
                    break
        
    clearScreen()
    if lose:
        msg = 'You Lose!'
    else:
        msg = f'Correct {name}\'s Phone Number is: {getPhoneNumber([-1], number)}'
    print(msg)

def checkShowNumber(name,number):
    clearScreen()
    show = 'n'
    print('Show the number before we start? [N,y]')
    show = getch.getch()
    if show == 'y':
        clearScreen()
        print(f'{name}\'s Phone Number is: {number}')
        print('Press any key when Ready to Play')
        getch.getch()

loadSecretsFile()

playAgain = 'y'
while playAgain == 'y':
    selection = menuSelect(phoneNumbers)
    name = selection['name']
    number = selection['number']
    checkShowNumber(name,number)
    game(name,number)
    print('Play again? [y,N]: ')
    playAgain = getch.getch()