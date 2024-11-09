import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from sosGame import sosGame

class TestBoardSizeSelection(unittest.TestCase):

    def setUp(self):
        """This method runs before each test."""
        self.root = tk.Tk()
        self.game = sosGame(self.root)

    def tearDown(self):
        """Destroy the root window after each test."""
        self.root.destroy()

    # AC 1.1 Choose a valid board size
    @patch('tkinter.Entry.get', return_value = 6)
    def test_valid_board_size(self, mock_entry_get):
        """Test if valid board size is set correctly."""
        self.game.board.select_size()
        self.assertEqual(self.game.board.size, 6)

    # AC 1.2 Choose invalid small board size
    @patch('tkinter.Entry.get', return_value='2')
    def test_invalid_small_board_size(self, mock_entry_get):
        """Test if defaults to sixe 5 for invalid small board size."""
        self.game.board.select_size()  # invalid, size = 2
        self.assertEqual(self.game.board.size, 8)
        self.assertEqual(self.game.gui.message_label['text'], "Error: Board size too small, must be 3 or more.")
    # AC 1.3 Board size not chosen
    def test_default_board_size(self):
        """Test if the default board size is 8 when not chosen."""
        self.game.board.select_size()
        self.assertEqual(self.game.board.size, 8)

   # AC 2.1 Choose game mode
    @patch('tkinter.StringVar.get', return_value = 'General')
    def test_select_game_mode(self, mock_entry_get):
        """Test if game mode is set correctly."""
        self.game.select_mode()
        self.assertEqual(self.game.mode, "General")

   # AC 2.2 Test default game mode
    def test_default_game_mode(self):
        """Test if default board size is set correctly."""
        self.assertEqual(self.game.mode, "Simple")

   # AC 3.1 New game created with empty board of selected mode and board size
    def test_start_new_game(self):
        """Test if new game with defaults is created with empty board."""
        self.game.create_new_game()
        self.assertEqual(self.game.mode, "Simple")
        self.assertEqual(self.game.board.size, 8)
        self.assertEqual(self.game.turn.color, "Red")
        for i in range(self.game.board.size):
          for j in range(self.game.board.size):
            self.assertEqual(self.game.board.spaces[i][j]['text'], "")

   # AC 4.1 Make a valid move (simple)
    def test_make_simple_move(self):
        """Test if valid moves set spaces and change turns."""
        self.game.create_new_game()
        self.game.players[1].symbol = 'O'
        self.game.place_move(0,0)
        self.assertEqual(self.game.board.spaces[0][0]['text'], "S")
        self.assertEqual(self.game.turn.color, "Blue")
        self.game.place_move(0,1)
        self.assertEqual(self.game.board.spaces[0][1]['text'], "O")
        self.assertEqual(self.game.turn.color, "Red")

   # AC 4.2 Make an invalid move (simple)
    def test_make_invalid_simple_move(self):
        """Test if valid moves set spaces and change turns."""
        self.game.players[1].symbol = 'O'
        self.game.create_new_game()
        self.game.place_move(0,0)
        self.game.place_move(0,0)
        self.assertEqual(self.game.board.spaces[0][0]['text'], "S")
        self.assertEqual(self.game.turn.color, "Blue")
        self.assertEqual(self.game.gui.message_label['text'], "Error: Please pick unoccupied space")

   # AC 4.3 Make an invalid move outside board (simple)
    def test_make_out_of_bounds_simple_move(self):
        """Test if valid moves set spaces and change turns."""
        self.game.create_new_game()
        self.game.place_move(8,8)
        self.assertEqual(self.game.gui.message_label['text'], "Error: Not a valid space")
        self.assertEqual(self.game.turn.color, "Red")

   # AC 4.1 Make a valid move (general) (GPT written)
    def test_make_move_general(self):
        """Test if valid moves set spaces and change turns."""
        self.game.board.size = 3  # Set board size to 3 for testing
        self.game.board.spaces = [[{'text': ''} for _ in range(3)] for _ in range(3)]  # Mock board spaces
        self.game.mode = "General"

        # When I select a cell on the grid and place an 'S' in that cell
        self.game.place_move(0, 0)

        # Then the move should be registered
        self.assertEqual(self.game.board.spaces[0][0]['text'], 'S')

        # The current player's symbol should be displayed in the selected cell
        self.assertEqual(self.game.current_symbol(), 'S')

        # Check that the board state reflects the move
        expected_board = [
            [{'text': 'S'}, {'text': ''}, {'text': ''}],
            [{'text': ''}, {'text': ''}, {'text': ''}],
            [{'text': ''}, {'text': ''}, {'text': ''}]
        ]
        self.assertEqual(self.game.board.spaces, expected_board)

        # Ensure the turn has changed to the other player
        self.assertEqual(self.game.turn.color, 'Blue')

    def test_invalid_move(self):
        self.game.board.size = 3  # Set board size to 3 for testing
        self.game.board.spaces = [[{'text': ''} for _ in range(3)] for _ in range(3)]  # Mock board spaces

        self.game.mode = "General"
        self.game.place_move(0, 0)  # Make the first valid move
       # Attempt to place a move in an invalid position
        self.game.place_move(5, 5)  # Out of bounds
        self.assertEqual(self.game.board.spaces[0][0]['text'], 'S')  # The first move should still be there
        self.assertIn("Not a valid space", self.game.gui.message_label.cget("text"))

        # Attempt to place a move in the same cell
        self.game.place_move(0, 0)  # Should already be occupied
        self.assertIn("Please pick unoccupied space", self.game.gui.message_label.cget("text"))

