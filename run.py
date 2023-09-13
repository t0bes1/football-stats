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
conceded = SHEET.worksheet("conceded")


def get_player_list():
    """
    Retrieves the list of all team players from the gspread
    This allows the team to be increased or reduced as necessary
    """
    players = appear.row_values(1)
    remove_blank = players.pop(0)

    return players


def get_game_number():
    """
    Returns the number of games that have been played by looking
    This is based on the completed data in the gspread
    """
    game_data = appear.col_values(2)
    games = len(game_data) - 1

    return games


def get_game_data(games):
    """
    Asks user for the game they would like to input data for
    This must be the next game or a previous game (to allow adjustments)
    """
    print(Back.BLUE + "\n GAME INPUT: Please input new game data here")
    print(Style.RESET_ALL)
    print(f"\nNote that the last game data received was for Game {games}")
    print("Please enter which game data you would like to add or adjust")
    print("Example: 6\n")
    print(Style.RESET_ALL)

    while True:
        raw_game_data = input("Enter the Game Number here:\n")
        if validate_game_data(raw_game_data, games):
            print("  Data is valid!")
            break
    game_data = int(raw_game_data) + 1

    return game_data


def validate_game_data(raw_game_data, games):
    """
    Inside the try, checks whether the game number is either the next game
    or a prior game, allowing the user to adjuts prior figures
    Otherwise, an error is returned
    """
    try:
        if int(raw_game_data) > games + 1:
            raise ValueError(Back.RED + f"a game has been missed out")
    except ValueError as e:
        print(Back.RED + f"Invalid data: {e}, please try again.\n")
        print(Style.RESET_ALL)
        return False

    return True


def get_appearance_data(players, game_data):
    """
    Requests the appearance data for players in the game that is being inputted
    Returns a list of the players that played in this match
    """

    print(" Please enter (y or n) which player featured in this match")
    print(" Example: 'y' or 'n'")

    played_game = []

    for x in players:
        while True:
            player_app = input(f"\nDid {x} play in the game (y/n):\n")

            if validate_appearance_data(player_app):
                print("  Data is valid!")
                break
        if player_app == "y":
            played = player_app.replace("y", "1")
            played_game.append(x)
        elif player_app == "n":
            played = player_app.replace("n", "0")
            gls.update_cell(game_data, int(players.index(x) + 2), 0)
        print("  Adding to the tracker ...")
        appear.update_cell(game_data, int(players.index(x) + 2), int(played))

    return played_game


def validate_appearance_data(player_app):
    """
    Inside the try, checks if the user has provided a valid 'y' or 'no'
    Otherwise, an eror is provided
    """
    data_check = "?"
    try:
        if player_app == "y" or player_app == "n":
            data_check = "OK"
        if data_check != "OK":
            raise ValueError(Back.RED + f"Input must be 'y' or 'n'")
    except ValueError as e:
        print(Back.RED + f"\nInvalid data: {e}, please try again.\n")
        print(Style.RESET_ALL)
        return False

    return True


def get_goals_data(players, played_game, game_data):
    """
    For the list of players that featured in the game, the number
    goals scored is requested
    """

    print("Please enter the goals scored by each player in this game")
    print("This must be a number, being 0 if they didn't score")
    print("Example: 1 or 2")

    for x in played_game:
        while True:
            player_gls = input(f"\nHow many goals did {x} score?:\n")

            if validate_goals_data(player_gls):
                print("  Data is valid!")
                break

        print("  Adding to the tracker ...")
        gls.update_cell(game_data, int(players.index(x) + 2), int(player_gls))


def get_conceded_data(game_data):
    """
    Requests the user provides the number of goals conceded in the game
    """

    print("Please enter the goals conceded in the game")
    print("This must be a number, being 0 if they didn't score")
    print("Example: 1 or 2")

    while True:
        conceded_gls = input(f"\nHow many goals did the other team score?:\n")

        if validate_goals_data(conceded_gls):
            print("  Data is valid!")
            break

    print("  Adding to the tracker ...")
    conceded.update_cell(game_data, 2, int(conceded_gls))


