import os
import time
from colorama import Fore, Back, Style
from simple_term_menu import TerminalMenu
from get_data import *

R = Style.RESET_ALL


def games_report_summary(games, wins, draws, losses):
    """For MENU 1: creates content for games summary report"""
    print(
        Back.BLUE
        + f"""\n GAMES SUMMARY REPORT:{R}
    \n Everett Rovers U9Y has played {games} games this season {R}
    {Fore.GREEN} \n We have won {wins} games
    {Fore.YELLOW} \n We have drawn {draws} games
    {Fore.RED} \n We have lost {losses} games {R}
    \n Whatever the results, it has been a fun season!"""
    )


def games_report_full(full_res):
    """For MENU 2: creates content for games run down report"""
    print(
        Back.BLUE
        + f"""\n FULL RESULTS REPORT:{R}
    \n{Fore.GREEN} Everett Rovers U9Y v Opponents\n {R}"""
    )
    [print(game) for game in full_res]


def goals_report(games, all_gls, av_gls, all_conceded_gls, gl_dif):
    """For MENU 3: creates content for goals summary report"""
    print(
        Back.BLUE
        + f"""\n GOALS REPORT:{R}
    {Fore.GREEN}\n The team has scored {all_gls} goals this season
    {R}\n We have done this in {games} games
    \n This is roughly {av_gls} goals per game; great scoring!
    {Fore.RED} \n We have conceded {all_conceded_gls} goals
    {Fore.YELLOW} \n Our goal difference is {gl_dif} goals!{R}"""
    )


def top_scorer_report(players, top_scorer, total_gls):
    """For MENU 4: creates content for top scorer report"""
    print(
        Back.BLUE
        + f"""\n TOP SCORER REPORT:{R}
    {Back.GREEN}\n The top scorer is {players[top_scorer]}{R}
    \n He has scored {Fore.YELLOW}{max(total_gls)}{R} this season
    \n But well done to all players!"""
    )


def form_report(no1_rank, no7_rank):
    """For MENU 5: creates content for form report"""
    print(
        Back.BLUE
        + f"""\n FORM REPORT:{R}
    {Back.GREEN}\n The top ranked player is {no1_rank}{R}
    \n Please select him as captain for the next match!
    {Back.RED}\n The low ranked player is {no7_rank}{R}
    \n Please make him for substitute for the next match :)"""
    )


def run_data_input(games, players):
    """
    For MENU 6: runs all get_data functions for inputted new game info
    Produces content to walk through process step by step
    """
    game_data = get_game_data(games)
    print(Back.BLUE + f"\n Thanks, Game confirmed{R}")
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n APPEARANCE INPUT: for Game {game_data - 1}{R}")
    played_game = get_appearance_data(players, game_data)
    print(Back.BLUE + f"\n Thanks, new appearance data has been confirmed{R}")
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n GOALS SCORED INPUT: for Game {game_data - 1}{R}")
    get_goals_data(players, played_game, game_data)
    print(Back.BLUE + f"\n Thanks, new goal data has been confirmed{R}")
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n GOALS AGAINST INPUT: for Game {game_data - 1}{R}")
    get_conceded_data(game_data)
    print(Back.BLUE + f"\n Thanks, new conceded data has been confirmed{R}")
    time.sleep(2)
    os.system("clear")
    print(Back.BLUE + f"\n WELCOME BACK. New results have been calculated.{R}")


def menu(players, games, total_app, total_gls, game_gls, total_vs):
    """Main MENU: used by user to navigate the program"""
    options = [
        "[1] Games Report : Performance Summary",
        "[2] Games Report : Full Results",
        "[3] Goals Report : Overall Performance",
        "[4] TOP SCORER REPORT",
        "[5] FORM PLAYER REPORT",
        "[6] INPUT or EDIT game figures",
        "[7] Quit",
    ]
    terminal_menu = TerminalMenu(options, title="\n MENU: Please select:")
    menu_entry_index = terminal_menu.show()
    os.system("clear")
    print(f"\n You have selected: {options[menu_entry_index]}")

    if menu_entry_index == 0:
        win_draw_loss = calculate_results(game_gls, total_vs)
        wins = win_draw_loss.count("W")
        draws = win_draw_loss.count("D")
        losses = win_draw_loss.count("L")
        games_report_summary(games, wins, draws, losses)
        main()

    elif menu_entry_index == 1:
        full_res = calculate_full_results(games, game_gls, total_vs)
        games_report_full(full_res)
        main()

    elif menu_entry_index == 2:
        all_gls = sum(total_gls)
        all_conceded_gls = sum(total_vs)
        av_gls = int(all_gls / games)
        gl_dif = all_gls - all_conceded_gls
        goals_report(games, all_gls, av_gls, all_conceded_gls, gl_dif)
        main()

    elif menu_entry_index == 3:
        top_scorer = total_gls.index(max(total_gls))
        top_scorer_report(players, top_scorer, total_gls)
        main()

    elif menu_entry_index == 4:
        no1_rank = calculate_form_ranking(players, total_gls, total_app)
        no7_rank = calculate_form_ranking(players, total_gls, total_app)
        form_report(no1_rank, no7_rank)
        main()

    elif menu_entry_index == 5:
        run_data_input(games, players)
        main()

    elif menu_entry_index == 6:
        os.system("clear")
        print(
            f"""\nThanks for using Everett Rovers stats reporting.
              Goodbye.:)\n"""
        )
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
    total_vs = calculate_total_conceded()
    menu(players, games, total_app, total_gls, game_gls, total_vs)


os.system("clear")
print(
    Back.BLUE
    + f"""\n Welcome to Everett Rovers U9Y Football team reporting{R}
\n There are various reports available to review our statistics
 You can review games, goals, top scorer & form information
{Style.DIM}
[Note: you may also input new figures to ensure full game stats]{R}"""
)
main()
