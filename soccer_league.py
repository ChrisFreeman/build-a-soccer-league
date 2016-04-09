#!/usr/bin/python3
"""Build a Soccer League - Treehouse Techdegree - Python Web Development

Partition player data from CSV file, into three teams, generate letters
to players guardians. See 'instructions.org' for grading rubric.

Each team is represented by a dict created by 'gen_team(name)'
    team = {'name': "", 'avg_height': 0, players=[]}
where,
   'name':  holds the name of the team,
   'avg_height':  is the average team height from the current players, and
   'players' is a list of dicts, where each player dict contains the
       information from CSV file

The Entire League is represented by a list of team dicts:
    entire_league = [team1, team2 ,team3]

The sorting algorithm works as follows:
    0. players are separated into two lists for experienced and new
    1. each player list is sorted by player height (tallest first)
    2. Loop:
        A. sort entire_league by avg team height (shortest first)
        B. Starting with tallest player, add one player to each team
        C. calculate new avg_height for each team
    3. The experienced players are added first, then the new players.

Algorithm research:
    1. Wikipedia Partition Problem Greedy Algorithm
        https://en.wikipedia.org/wiki/Partition_problem#The_greedy_algorithm
    2. Multi-Way Number Partitioning, Richard E. Korf
        http://ijcai.org/Proceedings/09/Papers/096.pdf
        Twenty-first IJCAI Proceeding 2009
        International Joint Conferences on Artificial Intelligence Organization

Program Output:
    1. 18 letters, one to each player's guardian(s), saved in a file named
        "player_<player_name>.txt"
    2. Bonus output: 3 team files, one for each team, summarizing the team
        information: Team name, practice time, average team height, player
        roster. Saved into a file named "<team_name>_roster.txt"
"""

import csv

__author__ = "Chris Freeman"
__copyright__ = "Copyright 2016, Chris Freeman"
__license__ = "MIT"


DATAFILE = "soccer_players.csv"

# practice times are as follows:
# Dragons - March 17, 1pm, Sharks - March 17, 3pm, Raptors - March 18, 1pm

PRACTICE_TIME = {
    'Dragons': "March 17, 2016 @ 1:00PM",
    'Sharks': "March 17, 2016 @ 3:00PM",
    'Raptors': "March 18, 2016 @ 1:00PM",
}

TEAM_NAMES = ['Dragons', 'Sharks', 'Raptors']


def get_players_from_file(filename=DATAFILE):
    """Read a CSV datafile, convert player data to dict
    and return list of player dicts
    """
    with open(filename, newline='') as csvfile:
        player_reader = csv.DictReader(csvfile)
        players = list(player_reader)
        return players


def gen_team(name):
    """Generate a dict to represent a soccer team
    """
    return {'name': name, 'avg_height': 0, 'players': []}


def get_team_avg_height(team):
    """calculate a new avg_height based on current team's player's heights.
    If no players on team, return 0
    """
    num_players = len(team['players'])
    if num_players == 0:
        # No players return 0
        return 0
    # calculate average height of existing players
    total_height = 0
    for player in team['players']:
        total_height += int(player['Height (inches)'])
    return total_height / num_players


def partition_players(players, league):
    """Partition players into teams by assigning the tallest player
    to the team with the lowest average height. 'players' list is
    assumed to be reverse sorted by height (tallest first)
    """
    # Partition experienced players into teams
    while players:
        # sort teams by avg_height (smallest first)
        league.sort(key=lambda team: team['avg_height'])
        # add player to each team
        for team in league:
            # add the next player (tallest first)
            team['players'].append(players.pop(0))
            # recalculate average height
            team['avg_height'] = get_team_avg_height(team)


def gen_player_letters(team):
    """Generate letter to each team player

    Generate a personalized letter to the guardians of each player
    on the team, letting them know:
        which team the child has been placed on, and
        when they should attend their first team team practice.
    Provide the necessary information
        player name,
        guardians’ names,
        practice date/time
    """
    for player in team['players']:
        # split on space
        player_name = player['Name'].split()
        # gen file name from player name (rejoin with '_')
        filename = "player_" + "_".join(player_name).lower() + ".txt"
        with open(filename, 'w') as file:
            # write header
            file.write("\n\n\t\t\tSoccer League -- Team {}\n\n"
                       "".format(team['name']))
            # salutation
            file.write("Dear {},\n\n".format(player['Guardian Name(s)']))
            # body
            file.write("We would like to welcome you and {} to the Soccer "
                       "League.\n".format(player['Name']))
            file.write("This year, {} will be playing on Team {}.\nThe first "
                       "".format(player_name[0], team['name']))
            file.write("practice will be on {} at Treehouse Stadium.\n"
                       "".format(PRACTICE_TIME[team['name']]))
            # closing
            file.write("\n\nWe look forward to another great year!"
                       "\n\nRegards, Coach Kicks.\n")


def gen_team_roster(team):
    """Bonus function: generate team rosters and save to file.
    """
    filename = team['name'].lower() + "_roster.txt"
    with open(filename, 'w') as file:
        # write header
        file.write("\n\n\t\t\tSoccer League -- Team {} Roster\n\n"
                   "".format(team['name']))
        # write practice time
        file.write("\tFirst Practice:\t{}\n\n"
                   "".format(PRACTICE_TIME[team['name']]))
        # write stats
        file.write("\tStats:\t\tNumber of players: {}, "
                   "Average Height (inches): {:0.2f}\n\n"
                   "".format(len(team['players']), team['avg_height']))
        # write roster of players
        file.write("\tPlayers:\n")
        for player in team['players']:
            file.write("\t\tName: {}\n".format(player['Name']))
            file.write("\t\t\tExperienced: {}, Height: {}, Guardian(s): {}\n"
                       "".format(player['Soccer Experience'],
                                 player['Height (inches)'],
                                 player['Guardian Name(s)']))


def output_stats(league):
    """Print to STDOUT team average heights stats
    """
    for team in league:
        print("Team {}: Avg Height {}".format(
            team['name'], team['avg_height']))


def main():
    """Organize a soccer league from player data in CSV file.
    Generate three balanced teams with respect to player experience and height.
    Generate personalized letters to each player's Guardians.
    """
    # generate base team containers
    entire_league = []
    for name in TEAM_NAMES:
        entire_league.append(gen_team(name))

    # get players
    players = get_players_from_file()

    # separate experienced and new players
    exp_players = []
    new_players = []
    for player in players:
        if player['Soccer Experience'] == 'YES':
            exp_players.append(player)
        else:
            new_players.append(player)
    # sort players by height
    exp_players.sort(key=lambda player: player['Height (inches)'],
                     reverse=True)
    new_players.sort(key=lambda player: player['Height (inches)'],
                     reverse=True)

    # algorithm summary: tallest available player
    # placed on team with shortest average height

    # Partition experienced players into teams
    partition_players(exp_players, entire_league)

    # Partition non-experienced players into teams
    partition_players(new_players, entire_league)

    # output team rosters and player letters
    for team in entire_league:
        gen_player_letters(team)
        gen_team_roster(team)

    # print to STDOUT average height stats
    output_stats(entire_league)

if __name__ == '__main__':
    main()
