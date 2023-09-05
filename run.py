# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("football-statistics-u9y")

appearances = SHEET.worksheet("appearances")
goals = SHEET.worksheet("goals")
form = SHEET.worksheet("form")
team = SHEET.worksheet("team")


def get_game_data():
    print("Please enter which game has been played")
    print("Example: 6\n")

    raw_game_data = input("Enter your data here: ")
    game_data = int(raw_game_data) + 1

    return game_data


def get_player_list():
    players = appearances.row_values(1)
    remove_blank = players.pop(0)

    return players


def get_appearance_data(players):
    """
    MOVE VALIDATION & CELL UPDATE INSIDE FOR LOOP
    """
    while True:
        print("Please enter which player feature in the last match")
        print("Example: y\n")

        appearance_data = []

        for x in players:
            player_appearance = input(f"Did {x} play in the game (y/n):")
            appearance_data.append(player_appearance)

        print(appearance_data)

        if validate_data(appearance_data):
            print("Data is valid!")
            break

    return appearance_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    return True


def update_worksheet(cell, data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.update(cell)
    print(f"{worksheet} worksheet updated successfully\n")


def main():
    players = get_player_list()
    print(players)
    game_data = get_game_data()
    print(game_data)
    appearance_data = get_appearance_data(players)
    appearances.update_cell(game_data, 2, appearance_data)

    # update_worksheet(cell, appearance_data, "appearances")
    # print(appearance_data)


print("Welcome to Everett Rovers Football stats reporting")
print("Input the latest match figures")
main()
