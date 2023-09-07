# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import os

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
goals = SHEET.worksheet("goals")
form = SHEET.worksheet("form")
team = SHEET.worksheet("team")


def get_player_list():
    players = appear.row_values(1)
    remove_blank = players.pop(0)

    return players


def get_game_data():
    print("Please enter which game has been played")
    print("Example: 6\n")

    raw_game_data = input("Enter your data here: ")
    game_data = int(raw_game_data) + 1

    return game_data


def get_appearance_data(players, game_data):
    """ """

    print("Please enter which player feature in the last match")
    print("Example: y\n")

    for x in players:
        while True:
            player_appearance = input(f"Did {x} play in the game (y/n):")
            print("Validating data ...")

            if validate_appearance_data(player_appearance):
                print("Data is valid!")
                break
        if player_appearance == "y":
            played = player_appearance.replace("y", "1")
        elif player_appearance == "n":
            played = player_appearance.replace("n", "0")
        print("Adding to the tracker ...")
        appear.update_cell(game_data, int(players.index(x) + 2), int(played))


def validate_appearance_data(player_appearance):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(player_appearance) != 1:
            raise ValueError(
                f"Exactly 1 value required, you provided {len(player_appearance)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def get_goals_data(players, game_data):
    """ """

    print("Please enter which player feature in the last match")
    print("Example: y\n")

    for x in players:
        while True:
            player_goals = input(f"How many goals did {x} score?:")
            print("Validating data ...")

            if validate_goals_data(player_goals):
                print("Data is valid!")
                break

        print("Adding to the tracker ...")
        goals.update_cell(game_data, int(players.index(x) + 2), int(player_goals))


def validate_goals_data(player_goals):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(player_goals) != 1:
            raise ValueError(
                f"Exactly 1 value required, you provided {len(player_goals)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def main():
    players = get_player_list()
    game_data = get_game_data()
    get_appearance_data(players, game_data)
    os.system("cls")
    get_goals_data(players, game_data)


print("Welcome to Everett Rovers Football stats reporting")
print("Input the latest match figures")
main()
