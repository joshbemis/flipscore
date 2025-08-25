"""
version 0.9
created 2025-08-14
Scores for Flip 7 are running totals
default winning condition is a score of 200
each player that ends the round with cards adds the total of their cards
if a player has 7 value cards in the line, they get a bonus 15 points
set up two modes: basic and guided
basic will take simple inputs from the user and add those inputs to the user's score
guided will allow the user to input the values of each individual card, add those to get the score, then add the score to the total

TODO: 
    D - v0.5 tweak winning condition message to state who won and with what score
    D - v0.6 handle winning ties 
    D - v0.7 added during 0.6 work, will need to reset player order each round to help say dealer
    W - v0.9 error handling
    ---pre-handling any potential errors
    ---validate entries (names should be strings, score should be whole numbers)
    v0.9.5 clean up variable names, formatting and prompt language. Add type hinting support. 
    v1.0 README and release
    v1.1 implement guided mode (probably just an extra function)
    v1.2 implment alternate table view
    
    Possibly migrate this to a better looking version by using textual
    Apprently having a function return two variable types is not great practice, so try to clean that up
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
    """Starts game, provides directions and records the win condition. Will collect game mode later."""
    print("Welcome to the Flip 7 score keeper! \n")
    print("This program has two modes: basic and guided. In basic mode, you will need to add each player's cards at the end of each round and enter the total.")
    print("In guided mode, you will enter each card individually and the program will total them for you.\n")
    # program_mode = input("Enter 1 for basic score keeping mode and 2 for guided: ")
    program_mode = "basic"
    win_score = int(input(f"You chose {program_mode} mode. What score would you like to play to? The default is 200: "))
    print("\n")
    
    # return program mode as well when implemented
    return win_score

def play_round(players, round_number, cur_totals):
    """Pulls the score for each player from input and sends the round scores and totals back as lists"""
    round_scores = [round_number]
    print(f"~~~~~Starting round number {round_number}!~~~~~")
    print(f"{players[0]} deals this round.")
    for player in players:
        round_scores.append(int(input(f"What was {player}'s score? ")))
    
    # updates total for each player
    for score in range(1, len(round_scores)):
        cur_totals[score] += round_scores[score]

    return round_scores, cur_totals # return new player list

def winning_player(players, cur_totals, win_score):
    """Accepts the player list and the current totals and returns the player with highest score"""
    winners = []
    start_value = 1 # since total list contains "Total" as first value we start at the second list value
    
    for total in cur_totals[1:]:
        if total >= win_score:
            winners.append(players[cur_totals.index(total, start_value) - 1])
            start_value += 1

    for winner in winners:
        if winners.index(winner) == 0:
            print(f"The first person to achieve {win_score} points was {winner}. They are our overall winner!")
        else:
            print(f"The next person to achieve {win_score} points was {winner}. Too slow!")

def reset_order(players, score_table):
    """Accepts the player list and scores lists, resets the order after each round to change dealer"""
    # shift first player to last player
    moved = players.pop(0)
    players.append(moved)

    # shift first total to last total to line up with players, start at index 1 to avoid "Total" value
    moved = score_table[-1].pop(1)
    score_table[-1].append(moved)

    # shift each rounds scores so they appear correctly on summary table, start at index -1 to exclude total item
    for round in score_table[:-1]:
        moved = round.pop(1)
        round.append(moved)

    return players, score_table

def reset_header(players):
    """Accepts player list to reset header of results table after shifting dealers"""
    new_header = players.copy()
    new_header.insert(0, "Round")

    return new_header

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
            player_list, table = reset_order(player_list, table)
            header = reset_header(player_list)
            round_number += 1
        else:
            winning_player(player_list, player_totals, win_score)
            break
