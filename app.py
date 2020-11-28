from datetime import timedelta
import random
from flask import Flask, redirect, render_template, request, session, url_for
from collections import deque

app = Flask(__name__)

app.secret_key = "45Q@3DS*wo64Uzae%98hmargh"
app.permanent_session_lifetime = timedelta(minutes=60)

playersList = []


class Match:
    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2


@app.route('/', methods=["POST", "GET"])
def home():
    game = {}
    if request.method == "POST":
        session['player_list'] = []
        session['gameSetup'] = []
        game_date = request.form['gameDateInput']
        game_location = request.form['gameLocationInput']
        game_amount = request.form['gameAmountInput']
        print(game_date + game_amount + game_location)
        game = {"date": game_date, "loc": game_location, "amount": game_amount}
        session['gameSetup'] = game
        return render_template("index.html", gameStuff=game)
    return render_template("index.html")


@app.route('/addPlayer', methods=["POST", "GET"])
def player():
    if request.method == "POST":
        game = session['gameSetup']
        p_name = request.form['playerName']
        p_email = request.form["playerEmail"]
        print(p_name + " " + p_email)
        players = {"name": p_name, "email": p_email}
        playersList.append(players)
        session['player_list'] = playersList
        return render_template("index.html", gameStuff=game)


@app.route('/gameResults', methods=["POST", "GET"])
def game_results():
    if request.method == "POST":
        loop = False
        p_list = session['player_list']
        names_list = []
        email_list = []
        final_list = []
        for p in p_list:
            names_list.append(p["name"])
            email_list.append(p["email"])

        names_list_two = list(names_list)
        random.shuffle(names_list)
        print(names_list)
        print(names_list_two)
        count = len(names_list)
        i = 0
        names_list_two = deque(names_list_two)
        names_list_two.rotate(1)
        for i in range(len(names_list)):
            if names_list[i] != names_list_two[i]:
                final_match = {"name1": names_list[i], "name2": names_list_two[i]}
                final_list.append(final_match)
            else:
                print("error: match")

        print(final_list)
        print(len(final_list))
        return render_template("results_page.html", game=session['gameSetup'],
                               names=final_list, email=email_list)


@app.route('/gameClear')
def game_clear():
    session['player_list'] = []
    session['gameSetup'] = []
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
