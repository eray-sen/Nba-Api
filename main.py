import requests
import time
from prettytable import PrettyTable


class link:

    def __init__(self):
        self.api_url_players = "https://www.balldontlie.io/api/v1/players"
        self.api_url_teams = "https://www.balldontlie.io/api/v1/teams"
        self.api_url_games = "https://www.balldontlie.io/api/v1/games"
        self.api_url_stats = "https://www.balldontlie.io/api/v1/stats"
        #definition of links that are used in the program

class players(link):

    def get_all_players(self):
        page = 0
        total_page = 39 #there are about 39k players
        total_page = 39 #there are approximately 39k players
        table = PrettyTable(['ID', 'F_name', 'L_name', 'Team', ])

        while page <= total_page:
            params = {
                "page": page,
                "per_page": 100
            }
            response = requests.get(
                self.api_url_players, params=params)

            players_data = response.json()["data"] #the information inside the 'data' is converted to string from json form
            players_data = response.json()["data"] # the information inside the 'data' is converted to string from JSON form
            print(response.status_code)

            for data in players_data:
                teams_data = data["team"]
                table.add_row(
                    [data["id"], data["first_name"], data["last_name"], teams_data["full_name"]])
            page += 1

        print(table)

    def get_players_by_names(self):
        table = PrettyTable(['ID', 'F_name', 'L_name', 'Team'])

        name = input("Name:")
        response = requests.get(self.api_url_players + "?search=" + name)
        print(response.status_code)

        players_data = response.json()["data"]
        print(response.status_code)

        for data in players_data:
            teams_data = data["team"]

            table.add_row(
                [data["id"], data["first_name"], data["last_name"], teams_data["full_name"]])

        print(table)

    def get_players_by_team_name(self):
        page = 0
        total_page = 39
        table = PrettyTable(['ID', 'F_name', 'L_name', 'Team'])
        team_name = input("Team-Name(abbreviation):").upper()

        while page <= total_page:
            params = {
                "page": page,
                "per_page": 100
            }
            response = requests.get(
                self.api_url_players, params=params)

            players_data = response.json()["data"]

            for data in players_data:
                teams_data = data["team"]

                if team_name == teams_data["abbreviation"]:
                    table.add_row(
                        [data["id"], data["first_name"], data["last_name"], teams_data["full_name"]])

            page += 1

        print(table)


class teams(link):

    def get_all_teams(self):
        response = requests.get(self.api_url_teams)
        print(response.json())
        print(response.status_code)

        teams_data = response.json()["data"]
        table = PrettyTable(['ID', 'Abbreviation', 'Conference', 'Full Name'])

        for data in teams_data:
            table.add_row([data["id"], data["abbreviation"], data["conference"], data["full_name"]])

        print(table)

    def get_a_team_by_abb(self):

        response = requests.get(self.api_url_teams)
        print(response.status_code)
        teams_data = response.json()["data"]

        team = input("Team-Name(abbreviation):").upper()
        table = PrettyTable(['ID', 'Abbreviation', 'City', 'Conference', 'Division', 'Name', 'Full-Name'])

        for data in teams_data:
            if team == data["abbreviation"]:
                table.add_row(
                    [data["id"], data["abbreviation"], data["city"], data["conference"], data["division"], data["name"],
                     data["full_name"]])
                break

        print(table)

    def get_teams_by_conference(self):

        response = requests.get(self.api_url_teams)
        print(response.status_code)
        teams_data = response.json()["data"]

        conference = input("Conference-Name(East/West):").upper()
        table = PrettyTable(['ID', 'Abbreviation', 'Conference', 'Full Name'])

        for data in teams_data:
            if conference == data["conference"].upper():
                table.add_row([data["id"], data["abbreviation"], data["conference"], data["full_name"]])

        print(table)


class games(link):

    def get_all_games_of_a_team_for_a_specific_season(self):

        team = input("Team(abbreviation):").upper()
        season = input("Season:")

        response_team_id = requests.get(self.api_url_teams)
        print(response_team_id.status_code)

        teams_data = response_team_id.json()["data"]

        for data in teams_data:
            if team == data["abbreviation"]:
                team_id = data["id"]
                break

        page = 0
        total_page = 15

        table = PrettyTable(['ID', 'Home-Team', 'Home-Score', 'Visitor-Score', 'Visitor-Team', 'Date', 'Status'])

        while page <= total_page:

            params = {
                "page": page,
            }

            response = requests.get(self.api_url_games + "?seasons[]=" + season + "&team_ids[]=" + str(team_id),
                                    params=params)
            print(response.status_code)
            games_data = response.json()["data"]

            for data in games_data:
                home_teams_data = data["home_team"]
                visitor_teams_data = data["visitor_team"]

                table.add_row(
                    [data["id"], home_teams_data["full_name"], data["home_team_score"], data["visitor_team_score"],
                     visitor_teams_data["full_name"], data["date"][0:10], data["status"]])

            page += 1
        print(table)

    def get_all_games_between_two_teams_in_a_specific_year(self):

        team1 = input("Team-1(abbreviation):").upper()
        team2 = input("Team-2(abbreviation):").upper()
        season = input("Season:")
        team1_id = None
        team2_id = None

        response_team = requests.get(self.api_url_teams)
        teams_data = response_team.json()["data"]
        for data in teams_data:
            if team1 == data["abbreviation"]:
                team1_id = data["id"]
            elif team2 == data["abbreviation"]:
                team2_id = data["id"]
            elif team1_id is not None and team2_id is not None:
                break

        table = PrettyTable(['ID', 'Home-Team', 'Home-Score', 'Visitor-Score', 'Visitor-Team', 'Date', 'Status'])

        params = {
            "per_page": 100
        }
        response = requests.get(self.api_url_games + "?seasons[]=" + season + "&team_ids[]=" + str(team1_id),
                                params=params)
        # all games of team1 in a specific season
        print(response.status_code)
        games_data = response.json()["data"]

        for data in games_data:
            home_team_data = data["home_team"]
            home_team_id = home_team_data["id"]

            visitor_team_data = data["visitor_team"]
            visitor_team_id = visitor_team_data["id"]

            if team2_id == home_team_id or team2_id == visitor_team_id:
                # team 1 is exactly the home or visitor team because of request
                table.add_row(
                    [data["id"], home_team_data["full_name"], data["home_team_score"],
                     data["visitor_team_score"],
                     visitor_team_data["full_name"], data["date"][0:10], data["status"]])
        print(table)

    def deneme(self, ):
        page = 0
        i = 0

        while True:
            params = {
                "page": page,
                "per_page": 100
            }
            response = requests.get(self.api_url_games + "?seasons[]=2019", params=params)
            all_data = response.json()["data"]

            for data in all_data:
                print(i)
                print(data)
                i += 1

            if i % 100 != 0:
                print("TOTAL GAME")
                print(i)
                break
            else:
                page += 1


