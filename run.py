import os
import time
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style
from simple_term_menu import TerminalMenu


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("football-statistics-u9y")

appear = SHEET.worksheet("appearances")
gls = SHEET.worksheet("goals")
form = SHEET.worksheet("form")
team = SHEET.worksheet("team")


def get_player_list():
    players = appear.row_values(1)
    remove_blank = players.pop(0)

    return players


def get_game_number():
    game_data = appear.col_values(2)
    games = len(game_data) - 1

    return games


def top_scorer_calculation(players, total_gls):
    player_gls = zip(players, total_gls)
    print(type(player_gls))
    top_scorers = sorted(list(player_gls), key=lambda x: x[1])
    print(f"\n The top scorer is {top_scorers[-1]}")
    main()


def get_game_data(games):
    print(Back.BLUE + "\nGAME INPUT: Please input new game data here")
    print(Style.RESET_ALL)
    print(f"\nNote that the last game inputted was Game {games}")
    print("Please enter which game has been played")
    print("Example: 6\n")
    print(Style.RESET_ALL)

    raw_game_data = input("Enter the Game Number here: ")
    game_data = int(raw_game_data) + 1

    return game_data


def get_appearance_data(players, game_data):
    """ """

    print("Please enter which player featured in the last match")
    print("Example: 'y' or 'n'")

    for x in players:
        while True:
            player_app = input(f"\nDid {x} play in the game (y/n):")

            if validate_appearance_data(player_app):
                print("  Data is valid!")
                break
        if player_app == "y":
            played = player_app.replace("y", "1")
        elif player_app == "n":
            played = player_app.replace("n", "0")
        print("  Adding to the tracker ...")
        appear.update_cell(game_data, int(players.index(x) + 2), int(played))


def validate_appearance_data(player_app):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(player_app) != 1:
            raise ValueError(
                Fore.RED + f"Exactly 1 value required, you provided {len(player_app)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def get_goals_data(players, game_data):
    """
    The
    """

    print("\nPlease enter the goals scored by the player in this match")
    print("This should be a number and could be 0")
    print("Example: 1 or 2\n")

    for x in players:
        while True:
            player_gls = input(f"How many goals did {x} score?:")

            if validate_goals_data(player_gls):
                print("  Data is valid!")
                break

        print("  Adding to the tracker ...")
        gls.update_cell(game_data, int(players.index(x) + 2), int(player_gls))


def validate_goals_data(player_gls):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(player_gls) != 1:
            raise ValueError(
                f"Exactly 1 value required, you provided {len(player_gls)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def calculate_total_app(players, games):
    """
    Accesses full appearance data from the spreadsheet
    This is manipulated into totals for each player
    """
    all_app = appear.get_all_values()
    remove_names = all_app.pop(0)

    all_app_array = []
    colnum = len(players) + 1

    for z in range(1, colnum):
        all_app_list = []
        for x in all_app:
            i = x[z]
            all_app_list.append(i)

        all_app_array.append(all_app_list)

    total_app_string = []

    for i in all_app_array:
        j = i[0:games]
        total_app_string.append(j)

    total_app = []

    for i in total_app_string:
        q = sum([eval(k) for k in i])
        total_app.append(q)

    return total_app


def calculate_total_gls(players, games):
    """
    Accesses full goals data from the spreadsheet
    This is manipulated into totals for each player
    """
    all_gls = gls.get_all_values()
    remove_names = all_gls.pop(0)

    all_gls_array = []
    colnum = len(players) + 1

    for z in range(1, colnum):
        all_gls_list = []
        for x in all_gls:
            i = x[z]
            all_gls_list.append(i)

        all_gls_array.append(all_gls_list)

    total_gls_string = []

    for i in all_gls_array:
        j = i[0:games]
        total_gls_string.append(j)

    total_gls = []

    for i in total_gls_string:
        q = sum([eval(k) for k in i])
        total_gls.append(q)

    return total_gls


def calculate_form(total_goals, total_appear, players):
    """
    Uses goals and appearance data to calcuate a "form" metric for each player
    The highest value is returned, representing the best current player
    """

    form = [a / b for a, b in zip(total_goals, total_appear)]

    ranking1 = form.index(max(form))

    no1_rank = players[ranking1]

    return no1_rank


def menu(games, players, total_app, total_gls):
    options = [
        "[1] How many games have we played this season?",
        "[2] Goals Report : Totals",
        "[3] Who has scored the most goals this season?",
        "[4] Which player is in the best form?",
        "[5] Input latest game figures",
        "[6] Quit",
    ]
    terminal_menu = TerminalMenu(options, title="\nMENU: Please select:")
    menu_entry_index = terminal_menu.show()
    print(f"\nYou have selected: {options[menu_entry_index]}")

    if menu_entry_index == 0:
        print(f"\nWe have data for {games} games so far this season")
        main()

    elif menu_entry_index == 1:
        all_gls = sum(total_gls)
        av_gls = all_gls / games
        print(f"\nWe have scored {all_gls} goals so far this season")
        print(f"\nWe have done this in {games} games")
        print(f"\nThis is {av_gls} goals per game")
        main()

    elif menu_entry_index == 2:
        top_scorer_calculation(players, total_gls)
        print("\nOption 3")

    elif menu_entry_index == 3:
        no1_rank = calculate_form(total_gls, total_app, players)
        print("Thank you for inputting the latest match scores.")
        print(f"The top ranked player is {no1_rank}")
        print("Please select him for the next match")

    elif menu_entry_index == 4:
        game_data = get_game_data(games)
        get_appearance_data(players, game_data)
        print(Back.BLUE + "Thanks, the new appearance data has been received")
        print(Style.RESET_ALL)
        time.sleep(2)
        os.system("clear")
        print(Back.BLUE + "\nGAME INPUT: Please input new game data here")
        get_goals_data(players, game_data)
        print(Back.BLUE + "Thanks, the new goal data has been received")
        print(Style.RESET_ALL)
        time.sleep(2)
        os.system("clear")
        main()

    elif menu_entry_index == 5:
        os.system("clear")
        quit()


def main():
    players = get_player_list()
    games = get_game_number()
    total_app = calculate_total_app(players, games)
    total_gls = calculate_total_gls(players, games)
    print(games)
    print(players)
    print(total_app)
    print(total_gls)
    menu(games, players, total_app, total_gls)


print("\n")
print(Back.BLUE + "Welcome to Everett Rovers Football stats reporting")
print(Style.RESET_ALL)
print("This program helps you review team performance")
print("You can also input the latest match figures to view up to date stats")
print(Style.RESET_ALL)
main()
