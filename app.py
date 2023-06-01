from flask import Flask, session, render_template, request, jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "some-secret-token"

@app.route("/")
def launch_app():
    """Make and display board"""
    #initialize board
    board = boggle_game.make_board()
    #creates dict-like object stored in session
    session['board'] = board
    #fetch highscore and num of plays from session with default val of 0
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)
    return render_template("base.html", board=board, highscore=highscore, num_plays=num_plays)

@app.route("/verify-word", methods=["GET"])
def verify_word():
    """Check word submission against dictionary"""
    #retrieve word from form submission
    word = request.args.get("word")
    #retrieve board from session
    board = session["board"]
    #check if valid word within board and return response
    response = boggle_game.check_valid_word(board, word)
    return jsonify({"result": response})

@app.route("/update-stats", methods=["POST"])
def update_stats():
    """retrieve and update stats for score, high score, and num_plays"""
    #flask request score as json object
    score = request.json["score"]
    #fetch highscore and num of plays from session with default val of 0
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)
    #update session
    session["highscore"] = max(score, highscore)
    session["num_plays"] = num_plays + 1

    return jsonify(personalRecord = score > highscore)
    