class stats(link):

    def get_the_stats_of_players_in_a_specific_game(self):
        error = 1
        while error == 1:
            error = 0
            game_id = input("Game-ID:")  # (1-46941)
            table_of_the_game = PrettyTable(
                ['ID', 'Home-Team', 'Home-Score', 'Visitor-Score', 'Visitor-Team', 'Date', 'Status'])
            table_players_stats_home_team = PrettyTable(['ID', 'First-Name', 'Surname', 'Pts', 'Ast', 'Reb', 'Min'])
            table_players_stats_visitor_team = PrettyTable(['ID', 'First-Name', 'Surname', 'Pts', 'Ast', 'Reb', 'Min'])
            try:
                response1 = requests.get(self.api_url_stats + "?game_ids[]=" + game_id)
                response2 = requests.get(self.api_url_teams)

                teams_names = response2.json()["data"]
                stats_data = response1.json()["data"]

                game_data = stats_data[0]["game"]

                home_team_id = game_data["home_team_id"]
                visitor_team_id = game_data["visitor_team_id"]
                home_team_name = None
                visitor_team_name = None

                for data in teams_names:
                    if home_team_id == data["id"]:
                        home_team_name = data["full_name"]
                    elif visitor_team_id == data["id"]:
                        visitor_team_name = data["full_name"]

                    if home_team_name is not None and visitor_team_name is not None:
                        table_of_the_game.add_row([game_data["id"], home_team_name, game_data["home_team_score"],
                                                   game_data["visitor_team_score"], visitor_team_name,
                                                   game_data["date"][0:10], game_data["status"]])
                        break

                for data in stats_data:
                    teams_data = data["team"]
                    player_data = data["player"]

                    if teams_data["id"] == home_team_id:

                        table_players_stats_home_team.add_row(
                            [player_data["id"], player_data["first_name"], player_data["last_name"],
                             data["pts"], data["ast"], data["reb"],
                             data["min"]])

                    elif teams_data["id"] == visitor_team_id:

                        table_players_stats_visitor_team.add_row(
                            [player_data["id"], player_data["first_name"], player_data["last_name"],
                             data["pts"], data["ast"], data["reb"],
                             data["min"]])

                print(table_of_the_game)
                print("")
                print(table_players_stats_home_team)
                print("")
                print(table_players_stats_visitor_team)

            except:
                print("There is no game which has this ID!")
                error = 1


def main():
    while True:
        Error = 1
        print("\n 1-Players \t 2-Teams \t 3-Games \t 4-Statistics \t 5-Exit")
        choise = input("Choise a section:")
        if choise == "5":
            exit()
        while Error == 1:
            Error = 0
            if choise == "1":
                player = players()
                print("\n 1-Get all players \n 2-Get players by name \n 3-Get players by their team name \n 4-Back ")
                choise_players = input("Choise a section:")

                if choise_players == "1":
                    player.get_all_players()
                elif choise_players == "2":
                    player.get_players_by_names()
                elif choise_players == "3":
                    player.get_players_by_team_name()
                elif choise_players == "4":
                    break
                else:
                    print("Invalid Choise!")
                    Error = 1

            if choise == "2":
                team = teams()
                print("\n 1-Get all teams \n 2-Get a team by abbreviation \n 3-Get all teams by conference \n 4-Back")
                choise_teams = input("Choise a section:")

                if choise_teams == "1":
                    team.get_all_teams()
                elif choise_teams == "2":
                    team.get_a_team_by_abb()
                elif choise_teams == "3":
                    team.get_teams_by_conference()
                elif choise_teams == "4":
                    break
                else:
                    print("Invalid Choise!")
                    Error = 1

            if choise == "3":
                game = games()
                print("\n 1-Get all games of a team for a specific season \n 2-Get all games between two teams  in a "
                      "specific year \n 3-Back")
                choise_game = input("Choise a section:")

                if choise_game == "1":
                    game.get_all_games_of_a_team_for_a_specific_season()
                elif choise_game == "2":
                    game.get_all_games_between_two_teams_in_a_specific_year()
                elif choise_game == "3":
                    break
                else:
                    print("Invalid Choise!")
                    Error = 1

            if choise == "4":
                statistics = stats()
                print("\n 1-Get stats of players in a specific game")
                choise_statistics = input("Choise a section:")

                if choise_statistics == "1":
                    statistics.get_the_stats_of_players_in_a_specific_game()

                else:
                    print("Invalid Choise!")
                    Error = 1


main()