class TestGameFunctionality(unittest.TestCase):

  @patch('tkinter.Entry.get', return_value = 3)
  def setUp(self, mock_entry_get):
    """This method runs before each test."""
    self.root = tk.Tk()
    self.game = sosGame(self.root)
    self.game.create_new_game()

  def tearDown(self):
    """Destroy the root window after each test."""
    self.root.destroy()

  # AC 5.1 Simple game over - Red wins
  def test_game_over_red_wins_simple(self):
    self.game.players[0].symbol = 'S'
    self.game.players[1].symbol = 'O'
    self.game.place_move(0, 0)
    self.game.place_move(0, 1)
    self.game.place_move(0, 2)
    self.assertEqual(self.game.players[0].score, 1)
    self.assertEqual(self.game.detect_game_ended(), True)
    self.assertEqual(self.game.determine_winner(), "Red")
    self.assertEqual(self.game.gui.message_label['text'], "Congratulations! Red has won the game!")

  # AC 5.2 Simple game over - Tie
  def test_game_over_tie_simple(self):
    self.game.place_move(0, 0)
    self.game.place_move(0, 1)
    self.game.place_move(0, 2)
    self.game.place_move(1, 0)
    self.game.place_move(1, 1)
    self.game.place_move(1, 2)
    self.game.place_move(2, 0)
    self.game.place_move(2, 1)
    self.game.place_move(2, 2)
    self.assertEqual(self.game.players[0].score, 0)
    self.assertEqual(self.game.players[1].score, 0)
    self.assertEqual(self.game.detect_game_ended(), True)
    self.assertEqual(self.game.determine_winner(), "tie")
    self.assertEqual(self.game.gui.message_label['text'], "The game has ended in a tie!")

  # AC 5.1 Simple game over - Blue wins
  def test_game_over__blue_wins_simple(self):
    self.game.place_move(0, 0)
    self.game.place_move(0, 2)
    self.game.place_move(1, 2)
    self.game.players[1].symbol = 'O'
    self.game.place_move(0, 1)
    self.assertEqual(self.game.players[1].score, 1)
    self.assertEqual(self.game.detect_game_ended(), True)
    self.assertEqual(self.game.determine_winner(), "Blue")
    self.assertEqual(self.game.gui.message_label['text'], "Congratulations! Blue has won the game!")

  # AC 7.1 General game over - Red wins
  @patch('tkinter.Entry.get', return_value = 3)
  def test_game_over_red_wins_general(self, mock_entry_get):
    self.game.mode = "General"
    self.game.create_new_game()
    self.game.place_move(0, 0)
    self.game.place_move(0, 1)
    self.game.place_move(0, 2)
    self.game.place_move(2, 0)
    self.game.place_move(2, 1)
    self.game.place_move(2, 2)
    self.game.place_move(1, 0)
    self.game.place_move(1, 2)
    self.game.players[0].symbol = 'O'
    self.game.place_move(1, 1)
    self.assertEqual(self.game.players[0].score, 4)
    self.assertEqual(self.game.players[1].score, 0)
    self.assertEqual(self.game.detect_game_ended(), True)
    self.assertEqual(self.game.determine_winner(), "Red")
    self.assertEqual(self.game.gui.message_label['text'], "Congratulations! Red has won the game!")

  # AC 7.1 General game over - Tie
  @patch('tkinter.Entry.get', return_value = 3)
  def test_game_over_tie_general(self, mock_entry_get):
    self.game.mode = "General"
    self.game.create_new_game()
    self.game.place_move(0, 0)
    self.game.place_move(0, 1)
    self.game.place_move(0, 2)
    self.game.place_move(2, 0)
    self.game.place_move(2, 1)
    self.game.place_move(2, 2)
    self.game.place_move(1, 1)
    self.game.players[0].symbol = 'O'
    self.game.players[1].symbol = 'O'
    self.game.place_move(1, 2)
    self.game.place_move(1, 0)
    self.assertEqual(self.game.players[0].score, 1)
    self.assertEqual(self.game.players[1].score, 1)
    self.assertEqual(self.game.detect_game_ended(), True)
    self.assertEqual(self.game.determine_winner(), "tie")
    self.assertEqual(self.game.gui.message_label['text'], "The game has ended in a tie!")

