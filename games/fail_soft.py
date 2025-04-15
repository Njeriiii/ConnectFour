# Fail-soft alpha-beta pruning
class ConnectFourFailSoft:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        print("Beginning FAil-soft alpha-beta pruning")
        return [[" " for _ in range(7)] for _ in range(6)]  # 6 rows, 7 columns

    def make_move(self, col, player):
        """
        Simulate placing a piece on the board.
        """
        for row in range(
            5, -1, -1
        ):  # Start from the bottom, looking for the first empty spot in the chosen column
            if self.board[row][col] == " ":
                self.board[row][col] = player
                return self.board

    def undo_move(self, col):
        """
        Reverse the previous move.
        """
        for row in range(6):  # Search from the top down
            if self.board[row][col] != " ":
                self.board[row][col] = " "
                return self.board

    def is_valid_move(self, col):
        """
        Check if a spot is available in the column of top row -- means there is a spot available to place a piece in that column
        """
        return self.board[0][col] == " "  # Top row of the column is empty

    def count_potential_lines(self, player):
        """
        Count the number of potential two-in-a-rows and three-in-a-rows.
        Analyze the board for lines that could lead to a win.
        """
        count = 0

        if player == "🔴":
            opponent = "🟡"
        else:
            opponent = "🔴"

        # Horizontal checks
        for row in range(6):
            for col in range(4):
                window = self.board[row][col : col + 4]  # Check for groups of 4 columns
                if window.count(player) == 2 and window.count(" ") == 2:
                    count += 1  # Potential 2-in-a-row
                if window.count(player) == 3 and window.count(" ") == 1:
                    count += 20  # Potential 3-in-a-row (more valuable)
                if window.count(player) == 4:
                    count += 10000
                if opponent in window:
                    if window.count(opponent) == 3 and window.count(" ") == 1:
                        count -= 10  # Block opponent's 3-in-a-row
                    if window.count(opponent) == 4:
                        count -= 500

        # Vertical checks
        for row in range(3):
            for col in range(7):
                window = [
                    self.board[row + i][col] for i in range(4)
                ]  # Check for groups of 4 rows
                if window.count(player) == 2 and window.count(" ") == 2:
                    count += 1
                if window.count(player) == 3 and window.count(" ") == 1:
                    count += 20
                if window.count(player) == 4:
                    count += 10000
                if opponent in window:
                    if window.count(opponent) == 3 and window.count(" ") == 1:
                        count -= 10  # Block opponent's 3-in-a-row
                    if window.count(opponent) == 4:
                        count -= 500

        # Diagonal checks (positive slope)
        for row in range(3):
            for col in range(4):
                window = [self.board[row + i][col + i] for i in range(4)]
                if window.count(player) == 2 and window.count(" ") == 2:
                    count += 1
                if window.count(player) == 3 and window.count(" ") == 1:
                    count += 20
                if window.count(player) == 4:
                    count += 10000
                if opponent in window:
                    if window.count(opponent) == 3 and window.count(" ") == 1:
                        count -= 10  # Block opponent's 3-in-a-row
                    if window.count(opponent) == 4:
                        count -= 500

        # Diagonal checks (negative slope)
        for row in range(3):
            for col in range(4):
                window = [self.board[row + 3 - i][col + i] for i in range(4)]
                if window.count(player) == 2 and window.count(" ") == 2:
                    count += 1
                if window.count(player) == 3 and window.count(" ") == 1:
                    count += 20
                if window.count(player) == 4:
                    count += 10000
                if opponent in window:
                    if window.count(opponent) == 3 and window.count(" ") == 1:
                        count -= 10  # Block opponent's 3-in-a-row
                    if window.count(opponent) == 4:
                        count -= 500

        return count

    def check_win(self, player):
        # Horizontal checks
        for row in range(6):
            for col in range(4):  # Only need to check groups of 4
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Vertical checks
        for row in range(3):  # Only need to check up to the third row from the bottom
            for col in range(7):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Diagonal checks (positive slope)
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Diagonal checks (negative slope)
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False  # No win detected

    def game_over(self):
        """
        Check for wins, losses, or a tie.
        """
        if self.check_win("🔴") or self.check_win("🟡"):
            return True  # Someone won
        elif all(row[0] != " " for row in self.board):
            return True  # Tie game
        else:
            return False

    def heuristic(self):
        """
        Simple Evaluation Function
        A straightforward heuristic counts the potential two-in-a-rows and three-in-a rows for both the AI and the opponent:
        """
        ai_score = self.count_potential_lines("🔴")
        opponent_score = self.count_potential_lines("🟡")

        return ai_score - opponent_score

    def minimax(self, depth, alpha, beta, is_maximizing):
        if self.game_over() or depth == 0:  # Check terminal conditions
            return self.heuristic()

        if is_maximizing:  # Whether it's the AI's turn to maximize the score.
            best_score = -float("inf")
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col, "🔴")  # Simulate AI move
                    score = self.minimax(depth - 1, alpha, beta, False)
                    self.undo_move(col)  # Undo for exploration
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)  # Fail-soft alpha-beta pruning
                    if beta <= best_score:  # if score > beta: break
                        break

            return best_score

        else:  # Minimizing player (the opponent)
            best_score = float("inf")
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col, "🟡")  # Simulate opponent move  # Human
                    score = self.minimax(depth - 1, alpha, beta, True)
                    self.undo_move(col)  # Undo for exploration
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if best_score <= alpha:
                        break
            return best_score

    def print_board(self):
        numbers = " | ".join(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"])
        print("| " + numbers + " |")
        for row in self.board:
            print("|", " | ".join(ch if ch != " " else "⚪️" for ch in row), "|")

    def get_ai_move(self):
        depth = 6  # You can adjust search depth
        best_score = -float("inf")
        best_col = None
        alpha = -float("inf")
        beta = float("inf")

        for col in range(7):
            if self.is_valid_move(col):
                board_copy = [
                    row[:] for row in self.board
                ]  # Create a copy of the board
                self.make_move(col, "🔴")
                score = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(col)  # Restore the board

            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def get_human_move(self):
        print("Beginning FAil-soft alpha-beta pruning")
        while True:
            try:
                col = int(input("Human player, select a column (1-7): ")) - 1
                if self.is_valid_move(col):
                    return col
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def play_game(self):
        current_player = "AI"  # Or choose who starts

        while not self.game_over():
            self.print_board()
            print("\n")

            if current_player == "AI":
                col = self.get_ai_move()
                self.make_move(col, "🔴")
            else:
                col = self.get_human_move()
                print("col to play", col)
                print("Human player plays. Please wait...")
                self.make_move(col, "🟡")
            current_player = "Human" if current_player == "AI" else "AI"

        # Game over!
        self.print_board()
        if self.check_win("🔴"):
            print("AI Wins!")
        elif self.check_win("🟡"):
            print("Human Wins!")
        else:
            print("It's a tie!")


# # To play the game
# game = ConnectFour()
# game.play_game()
