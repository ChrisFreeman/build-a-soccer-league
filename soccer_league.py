#!/usr/bin/python3
"""Build a Soccer League - Treehouse Techdegree - Python Web Development

Partition player data from CSV file, into three teams, generate letters
to players guardians. See 'instructions.org' for grading rubric.
"""

import csv


DATAFILE = "soccer_players.csv"

# practice times are as follows:
# Dragons - March 17, 1pm, Sharks - March 17, 3pm, Raptors - March 18, 1pm

PRACTICE_TIME = {
    'Dragons': "March 17, 2016 @ 1:00PM",
    'Sharks': "March 17, 2016 @ 3:00PM",
    'Raptors': "March 18, 2016 @ 1:00PM",
}

TEAM_NAMES = ['Dragons', 'Sharks', 'Raptors']

"""create a team object with such as
{'name': "", 'avg_height': 0, players=[]}

teams = [team1, team2 ,team3]

sort teams by avg_height (biggest first)
add one player to each team from lowest-first sorted players
resort teams
"""


def get_players_from_file(filename=DATAFILE):
    """Read a CSV datafile, convert player data to dict
    and return list of player dicts
    """
    with open(filename, newline='') as csvfile:
        player_reader = csv.DictReader(csvfile)
        players = list(player_reader)
        return players


def gen_team(name):
    """Generate a dict to represent a soccor team
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


def gen_player_letters(team):
    """Generate letter to each team player

    Create logic that iterates through all three teams of players
    generates a personalized letter to the guardians, letting them
    know:
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
            file.write("\n\nWe look foward to another great year!"
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


def main():
    """Organize a soccer league from player data in CSV file.
    Generate three balanced teams with respect to player experience and height.
    Generate personalized letters to each players's Guardians.

    Sorting
    """
    # generate base team containers
    teams = []
    for name in TEAM_NAMES:
        teams.append(gen_team(name))

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

    # Sort experienced players
    while exp_players:
        # sort teams by avg_height (largest first)
        teams.sort(key=lambda team: team['avg_height'])  # , reverse=True)
        # add player to each team
        for team in teams:
            # add the next player (shortest first)
            team['players'].append(exp_players.pop(0))
            # recalculate average height
            team['avg_height'] = get_team_avg_height(team)

    # Sort non-experienced players
    while new_players:
        # sort teams by avg_height (largest first)
        teams.sort(key=lambda team: team['avg_height'])  # , reverse=True)
        # add player to each team
        for team in teams:
            # add the next player (shortest first)
            team['players'].append(new_players.pop(0))
            # recalculate average height
            team['avg_height'] = get_team_avg_height(team)

    # output team rosters and player letters
    for team in teams:
        gen_team_roster(team)
        gen_player_letters(team)


if __name__ == '__main__':
    main()