def validate_goals_data(data_gls):
    """
    Validates all goal data (scored & conceded)
    Inside the try, attenpts to converts all string values into integers.
    Raises ValueError if a string is passed on, or a number above 9
    """
    try:
        if int(data_gls) > 9:
            raise ValueError(Back.RED + f"This number is too high")
    except ValueError as e:
        print(Back.RED + f"Invalid data: {e}, please try again.\n")
        print(Style.RESET_ALL)
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


def calculate_total_game_gls(games):
    """
    Accesses full goals data from the spreadsheet
    This is manipulated into totals for each game
    """
    all_gls = gls.get_all_values()
    range = games + 1

    all_game_gls = all_gls[1:range]
    aggs = []
    for x in all_game_gls:
        i = x.pop(0)
        aggs.append(x)

    game_gls_list = [[int(string) for string in sublist] for sublist in aggs]
    game_gls = []
    for x in game_gls_list:
        i = sum(x)
        game_gls.append(i)

    return game_gls


def calculate_total_conceded():
    """
    Accesses full conceded data from the spreadsheet
    This is manipulated into totals for each game
    """
    total_conceded_string = conceded.col_values(2)
    remove_name = total_conceded_string.pop(0)

    total_conceded = []

    for i in total_conceded_string:
        q = sum([eval(k) for k in i])
        total_conceded.append(q)

    return total_conceded


def calculate_results(game_gls, total_conceded):
    """
    For MENU1: calculates results data for
    Compares goals scored vs goals conceded
    """
    net_result = []
    for x in game_gls:
        i = x - total_conceded[game_gls.index(x)]
        net_result.append(i)

    win_draw_loss = []
    for x in net_result:
        if x < 0:
            win_draw_loss.append("L")
        elif x > 0:
            win_draw_loss.append("W")
        else:
            win_draw_loss.append("D")

    return win_draw_loss


def games_report_summary(games, game_gls, total_conceded):
    """
    For MENU 1: creates content for games summary report
    """
    win_draw_loss = calculate_results(game_gls, total_conceded)
    wins = win_draw_loss.count("W")
    losses = win_draw_loss.count("L")
    draws = win_draw_loss.count("D")
    os.system("clear")
    print(Back.BLUE + f"\n GAMES REPORT:\n")
    print(f" Everett Rovers U9Y have played {games} games this season")
    print(Style.RESET_ALL)
    print(Fore.GREEN + f" We have won {wins} games")
    print(Fore.YELLOW + f" We have drawn {draws} games")
    print(Fore.RED + f" We have lost {losses} games")
    print(Style.RESET_ALL)
    print(" Whatever the results, it has been a fun season!")


def games_report_full(game_gls, total_conceded):
    """
    For MENU 2: creates content for games run down report
    """
    gls_string = []
    for x in game_gls:
        i = " Game " + str(game_gls.index(x) + 1) + ": " + str(x) + " - "
        gls_string.append(i)

    full_res = [str(a) + str(b) for a, b in zip(gls_string, total_conceded)]
    os.system("clear")
    print(Back.BLUE + f"\n FULL RESULTS REPORT:\n")
    print(Style.RESET_ALL)
    print(Fore.GREEN + f" Everett Rovers v Opponents")
    print(Style.RESET_ALL)
    [print(x) for x in full_res]


def goals_report(games, total_gls, total_conceded):
    """
    For MENU 3: creates content for goals summary report
    """
    all_gls = sum(total_gls)
    all_conceded_gls = sum(total_conceded)
    av_gls = int(all_gls / games)
    gl_dif = all_gls - all_conceded_gls
    os.system("clear")
    print(Back.BLUE + f"\n GOALS REPORT:\n")
    print(Style.RESET_ALL)
    print(Fore.GREEN + f" The team has scored {all_gls} goals this season")
    print(Style.RESET_ALL)
    print(f" We have done this in {games} games")
    print(f" This is roughly {av_gls} goals per game; great scoring!")
    print(Fore.RED + f"\n We have conceded {all_conceded_gls} goals")
    print(Fore.YELLOW + f"\n Our goal difference is {gl_dif} goals!")
    print(Style.RESET_ALL)


def top_scorer_report(players, total_gls):
    """
    For MENU 4: creates content for top scorer report
    """
    os.system("clear")
    print(Back.BLUE + f"\n TOP SCORER REPORT:\n")
    top_scorer = total_gls.index(max(total_gls))
    print(Back.GREEN + f" The top scorer is {players[top_scorer]}")
    print(f"\n He has scored {max(total_gls)} this season")
    print(Style.RESET_ALL)
    print(f" But well done to all players!")


