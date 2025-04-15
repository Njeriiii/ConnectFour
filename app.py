from flask import Flask, render_template, jsonify, request, redirect, url_for
from games.plain_eval import ConnectFourPlainEval

from games.fail_hard import ConnectFourFailHard
from games.fail_soft import ConnectFourFailSoft

app = Flask(__name__)

game_instances = {
    "Plain Evaluation Function": ConnectFourPlainEval,
    "Fail Soft Alpha Beta Pruning": ConnectFourFailSoft,
    "Fail Hard Alpha Beta Pruning": ConnectFourFailHard,
}

game = game_instances["Plain Evaluation Function"]()  # Initialize with default game

@app.route("/", methods=["GET", "POST"])
def index():

    # global game, game1, game2
    global game, game_instances

    if request.method == "GET":

        # Reset the game instance when the "Play Again" button is clicked
        game_choice = request.args.get("game", "Plain Evaluation Function")
        game_class = game_instances.get(
            game_choice, game_instances["Plain Evaluation Function"]
        )
        game = game_class()  # Create a new instance of the game class
        print(f"GET request received, game reset to: {game_choice}")

    winner = None

    if request.method == "POST":
        # Get the column from the form data
        col = int(request.form["column"]) - 1

        # Make the human move
        game.make_move(col, "🟡")

        # Check for a winner
        if game.check_win("🟡"):
            winner = "Human"

        else:
            # Get the AI move
            ai_col = game.get_ai_move()
            game.make_move(ai_col, "🔴")

            # Check for a winner
            if game.check_win("🔴"):
                winner = "AI"
            elif game.game_over():
                winner = "Tie"

    # Render the game board
    board = game.board

    game_name = [name for name, cls in game_instances.items() if isinstance(game, cls)][
        0
    ]

    return render_template(
        "index.html",
        board=board,
        winner=winner,
        game_name=game_name,
        game_instances=game_instances,
    )
