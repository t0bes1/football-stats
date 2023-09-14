import os
import time
from colorama import Fore, Back, Style
from simple_term_menu import TerminalMenu
from get_data import *


def games_report_summary(games, game_gls, total_vs):
    """
    For MENU 1: creates content for games summary report
    """
    win_draw_loss = calculate_results(game_gls, total_vs)
    wins = win_draw_loss.count("W")
    losses = win_draw_loss.count("L")
    draws = win_draw_loss.count("D")
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n GAMES SUMMARY REPORT:\n{Style.RESET_ALL}
    \nEverett Rovers U9Y has played {games} games this season {Style.RESET_ALL}
    {Fore.GREEN} \nWe have won {wins} games
    {Fore.YELLOW} \nWe have drawn {draws} games
    {Fore.RED} \nWe have lost {losses} games {Style.RESET_ALL}
    \nWhatever the results, it has been a fun season!"""
    )


def games_report_full(game_gls, game_list, total_vs):
    """
    For MENU 2: creates content for games run down report
    """
    total_for = []
    for gls in game_gls:
        game_res = ":   |   " + str(gls) + "    -   "
        total_for.append(game_res)

    full_res = [
        str(a) + str(b) + str(c)
        for a, b, c in zip(
            game_list,
            total_for,
            total_vs,
        )
    ]
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n FULL RESULTS REPORT:{Style.RESET_ALL}
    \n{Fore.GREEN} Everett Rovers U9Y v Opponents {Style.RESET_ALL}"""
    )
    [print(game) for game in full_res]


def goals_report(games, total_gls, total_vs):
    """
    For MENU 3: creates content for goals summary report
    """
    all_gls = sum(total_gls)
    all_conceded_gls = sum(total_vs)
    av_gls = int(all_gls / games)
    gl_dif = all_gls - all_conceded_gls
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n GOALS REPORT:\n {Style.RESET_ALL}
    {Fore.GREEN} The team has scored {all_gls} goals this season
    {Style.RESET_ALL}We have done this in {games} games
    This is roughly {av_gls} goals per game; great scoring!
    {Fore.RED} \n We have conceded {all_conceded_gls} goals
    {Fore.YELLOW} \n Our goal difference is {gl_dif} goals!{Style.RESET_ALL}"""
    )


def top_scorer_report(players, total_gls):
    """
    For MENU 4: creates content for top scorer report
    """
    top_scorer = total_gls.index(max(total_gls))
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n TOP SCORER REPORT:\n
    {Back.GREEN} The top scorer is {players[top_scorer]}
    \n He has scored {max(total_gls)} this season {Style.RESET_ALL})
    But well done to all players!"""
    )


def form_report(total_gls, total_appear, players):
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
    print(
        Back.BLUE
        + f"""\n FORM REPORT:\n
    {Back.GREEN} The top ranked player is {no1_rank}
    \n Please select him as captain for the next match!\n
    {Back.RED} The low ranked player is {no7_rank}
    \n Please make him for substitute for the next match {Style.RESET_ALL}"""
    )


def run_data_input(games, players):
    """
    For MENU 6: runs all get_data functions for inputted new game
    Produces content to walk through process step by step
    """
    os.system("clear")
    game_data = get_game_data(games)
    print(Back.BLUE + f"\n Thanks, Game confirmed{Style.RESET_ALL}")
    time.sleep(2)
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n APPEARANCE INPUT: for Game {game_data - 1}{Style.RESET_ALL}"""
    )
    played_game = get_appearance_data(players, game_data)
    print(
        Back.BLUE
        + f"""\n Thanks, new appearance data has been confirmed
          {Style.RESET_ALL}"""
    )
    time.sleep(2)
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n GOALS SCORED INPUT: for Game {game_data - 1}
        {Style.RESET_ALL}"""
    )
    get_goals_data(players, played_game, game_data)
    print(
        Back.BLUE
        + f"""\n Thanks, new goal data has been confirmed
          {Style.RESET_ALL}"""
    )
    time.sleep(2)
    os.system("clear")
    print(
        Back.BLUE
        + f"""\n GOALS AGAINST INPUT: for Game {game_data - 1}
        {Style.RESET_ALL}"""
    )
    get_conceded_data(game_data)
    print(
        Back.BLUE
        + f"""\n Thanks, new conceded data has been confirmed
          {Style.RESET_ALL}"""
    )
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + "\n WELCOME BACK. New results have been calculated.")
    print(Style.RESET_ALL)


def menu(players, games, game_list, total_app, total_gls, game_gls, total_vs):
    """
    Main MENU: used by user to navigate the program
    """
    options = [
        "[1] Games Report : Performance Summary",
        "[2] Games Report : Full Results",
        "[3] Goals Report : Overall Performance",
        "[4] Who has scored the most goals this season?",
        "[5] Which player is in the best form?",
        "[6] INPUT or EDIT game figures",
        "[7] Quit",
    ]
    terminal_menu = TerminalMenu(options, title="\n MENU: Please select:")
    menu_entry_index = terminal_menu.show()
    print(f"\n You have selected: {options[menu_entry_index]}")

    if menu_entry_index == 0:
        games_report_summary(games, game_gls, total_vs)
        main()

    elif menu_entry_index == 1:
        games_report_full(game_gls, game_list, total_vs)
        main()

    elif menu_entry_index == 2:
        goals_report(games, total_gls, total_vs)
        main()

    elif menu_entry_index == 3:
        top_scorer_report(players, total_gls)
        main()

    elif menu_entry_index == 4:
        form_report(total_gls, total_app, players)
        main()

    elif menu_entry_index == 5:
        run_data_input(games, players)
        main()

    elif menu_entry_index == 6:
        os.system("clear")
        print(f"Thank you for using Everett Rovers stats reporting. Goodbye.")
        quit()


def main():
    """
    Main program begin/restart
    All base data is recalcuated to ensure up to date information provided
    """
    players = get_player_list()
    games = get_game_number()
    game_list = get_game_list(games)
    total_app = calculate_total_app(players, games)
    total_gls = calculate_total_gls(players, games)
    game_gls = calculate_total_game_gls(games)
    total_vs = calculate_total_conceded()
    menu(players, games, game_list, total_app, total_gls, game_gls, total_vs)


os.system("clear")
print(
    Back.BLUE
    + f"""\n Welcome to Everett Rovers U9Y Football team reporting
{Style.RESET_ALL}
There are various reports available to review our statistics
You can review games, goals, top scorer & form information
{Style.DIM}
[Note: you may also input new figures to ensure full game stats]
{Style.RESET_ALL}"""
)
main()