def calculate_form(total_gls, total_appear, players):
    """
    For MENU 5: creates content for form report
    uses goals/appearance data to calcuate a player "form" metric
    The highest value is returned, representing the best current player
    """
    form = [a / b for a, b in zip(total_gls, total_appear)]
    ranking1 = form.index(max(form))
    no1_rank = players[ranking1]
    ranking7 = form.index(min(form))
    no7_rank = players[ranking7]
    os.system("clear")
    print(Back.BLUE + f"\n FORM REPORT:\n")
    print(Back.GREEN + f" The top ranked player is {no1_rank}")
    print("\n Please select him as captain for the next match!\n")
    print(Back.RED + f" The low ranked player is {no1_rank}")
    print("\n Please consider him for substitute for the next match")
    print(Style.RESET_ALL)


def run_data_input(games, players):
    """
    For MENU 6: runs all get_data functions for inputted new game
    Produces content to walk through process step by step
    """
    os.system("clear")
    game_data = get_game_data(games)
    print(Back.BLUE + "\n Thanks, Game confirmed")
    print(Style.RESET_ALL)
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n APPEARANCE INPUT: for Game {game_data - 1}")
    print(Style.RESET_ALL)
    played_game = get_appearance_data(players, game_data)
    print(Back.BLUE + "\n Thanks, new appearance data has been received")
    print(Style.RESET_ALL)
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n GOALS INPUT: for Game {game_data - 1}")
    print(Style.RESET_ALL)
    get_goals_data(players, played_game, game_data)
    print(Back.BLUE + "\n Thanks, the new goal data has been received")
    print(Style.RESET_ALL)
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n GOALS AGAINST INPUT: for Game {game_data - 1}")
    print(Style.RESET_ALL)
    get_conceded_data(game_data)
    print(Back.BLUE + "\n Thanks, the new conceded data has been received")
    print(Style.RESET_ALL)
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + "\n WELCOME BACK. New results have been calculated.")
    print(Style.RESET_ALL)


def menu(games, players, total_app, total_gls, game_gls, total_conceded):
    """
    Main MENU: used by user to navigate the program
    """
    options = [
        "[1] Games Report : Performance Summary",
        "[2] Games Report : Full Results",
        "[3] Goals Report : Overall Performance",
        "[4] Who has scored the most goals this season?",
        "[5] Which player is in the best form?",
        "[6] INPUT latest game figures",
        "[7] Quit",
    ]
    terminal_menu = TerminalMenu(options, title="\n MENU: Please select:")
    menu_entry_index = terminal_menu.show()
    print(f"\n You have selected: {options[menu_entry_index]}")

    if menu_entry_index == 0:
        games_report_summary(games, game_gls, total_conceded)
        main()

    elif menu_entry_index == 1:
        games_report_full(game_gls, total_conceded)
        main()

    elif menu_entry_index == 2:
        goals_report(games, total_gls, total_conceded)
        main()

    elif menu_entry_index == 3:
        top_scorer_report(players, total_gls)
        main()

    elif menu_entry_index == 4:
        calculate_form(total_gls, total_app, players)
        main()

    elif menu_entry_index == 5:
        run_data_input(games, players)
        main()

    elif menu_entry_index == 6:
        os.system("clear")
        quit()


def main():
    """
    Main program begin/restart
    All base data is recalcuated to ensure up to date information provided
    """
    players = get_player_list()
    games = get_game_number()
    total_app = calculate_total_app(players, games)
    total_gls = calculate_total_gls(players, games)
    game_gls = calculate_total_game_gls(games)
    total_conceded = calculate_total_conceded()
    menu(games, players, total_app, total_gls, game_gls, total_conceded)


os.system("clear")
print("\n")
print(Back.BLUE + " Welcome to Everett Rovers Football team reporting")
print(Style.RESET_ALL)
print(" There are various reports available to review our statistics")
print(" You can review games, goals, top scorer & form information")
print(Style.DIM)
print(" [Note: you may also input new figures to ensure full game stats]")
print(Style.RESET_ALL)
main()
