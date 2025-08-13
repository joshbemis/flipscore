"""
version 0.1 
created 2025-08-13
Scores for Flip 7 are running totals
default winning condition is a score of 200
each player that ends the round with cards adds the total of their cards
if a player has 7 value cards in the line, they get a bonus 15 points
set up two modes: basic and guided
basic will take simple inputs from the user and add those inputs to the user's score
guided will allow the user to input the values of each individual card, add those to get the score, then add the score to the total

maybe allow two differnet table displays: by round and just total by player
TODO: 
    v 0.5 tweak winning condition message to state who won and with what score
    v 0.6 handle winning ties (if wanted. instructions say first player to 200, so home rule if not)
    v 0.9 error handling
    v 1.0 clean up and README
    v 1.1 implement guided mode (probably just an extra function)
"""

from tabulate import tabulate

def get_player_list():
    """ Prompts user to enter all player names, then returns them as a list """
    player_list = []
    print("In the following prompts, enter each player's name one at a time. When all players are entered, type done.")

    while True:
        player_name = input("Enter player name: ")
        if player_name.lower() == "done":
            break
        else:
            player_list.append(player_name)
    print("\n")
          
    return player_list

def intro():
    print("Welcome to the Flip 7 score keeper! \n")
    print("This program has two modes: basic and guided. In basic mode, you will need to add each player's cards at the end of each round and enter the total.")
    print("In guided mode, you will enter each card individually and the program will total them for you.\n")
    # program_mode = input("Enter 1 for basic score keeping mode and 2 for guided: ")
    win_score = int(input(f"You chose basic mode. What score would you like to play to? The default is 200: "))
    print("\n")
    
    return win_score
    # return program_mode and win score

def play_round(players, round_number, cur_totals):
    """Pulls the score for each player from input and sends the round scores and totals back as lists"""
    round_scores = [round_number]
    print(f"~~~~~Starting round number {round_number}!~~~~~")
    for player in players:
        round_scores.append(int(input(f"What was {player}'s score? ")))
    
    # updates total for each player
    for score in range(1, len(round_scores)):
        cur_totals[score] += round_scores[score]

    return round_scores, cur_totals

if __name__ == "__main__":
    # say hello to the player, give instructions and get the list of players
    win_score = intro()
    player_list = get_player_list()
    
    # set up for round loop
    round_number = 1
    player_totals = [0] * (len(player_list) + 1)
    player_totals[0] = "Total"
    
    # set up for tabulate table
    header = player_list.copy()
    header.insert(0, "Round")
    table = [player_totals]

    while True:
        if max(player_totals[1:]) < win_score:
            cur_round, player_totals = play_round(player_list, round_number, player_totals)
            table.insert(-1, cur_round)
            print(tabulate(table, headers=header, tablefmt="outline"))
            print("\n")
            round_number += 1
        else:
            print("Winning score!")
            break
