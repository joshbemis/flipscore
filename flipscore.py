"""
/******************************************************************************/
Flip 7 Score Keeper
Created by Josh Bemis
Last Updated: 2025-08-26
v 0.9.5 - code rewrite

This program is meant entirely for individual use and is not intended to be
monitized. I have no affiliation with the Flip 7 card game or its creators. 
/******************************************************************************/
"""

from tabulate import tabulate

class Player:
    """Class for each player that tracks scores"""

    def __init__(self, name, current_score, total_score):
        self.name = name
        self.current_score = current_score
        self.total_score = total_score


def intro():
    """Greets player and collects each name, returns list of players"""
    print(f"Welcome to the Flip 7 score keeper!\n")
    player_number = int(input("How many players will be playing? "))
    player_list = get_player_names(player_number)

    return player_list


def get_player_names(player_number):
    """Runs during intro, returns list of player objects"""
    count = 1
    player_list = []
    
    # create player object for each name and store in player list
    while count <= player_number:
        player_name = str(input(f"---Enter a name for player {count}: "))
        new_player = Player(player_name, 0, 0)
        player_list.append(new_player)
        count += 1

    return player_list

def set_winning_score():
    """Lets user define the score needed to win"""
    winning_score = int(input("\nEnter the score you'd like to set to win " \
                              "(default is 200): "))
    # error handle this for only numerics and provide default if blank use try
    
    print(f"\nAlright, the first to {winning_score} points wins the game!")

    return winning_score

def play_round(player_list, round_number, dealer):
    """Controls a round of play and updates scores afterwards"""
    # make things pretty and note who is dealing in case players forget
    print(f"\n~~~~~~~~~~~~~~~ROUND {round_number}~~~~~~~~~~~~~~~")
    print(f"{dealer} is dealing this round.")

    # set up empty list for current round scores
    current_round = []

    # loop through players and update scores
    for player in player_list:
        player.current_score = int(input(f"---What was {player.name}'s " \
                "score? "))
        player.total_score += player.current_score
        current_round.append(player.current_score)

    # insert round number to current score list, then return it
    current_round.insert(0, round_number)

    return current_round

def check_for_winner(player_list, winning_score):
    """Loops through all players and looks for totals above win condition"""
    win_flag = 0

    for player in player_list:
        if player.total_score >= winning_score:
            win_flag = 1
    
    return win_flag

def shift_dealer(player_list, dealer_index, win_flag):
    """Moves dealer flag to next player in player list"""
    if win_flag == 1:
        pass
    elif dealer_index == (len(player_list) - 1):
        dealer_index = 0
    else:
        dealer_index += 1

    return dealer_index, player_list[dealer_index].name

def print_round(player_list, round_number, round_scores):
    """Prints rolling total table after each round using Tabulate"""
    # set up table header
    header = []
    for player in player_list:
        header.append(player.name)

    header.insert(0, "Round")

    # set up content table, pull in overall totals
    player_totals = []
    for player in player_list:
        player_totals.append(player.total_score)

    # avoid having to copy list
    table = []
    player_totals.insert(0, "Total")
    for round in round_scores:
        table.append(round)
    table.append(player_totals)
    
    # print with tabulate
    print("\n")
    print(tabulate(table, headers=header, tablefmt="grid"))


def end_game(player_list, dealer_index, winning_score):
    """Determines winner and any other players that hit win score"""
    # create empty list to populate with players that won
    winners = []
    
    # start by looking for a winner to the right of dealer
    for player in player_list[(dealer_index + 1):]:
        if player.total_score >= winning_score:
            winners.append(player.name)

    # continue looking for winners to the left of and including dealer
    for player in player_list[:(dealer_index + 1)]:
        if player.total_score >= winning_score:
            winners.append(player.name)

    return winners

def print_results(winners, winning_score, player_list):
    """Prints end game result strings"""
    for player in player_list:
        if player.name == winners[0]:
            final_score = player.total_score
    print(f"\n{winners[0]} was our overall winner with " \
            f"{final_score} points!\n")

    # print all players with required score
    print(f"The players that got {winning_score} points are:")
    count = 1
    for winner in winners:
        for player in player_list:
            if player.name == winner:
                print(f"---{count}. {winner} - {player.total_score} points")
                count += 1

if __name__ == "__main__":
    # define a few starting variables
    round_number = 1
    win_flag = 0
    dealer_index = 0
    round_scores = []

    # game setup
    player_list = intro()
    winning_score = set_winning_score()
    dealer = player_list[dealer_index].name

    # start play
    while win_flag == 0:
        current_round = play_round(player_list, round_number, dealer)
        round_scores.append(current_round)
        print_round(player_list, round_number, round_scores)
        win_flag = check_for_winner(player_list, winning_score)
        round_number += 1
        dealer_index, dealer = shift_dealer(player_list, dealer_index, win_flag)
    
    # win condition has been reached - print winners and results
    winners = end_game(player_list, dealer_index, winning_score)
    print_results(winners, winning_score, player_list)
