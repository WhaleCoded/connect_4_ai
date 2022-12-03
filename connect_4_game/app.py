from flask import Flask, render_template, request
import numpy as np
import torch

from model import get_and_load_model
from play import check_for_valid_game_board

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYER_VALUE = -1
AI_VALUE = 1

CURR_BOARD = np.zeros((BOARD_WIDTH, BOARD_HEIGHT))
MODEL_PATH = "/home/dallin/byu/fall_2022/machine_learning/connect_4/deep_learning/model_6_0_3_12.pt"
MODEL = get_and_load_model(MODEL_PATH)

app = Flask(__name__)


def check_for_winner():
    player_won = check_for_valid_game_board(CURR_BOARD, PLAYER_VALUE)

    if not player_won:
        ai_won = check_for_valid_game_board(CURR_BOARD, AI_VALUE)

        if ai_won:
            return "AI"
    else:
        return "player"

    return None


def check_for_tie():
    return not (CURR_BOARD == 0).any()


@app.route("/")
def index():
    return render_template("index.html", width=BOARD_WIDTH, height=BOARD_HEIGHT)


@app.route("/reset_board", methods=["POST"])
def reset_board():
    global CURR_BOARD
    CURR_BOARD = np.zeros((BOARD_WIDTH, BOARD_HEIGHT))

    return "success"


@app.route("/make_move", methods=["GET"])
def make_move():
    winner = check_for_winner()
    tie = check_for_tie()
    if winner is None and not tie:
        col_index = int(request.args.get("col_index"))

        player_move_made = False
        player_move = None
        for row_index in range(BOARD_HEIGHT):
            if CURR_BOARD[col_index, row_index] == 0:
                CURR_BOARD[col_index, row_index] = PLAYER_VALUE
                player_move_made = True
                player_move = (col_index, row_index)
                break

        winner = check_for_winner()
        if winner is not None:
            return {"winner": winner, "player_move": player_move}

        ai_move = None
        if player_move_made:
            transformed_data = torch.tensor(
                CURR_BOARD.reshape(1, 1, BOARD_WIDTH, BOARD_HEIGHT)
            ).float()
            results = MODEL(transformed_data)
            ai_move = int(torch.argmax(results))

            for row_index in range(BOARD_HEIGHT):
                if CURR_BOARD[ai_move, row_index] == 0:
                    CURR_BOARD[ai_move, row_index] = AI_VALUE
                    ai_move = (ai_move, row_index)
                    break

        if player_move is None and ai_move is None:
            return
        elif player_move is None:
            return

        winner = check_for_winner()
        if winner is not None:
            return {"winner": winner, "player_move": player_move, "ai_move": ai_move}

        if check_for_tie():
            return {"winner": "tie"}

        return {"player_move": player_move, "ai_move": ai_move}
    else:
        if winner is not None:
            return {"winner": winner}

        if tie:
            return {"winner": "tie"}


if __name__ == "__main__":
    app.run(debug=True)
