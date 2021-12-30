#import word list, make sure file is in same folder
from itertools import count, permutations
import random
from typing import cast

#get random words
f = open("words_alpha.txt","r")
random_words = f.read().split()
f.close()

#already used words
used_words = []

#get wheel segments
f = open("segments.txt","r")
segments = f.read().split()
f.close()


temp_bank = {1:0, 2:0, 3:0}
overall_bank = {1:0, 2:0, 3:0}

#global variables =============================================================================================

round_counter = 1

players = [1,2,3]
started_already = []

consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]
vowels = ["a","e","i","o","u"]
RSTLNE = ["r","s","t","l","n","e"]
vowel_price = 250

solved = False

#functions=======================================================================================================

def turn_choice():
    print("1. Spin Wheel")
    print("2. Buy Vowel")
    print("3. Solve Puzzle")

def solve():
    guess = str(input("Solve the puzzle: "))
    while True:
        global overall_bank
        global temp_bank
        if guess in guessed_words:
            print("That word has already been guessed.")
            print(guessed_words)
            break
        elif guess != word:
            guessed_words.append(guess)
            print("That is not correct.")
            break
        else:
            global solved
            solved = True
            print("Congrats! You solved the puzzle!")
            #transfer money won in round to overall_bank
            overall_bank[current_player] += temp_bank[current_player]
            print(f"\nYou've won ${temp_bank[current_player]} this round.")
            #(if player != current player, then temp_bank = 0 maybe???) deplete other players temp_bank to zero
            for key in temp_bank.keys():
                temp_bank[key] = 0
            print(f"\nYou've won ${overall_bank[current_player]} total so far.")

            global round_counter
            round_counter += 1
            #solved = False
            break

def buy_vowel(): #cost $250 for one, don't pay for each instance of the vowel
    while True:
        global temp_bank
        if temp_bank[current_player] < vowel_price:
            print("You do not have enough money to buy a vowel.")
            break
        else: 
            guess_vowel = str(input("Buy a vowel: "))
            while True:
                if guess_vowel in guessed_letters:
                    print("That letter has already been guessed.")
                    break
                elif guess_vowel in consonants:
                    print("That's not a vowel.")
                    break
                elif len(guess_vowel) != 1:
                    print("That is not one vowel.")
                    guess_vowel = str(input("Buy a vowel: "))
                    break
                elif guess_vowel.isalpha() == False:
                    print("That is not a letter.")
                    guess_vowel = str(input("Buy a vowel: "))
                    break
                elif guess_vowel not in letters:
                    print("That vowel is not in the word.")
                    #subtract 250 from temp_bank
                    temp_bank[current_player] -= vowel_price
                    print(f"Player {current_player}, your balance is now {temp_bank[current_player]}.")
                    break
                elif guess_vowel in letters:
                    for x in range(0, len(word)):
                        if guess_vowel == word[x] and goal[x] == '_':
                            goal[x] = guess_vowel
                    print(goal)
                    print(f"{guess_vowel} is in the word, great job!")
                    guessed_letters.append(guess_vowel)
                    letters.remove(guess_vowel)

                    #subtract 250 from temp_bank
                    temp_bank[current_player] -= vowel_price
                    print(f"Player {current_player}, your balance is now {temp_bank[current_player]}.")

                    turn_choice()
                    choice = int(input("Choose what to do next: "))
                        
                    while True:
                        if choice == 1:
                            spin_wheel()
                            break
                        elif choice == 2:
                            buy_vowel()
                            break
                        elif choice == 3:
                            solve()
                            break
                        else:
                            print("Please select 1, 2, or 3.")
                            choice = int(input("Choose what to do next: "))
                            break
                break
            break

def list_contains(List1, List2):
    set1 = set(List1)
    set2 = set(List2)

    if set1.intersection(set2):
        return True
    else:
        return False

