import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style
from validation import *

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("football-statistics-u9y")

app = SHEET.worksheet("appearances")
gls = SHEET.worksheet("goals")
conceded = SHEET.worksheet("conceded")
R = Style.RESET_ALL
FR = Fore.RED
FY = Fore.YELLOW
FG = Fore.GREEN


def get_player_list():
    """
    Retrieves the list of all team players from the gspread
    This allows the team to be increased or reduced as necessary
    """
    players = app.row_values(1)
    remove_blank = players.pop(0)

    return players


def get_game_number():
    """
    Returns the number of games that have been played
    This is based on the completed data in the gspread
    """
    game_data = app.col_values(2)
    games = len(game_data) - 1

    return games


def get_game_data(games):
    """
    Asks user for the game they would like to input data for
    This must be the next game or a previous game (to allow adjustments)
    """
    print(
        Back.BLUE
        + f"""\n GAME INPUT: ADD OR EDIT game data here {R}
    \nYou may add a new game or adjust the figures from previous games
    ------------------------------------------------------------
    \nNote that the last game data received was for Game {games}
    \nIf you'd like to {FY}enter the next game{R}, please input {games + 1}
    \nIf you'd like to {FR}adjust a previous game{R}, please input 1-{games}\n
    ------------------------------------------------------------"""
    )

    while True:
        raw_game_data = input("\nEnter the Game Number here:\n")
        if validate_game_data(raw_game_data, games):
            print("  Data is valid!")
            break
    game_data = int(raw_game_data) + 1

    return game_data


def get_appearance_data(players, game_data):
    """
    Requests the appearance data for players in the game that is being inputted
    Returns a list of the players that played in this match
    """

    print(
        """\n Please enter (y or n) for which player featured in this match
        \n Example: 'y' or 'n'\n"""
    )

    played_game = []
    for player in players:
        while True:
            player_app = input(f" Did {FY}{player}{R} play the match?(y/n):\n")
            if validate_appearance_data(player_app):
                print("\n  Data is valid!")
                break
        if player_app == "y":
            played = player_app.replace("y", "1")
            played_game.append(player)
        elif player_app == "n":
            played = player_app.replace("n", "0")
            gls.update_cell(game_data, int(players.index(player) + 2), 0)
        print("  Adding to the tracker ...\n")
        app.update_cell(game_data, int(players.index(player) + 2), int(played))

    return played_game


def get_goals_data(players, played_game, game_data):
    """
    For the list of players that featured in the game, the number
    goals scored is requested
    """

    print(
        f"""\nPlease enter the {FG}goals scored by each player{R} in this game
    \nThis must be a number, being 0 if they didn't score
    \nExample: 1 or 2"""
    )

    for played in played_game:
        while True:
            pl_gls = input(f"\nHow many goals did {FY}{played}{R} score?:\n")

            if validate_goals_data(pl_gls):
                print("  Data is valid!")
                break

        print("  Adding to the tracker ...")
        gls.update_cell(game_data, int(players.index(played) + 2), int(pl_gls))


def get_conceded_data(game_data):
    """Requests the user provides the number of goals conceded in the game"""

    print(
        f"""\n Please enter the {FR}goals conceded{R} in the game
        ----------------------------------------------------------
    \n This must be a number, being 0 if they didn't score
    \n Example: 1 or 2
        ---------------------------------------------------------"""
    )

    while True:
        conceded_gls = input(f"\n How many goals did the other team score?:\n")

        if validate_goals_data(conceded_gls):
            print("  Data is valid!")
            break

    print("  Adding to the tracker ...")
    conceded.update_cell(game_data, 2, int(conceded_gls))


def calculate_total_app(players, games):
    """
    Accesses full appearance data from the spreadsheet
    This is manipulated into totals for each player
    """
    all_data = app.get_all_values()
    remove_names = all_data.pop(0)
    refined_data = refine_data(all_data, players, games)
    total_app = refined_data

    return total_app


