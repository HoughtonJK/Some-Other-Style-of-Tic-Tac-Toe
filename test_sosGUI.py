import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from sosGUI import GameGUI

class TestBoardSizeSelection(unittest.TestCase):

    def setUp(self):
        """This method runs before each test."""
        self.root = tk.Tk()
        self.game = GameGUI(self.root)


    def tearDown(self):
        """Destroy the root window after each test."""
        self.root.destroy()

    # AC 1.1 Choose a valid board size
    @patch('tkinter.Entry.get', return_value = 6)
    def test_valid_board_size(self, mock_entry_get):
        """Test if valid board size is set correctly."""
        self.game.select_size()
        self.assertEqual(self.game.board_size, 6)

    # AC 1.2 Choose invalid small board size
    @patch('tkinter.Entry.get', return_value='2')
    def test_invalid_small_board_size(self, mock_entry_get):
        """Test if defaults to sixe 5 for invalid small board size."""
        self.game.select_size()  # invalid, size = 2
        self.assertEqual(self.game.board_size, 8)

    # AC 1.3 Board size not chosen
    def test_default_board_size(self):
        """Test if the default board size is 8 when not chosen."""
        self.assertEqual(self.game.board_size, 8)

   # AC 2.1 Choose game mode
    @patch('tkinter.StringVar.get', return_value = 'General')
    def test_select_game_mode(self, mock_entry_get):
        """Test if valid board size is set correctly."""
        self.game.select_mode()
        self.assertEqual(self.game.game_mode, "General")

   # AC 2.2 Choose a valid board size
    def test_default_game_mode(self):
        """Test if valid board size is set correctly."""
        self.assertEqual(self.game.game_mode, "Simple")





if __name__ == '__main__':
    unittest.main()