def spin_wheel():
    landed_on = segments[random.randint(0, len(segments)-1)]
    while True:
        global temp_bank
        if '_' not in goal: #if there aren't any more letters to guess, have to solve
            solve()
            break
        elif '_' in goal and list_contains(letters, vowels) == True and list_contains(letters, consonants) == False: #if there's still letters left, but no more consonants
            print("\nThere are no consonants left, please buy a vowel or attempt to solve the puzzle.")
            print("1. Buy Vowel\n2. Solve Puzzle") #hard code the menu with only buy vowel and solve
            choice = int(input("Choose what to do next: "))
            while True:
                if choice == 1:
                    buy_vowel()
                    break
                elif choice == 2:
                    solve()
                    break
                else:
                    print("Not a valid entry.")
                    break
            break
        elif landed_on == "bankrupt":
            print(f"You've landed on {landed_on}.")
            #decrease temp_bank to zero
            temp_bank.update({current_player:0})
            break
        elif landed_on == "lose_a_turn":
            print(f"You've landed on {landed_on}.")
            break
        else: #land on money
            #add the number to temp_bank when correct
            print(f"You've landed on ${landed_on}.")
            print(f"These letters have been guessed already: {guessed_letters}")
            guess_letter = str(input("Guess a consonant: "))
            while solved == False:
                if guess_letter in guessed_letters: #this one doesn't work?
                    print("That consonant has already been chosen.")
                    break
                elif guess_letter in vowels: #this one also doesn't work?
                    print("That is not a consonant.")
                    break
                elif len(guess_letter) != 1:
                    print("More than one digit entered. Please guess one consonant.")
                    break
                elif guess_letter.isalpha() == False:
                    print("That is not a letter.")
                    break
                elif guess_letter not in letters:
                    print(goal)
                    print(f"{guess_letter} is not in the puzzle.")
                    guessed_letters.append(guess_letter)
                    break
                else:
                    for x in range(0, len(word)): #x is index number, loops through word length
                        if guess_letter == word[x] and goal[x] == '_': #compare if guess is in word and the index place has a _
                            goal[x] = guess_letter #then replace that place in goal with the guess
                    #don't need to have automatic win here, they still have to "solve the puzzle" technically
                    print(goal)
                    print(f"{guess_letter} is in the word, great job!")
                    guessed_letters.append(guess_letter)

                    #add money to the temp bank
                    temp_bank[current_player] += int(landed_on)*letters.count(guess_letter)
                    print(f"Player {current_player}, your balance is now ${temp_bank[current_player]}.")

                    try:
                        while True:
                            letters.remove(guess_letter)
                    except ValueError:
                        pass

                    turn_choice()
                    choice = int(input("Choose what to do next: "))
                    while True:
                        if choice == 1:
                            spin_wheel()
                            break
                        elif choice == 2:
                            buy_vowel()
                            break
                        elif choice == 3:
                            solve()
                            break
                        else:
                            print("Please select 1, 2, or 3.")
                            choice = int(input("Choose what to do next: "))
                            break  
                break 
            break #breaks to change players - DO NOT MOVE/REMOVE

def rstlne():

    for x in range(0, len(word)):
        if "r" == word[x] and goal[x] == '_':
            goal[x] = "r"
    for x in range(0, len(word)):
        if "s" == word[x] and goal[x] == '_':
            goal[x] = "s"
    for x in range(0, len(word)):
        if "t" == word[x] and goal[x] == '_':
            goal[x] = "t"
    for x in range(0, len(word)):
        if "l" == word[x] and goal[x] == '_':
            goal[x] = "l"
    for x in range(0, len(word)):
        if "n" == word[x] and goal[x] == '_':
            goal[x] = "n"
    for x in range(0, len(word)):
        if "e" == word[x] and goal[x] == '_':
            goal[x] = "e"

#game play, rounds 1 & 2============================================================================================

print("\nWelcome to Wheel of Fortune!")

while round_counter < 3:
    
    print(f"\nRound {round_counter}")

    #choose random player
    player_order = [player for player in players]
    current_player = ""
    playerNotChosen = True

    while playerNotChosen == True:
        current_player = random.choice(player_order)
    
        if current_player not in started_already:
            started_already.append(current_player)
            playerNotChosen = False
        else:
            player_order.remove(player_order)


    #choose a random word
    word = random.choice(random_words)
    letters = list(word)
    while True:
        if word in used_words:
            continue
        else:
            used_words.append(word)
            goal = list("_"*len(word))
            break

    solved = False

    guessed_letters = []
    guessed_words = []

    while solved == False:
        if current_player == 1:
            print(f"\nHere is the puzzle:\n{goal}")
            print(f"\nPlayer {current_player}, spin the wheel!")
            spin_wheel()
            current_player = 2
            continue
        elif current_player == 2:
            print(f"\nHere is the puzzle:\n{goal}")
            print(f"\nPlayer {current_player}, spin the wheel!")
            spin_wheel()
            current_player = 3
            continue
        elif current_player == 3:
            print(f"\nHere is the puzzle:\n{goal}")
            print(f"\nPlayer {current_player}, spin the wheel!")
            spin_wheel()
            current_player = 1
            continue

#round 3 ========================================================================================================