class TestGameOver(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.game = sosGame(self.root)
        self.game.board.size = 3
        self.game.board.spaces = [[{'text': ''} for _ in range(3)] for _ in range(3)]

    def tearDown(self):
        self.root.destroy()

    @patch('sosGame.GameGUI.display_message')
    def test_game_over_general(self, mock_display_message):
        # Set up a game-ending scenario
        self.game.mode = "General"
        self.game.players[0].score = 2
        self.game.players[1].score = 1
        self.game.board.move_count = 8  # Full board

        # Simulate the last move
        self.game.place_move(2, 2)

        # Check if the game ended
        self.assertTrue(self.game.detect_game_ended())

        # Check if the winner is correctly determined
        winner = self.game.determine_winner()
        self.assertEqual(winner, "Red")

        # Verify that the display_message method was called with the correct information
        expected_message = (
            "Congratulations! Red has won the game!"
        )
        mock_display_message.assert_called_with(expected_message)

    @patch('sosGame.GameGUI.display_message')
    def test_game_over_tie(self, mock_display_message):
        # Set up a tie scenario
        self.game.mode = "General"
        self.game.players[0].score = 1
        self.game.players[1].score = 1
        self.game.board.move_count = 8  # Full board

        # Simulate the last move
        self.game.place_move(2, 2)

        # Check if the game ended
        self.assertTrue(self.game.detect_game_ended())

        # Check if the tie is correctly determined
        winner = self.game.determine_winner()
        self.assertEqual(winner, "tie")

        # Verify that the display_message method was called with the correct information
        expected_message = (
            "The game has ended in a tie!"
        )
        mock_display_message.assert_called_with(expected_message)

class TestGameOver(unittest.TestCase):

    def setUp(self):
      self.root = tk.Tk()
      self.game = sosGame(self.root)

    def tearDown(self):
        self.root.destroy()

    # AC 8.1 Computer makes move after Human player moves
    def test_computer_moves_after_human(self):
      self.game.players[0].type = 'Human'
      self.game.players[1].type = 'Computer'
      self.game.create_new_game()
      self.game.place_move(0, 0);
      filled_spaces = 0
      for i in range(self.game.board.size):
        for j in range(self.game.board.size):
          if self.game.board.spaces[i][j]['text'] != '':
            filled_spaces += 1
      self.assertEqual(filled_spaces, 2)
      self.assertEqual(self.game.turn.color, 'Red')

    # AC 8.2 Computer makes first move when red in new game
    def test_computer_makes_first_move(self):
      self.game.players[0].type = 'Computer'
      self.game.create_new_game()
      filled_spaces = 0
      for i in range(self.game.board.size):
        for j in range(self.game.board.size):
          if self.game.board.spaces[i][j]['text'] != '':
            filled_spaces += 1
      self.assertEqual(filled_spaces, 1)
      self.assertEqual(self.game.turn.color, 'Blue')

    # AC 8.3 Computer makes winning moves
    def test_computer_makes_winning_moves(self):
      self.game.players[1].type = 'Computer'
      self.game.mode = 'General'
      self.game.create_new_game()

      #create an 'S_S' and an 'SO_' configuration
      self.game.board.set_move(0, 0, 'S')
      self.game.board.set_move(0, 1, 'O')
      self.game.place_move(2, 0)

      #verify that computer places in both positions
      self.assertEqual(self.game.players[1].score, 1)
      self.game.place_move(1, 1)
      self.assertEqual(self.game.players[1].score, 2)

if __name__ == '__main__':
    unittest.main()
