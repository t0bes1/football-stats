from colorama import Fore, Back, Style


def validate_game_data(raw_game_data, games):
    """
    Inside the try, checks whether the game number is either the next game
    or a prior game, allowing the user to adjust prior figures
    Otherwise, an error is returned
    """
    try:
        if int(raw_game_data) > games + 1:
            raise ValueError(Back.RED + f"a game has been missed out")
        elif int(raw_game_data) < 1:
            raise ValueError(Back.RED + f"game number must be more than 0")
    except ValueError as e:
        print(
            Back.RED
            + f"""\nInvalid data: {e},
            please try again.\n{Style.RESET_ALL}"""
        )
        return False

    return True


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
        print(
            Back.RED
            + f"""\nInvalid data: {e},
            please try again.\n{Style.RESET_ALL}"""
        )
        return False

    return True


def validate_goals_data(data_gls):
    """
    Validates all goal data (scored & conceded)
    Inside the try, attenpts to converts all string values into integers.
    Raises ValueError if a string is passed on, or a number above 9
    """
    try:
        if int(data_gls) > 5:
            print(
                Back.YELLOW
                + f"""This number "{data_gls}" is possible but very high,
                please re-enter figures later if an error has been made"""
            )
            return True
        elif int(data_gls) < 0:
            raise ValueError(Back.RED + f"Goals must be a positive number")
    except ValueError as e:
        print(
            Back.RED
            + f"""\nInvalid data: {e},
            please try again.\n{Style.RESET_ALL}"""
        )
        return False

    return True