while round_counter == 3:
    
    prize_money = 1
    guessed_letters = []
    guesses = 0

    #select player with the highest overall_bank
    value = overall_bank[max(overall_bank, key=overall_bank.get)] #this returns the max value, not key 
    current_player = list(overall_bank.keys())[list(overall_bank.values()).index(value)]

    #choose a random word for round
    word = random.choice(random_words)
    letters = list(word)
    if word in used_words:
        continue
    else:
        used_words.append(word)
    goal = list("_"*len(word))

    rstlne() #puts rstlne in correct indexes in word

    print(f"\nPlayer {current_player}, with a total earnings amount of ${overall_bank[current_player]},\nyou've been selected for the Final Round!")
    print("\nHere is your word:")
    print(goal)
    print("\nGuess 3 consonants and 1 vowel.\nAfterwards, make your guess.")

    while True:
        guess1 = str(input("Guess a consonant: "))
        while True:
            if len(guess1) > 1 or len(guess1) == 0:
                print("Invalid entry, please input a consonant.")
                guess1 = str(input("Guess a consonant: "))
                break
            elif guess1 in RSTLNE:
                print("That letter is already provided.")
                guess1 = str(input("Guess a consonant: "))
                break
            elif guess1 not in consonants:
                print(f"{guess1} is not a consonant.")
                guess1 = str(input("Guess a consonant: "))
                break
            elif guess1 not in letters:
                print(f"{guess1} was not in the puzzle.")
                print(goal)
                break
            elif guess1 in letters:
                for x in range(0,len(word)):
                    if guess1 == word[x] and goal[x] == '_':
                        goal[x] = guess1
                print(f"{guess1} was in the word!")
                print(goal)
                break

        guess2 = str(input("Guess a consonant: "))
        while True:
            if len(guess2) > 1 or len(guess2) == 0:
                print("Invalid entry, please input a consonant.")
                guess2 = str(input("Guess a consonant: "))
                break
            elif guess2 in RSTLNE:
                print("That letter is already provided.")
                guess2 = str(input("Guess a consonant: "))
                break
            elif guess2 not in consonants:
                print(f"{guess2} is not a consonant.")
                guess2 = str(input("Guess a consonant: "))
                break
            elif guess2 not in letters:
                print(f"{guess2} was not in the puzzle.")
                print(goal)
                break
            elif guess2 in letters:
                for x in range(0,len(word)):
                    if guess2 == word[x] and goal[x] == '_':
                        goal[x] = guess2
                print(f"{guess2} was in the word!")
                print(goal)
                break

        guess3 = str(input("Guess a consonant: "))
        while True:
            if len(guess3) > 1 or len(guess3) == 0:
                print("Invalid entry, please input a consonant.")
                guess3 = str(input("Guess a consonant: "))
                break
            elif guess3 in RSTLNE:
                print("That letter is already provided.")
                guess3 = str(input("Guess a consonant: "))
                break
            elif guess3 not in consonants:
                print(f"{guess3} is not a consonant.")
                guess3 = str(input("Guess a consonant: "))
                break
            elif guess3 not in letters:
                print(f"{guess3} was not in the puzzle.")
                print(goal)
                break
            elif guess3 in letters:
                for x in range(0,len(word)):
                    if guess3 == word[x] and goal[x] == '_':
                        goal[x] = guess3
                print(f"{guess3} was in the word!")
                print(goal)
                break

        guess4 = str(input("Guess a vowel: "))
        while True:
            if len(guess4) > 1 or len(guess4) == 0:
                print("Invalid entry, please input a vowel.")
                guess4 = str(input("Guess a vowel: "))
                break
            elif guess4 in RSTLNE:
                print("That letter is already provided.")
                guess4 = str(input("Guess a vowel: "))
                break
            elif guess4 not in vowels:
                print(f"{guess4} is not a consonant.")
                guess4 = str(input("Guess a vowel: "))
                break
            elif guess4 not in letters:
                print(f"{guess4} was not in the puzzle.")
                print(goal)
                break
            elif guess4 in letters:
                for x in range(0,len(word)):
                    if guess4 == word[x] and goal[x] == '_':
                        goal[x] = guess4
                print(goal)
                break

        solve = str(input("Solve the puzzle: "))
        while True:
            if solve == word:
                print(f"Congratulations Player {current_player}, you've won!\nYour prize is: ${prize_money}")
                #add prize money to overall_bank lol
                overall_bank[current_player] += int(prize_money)
                print(f"You'll be taking home ${overall_bank[current_player]} today!")
                break
            else:
                print("Sorry, that wasn't the puzzle.")
                break
        break
    quit()