COMPUTER_COLOR = "#E9E124";
PLAYER_COLOR = "#D62F2F";
NUETRAL_COLOR = "#FFFFFF";
BOARD_WIDTH = 7;
BOARD_HEIGHT = 6;

function reset_board() {
    $.ajax({
        url: '/reset_board',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            for (let col_index = 0; col_index < BOARD_WIDTH; col_index++) {
                for (let row_index = 0; row_index < BOARD_HEIGHT; row_index++) {
                    tile_id = "entry" + col_index + "_" + row_index;
                    tile = document.getElementById(tile_id);
                    tile.style.backgroundColor = NUETRAL_COLOR;
                }
            }

        }
    });
}

function make_player_move(col_index) {

    $.ajax({
        url: '/make_move',
        type: 'GET',
        data: { col_index: col_index },
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            console.log(response);

            if ("player_move" in response) {
                player_moves = response["player_move"]
                player_tile = "entry" + player_moves[0] + "_" + player_moves[1];
                player_location = document.getElementById(player_tile);
                player_location.style.backgroundColor = PLAYER_COLOR;
            }

            if ("ai_move" in response) {
                ai_moves = response["ai_move"]
                ai_tile = "entry" + ai_moves[0] + "_" + ai_moves[1];
                ai_location = document.getElementById(ai_tile);
                ai_location.style.backgroundColor = COMPUTER_COLOR;
            }

            if ("winner" in response) {
                if (response["winner"] == "player") {
                    alert("You win!");
                } else if (response["winner"] == "AI") {
                    alert("You lose!");
                } else {
                    alert("It's a tie!");
                }
            }
        }
    });
}