def calculate_total_gls(players, games):
    """
    Accesses full goals data from the spreadsheet
    This is manipulated into totals for each player
    """
    all_data = gls.get_all_values()
    remove_names = all_data.pop(0)
    refined_data = refine_data(all_data, players, games)
    total_gls = refined_data

    return total_gls


def refine_data(all_data, players, games):
    """
    Converts raw data from the gspread into total formats
    These totals are for each player
    """
    # Converts list of list (rows) into a list of list (columns)
    new_all_data_array = []
    colnum = len(players) + 1
    for index in range(1, colnum):
        all_data_list = []
        for list in all_data:
            new_list = list[index]
            all_data_list.append(new_list)

        new_all_data_array.append(all_data_list)

    # Removes excess data for games that have not been played
    sliced_data_array = []
    for list in new_all_data_array:
        sliced_list = list[0:games]
        sliced_data_array.append(sliced_list)

    # Converts list of list (strings) to list of totals (integers)
    refined_data = []
    for list in sliced_data_array:
        integer_list = sum([eval(string) for string in list])
        refined_data.append(integer_list)

    return refined_data


def calculate_total_game_gls(games):
    """
    Accesses full goals data from the spreadsheet
    This is manipulated into totals for each game
    """
    all_gls = gls.get_all_values()
    range = games + 1

    # Removes data from games that haven't been played
    all_game_gls_raw = all_gls[1:range]

    # Removes "Game" headings from each row
    all_game_gls = []
    for row in all_game_gls_raw:
        new_row = row.pop(0)
        all_game_gls.append(row)

    # Converts goal strings to goal integers, then totals,
    # This creates the final list of goal totals
    game_gls_list = [[int(str) for str in sublist] for sublist in all_game_gls]
    game_gls = []
    for list in game_gls_list:
        total_list = sum(list)
        game_gls.append(total_list)

    return game_gls


def calculate_total_conceded():
    """
    Accesses full conceded data from the spreadsheet
    This is manipulated into totals for each game
    """
    total_vs_str = conceded.col_values(2)
    remove_name = total_vs_str.pop(0)

    # the string of goals conceded is converted to integers
    total_vs = []
    for gl_str in total_vs_str:
        gls_int = sum([eval(gl_int) for gl_int in gl_str])
        total_vs.append(gls_int)

    return total_vs


def calculate_results(game_gls, total_vs):
    """
    For MENU1: calculates results data for each game
    Compares goals scored vs goals conceded
    """
    # goals scored less goals conceded, gives a net goal difference (number)
    net_result = [score - vs for score, vs in zip(game_gls, total_vs)]

    # goal difference number is converted into a result (W/D/L)
    win_draw_loss = []
    for net_gls in net_result:
        if net_gls < 0:
            win_draw_loss.append("L")
        elif net_gls > 0:
            win_draw_loss.append("W")
        else:
            win_draw_loss.append("D")

    return win_draw_loss


def calculate_full_results(games, game_gls, total_vs):
    """For MENU2: calculates full result history for each game"""
    # accesses a list of Game names from the gspread
    full_game_list = gls.col_values(1)
    range = games + 1
    game_list = full_game_list[1:range]

    # a list with goals scored in each match, & converts into a useful string
    total_for = []
    for gls in game_gls:
        game_res = ":   |   " + str(gls) + "    -   "
        total_for.append(game_res)

    # returns a full game list by combining game name, scored & conceded goals
    full_res = [
        str(game) + str(score) + str(concede)
        for game, score, concede in zip(
            game_list,
            total_for,
            total_vs,
        )
    ]

    return full_res


def calculate_form_ranking(players, total_gls, total_app):
    """FOR MENU5: uses goals/appearance data to calcuate a player "form" metric
    The highest value is returned, representing the best current player"""
    form = [gls / app for gls, app in zip(total_gls, total_app)]
    ranking1 = form.index(max(form))
    no1_rank = players[ranking1]
    ranking7 = form.index(min(form))
    no7_rank = players[ranking7]

    return no1_rank, no7_rank
