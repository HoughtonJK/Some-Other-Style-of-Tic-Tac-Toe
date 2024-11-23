import datetime
import time
import random
import tkinter as tk
from sosGUI import GameGUI

class Player:
  def __init__(self, color):
    self.color = color
    self.score = 0
    self.symbol = 'S'
    self.type = 'Human' # Alternatively, 'Computer'

  def change_symbol(self, symbol):
    self.symbol = symbol

  def change_type(self, type):
    self.type = type

  def get_score(self):
    return self.score

  def score_point(self):
    self.score += 1

class sosGame:
  def __init__(self, root):
    self.root = root
    self.mode = "Simple"
    self.players = [Player("Red"), Player("Blue")]
    self.turn = self.players[0]
    self.board = sosBoard(self, 0)
    self.gui = GameGUI(self, self.root)

  def select_mode(self):
    self.gui.clear_message()
    self.mode = self.gui.selected_mode.get()
    self.gui.show_stuff()

  def current_symbol(self):
    return self.turn.symbol

  def place_move(self, i, j):
    if (i >= self.board.size or i < 0 or j >= self.board.size or j < 0):
      self.gui.display_message("Error: Not a valid space")
      return
    if not self.detect_game_ended():
      if self.board.spaces[i][j]['text'] == '':
        self.gui.clear_message()
        self.board.set_move(i, j, self.current_symbol())
        if self.turn.type != 'Replay':
          self.recording.write(f"{i}, {j}, {self.current_symbol()}\n")
        self.score_sos(i, j)
        self.gui.display_scores()
        if (self.detect_game_ended()):
          if (self.determine_winner() != 'tie'):
            self.gui.display_message(f"Congratulations! {self.determine_winner()} has won the game!")
          else:
            self.gui.display_message("The game has ended in a tie!")
          return
        self.change_turn()
      else:
        self.gui.display_message("Error: Please pick unoccupied space")

  def change_turn(self):
    self.turn = self.players[1] if self.turn == self.players[0] else self.players[0]
    self.gui.display_turn()
    if self.turn.type == 'Computer':
      self.computer_turn()
    if self.turn.type == 'Replay':
      self.replay_turn()

  def computer_turn(self):
    move = self.board.best_move()
    if (move[2] != ''):
      i = move[0][0]
      j = move[0][1]
      symbol = move[2]
    else:
      symbol = random.choice(['S', 'O'])
      i = random.randint(0,self.board.size - 1)
      j = random.randint(0,self.board.size - 1)
      while (not self.board.valid_move(i, j) or not self.board.good_move(i, j, symbol)):
        symbol = random.choice(['S', 'O'])
        i = random.randint(0,self.board.size - 1)
        j = random.randint(0,self.board.size - 1)
    self.turn.change_symbol(symbol)
    self.place_move(i, j)

  #change to detect_sos()
  def score_sos(self, i, j):
    if self.board.spaces[i][j]['text'] == 'O':
      if i > 0 and j > 0 and i < self.board.size - 1 and j < self.board.size - 1 and self.board.spaces[i + 1][j + 1]['text'] == 'S' and self.board.spaces[i - 1][j - 1]['text'] == 'S':
        self.turn.score_point()
      if i > 0 and j > 0 and i < self.board.size - 1 and j < self.board.size - 1 and self.board.spaces[i + 1][j - 1]['text'] == 'S' and self.board.spaces[i - 1][j + 1]['text'] == 'S':
        self.turn.score_point()
      if j > 0 and j < self.board.size - 1 and self.board.spaces[i][j + 1]['text'] == 'S' and self.board.spaces[i][j - 1]['text'] == 'S':
        self.turn.score_point()
      if i > 0 and i < self.board.size - 1 and self.board.spaces[i + 1][j]['text'] == 'S' and self.board.spaces[i - 1][j]['text'] == 'S':
        self.turn.score_point()
    if self.board.spaces[i][j]['text'] == 'S':
      if i < self.board.size - 2 and j < self.board.size - 2 and self.board.spaces[i + 1][j + 1]['text'] == 'O' and self.board.spaces[i + 2][j + 2]['text'] == 'S':
        self.turn.score_point()
      if j > 1 and i < self.board.size - 2 and self.board.spaces[i + 1][j - 1]['text'] == 'O' and self.board.spaces[i + 2][j - 2]['text'] == 'S':
        self.turn.score_point()
      if j < self.board.size - 2 and self.board.spaces[i][j + 1]['text'] == 'O' and self.board.spaces[i][j + 2]['text'] == 'S':
        self.turn.score_point()
      if i < self.board.size - 2 and self.board.spaces[i + 1][j]['text'] == 'O' and self.board.spaces[i + 2][j]['text'] == 'S':
        self.turn.score_point()
      if i > 1 and j > 1 and self.board.spaces[i - 1][j - 1]['text'] == 'O' and self.board.spaces[i - 2][j - 2]['text'] == 'S':
        self.turn.score_point()
      if i > 1 and j < self.board.size - 2 and self.board.spaces[i - 1][j + 1]['text'] == 'O' and self.board.spaces[i - 2][j + 2]['text'] == 'S':
        self.turn.score_point()
      if j > 1 and self.board.spaces[i][j - 1]['text'] == 'O' and self.board.spaces[i][j - 2]['text'] == 'S':
        self.turn.score_point()
      if i > 1 and self.board.spaces[i - 1][j]['text'] == 'O' and self.board.spaces[i - 2][j]['text'] == 'S':
        self.turn.score_point()

  def detect_game_ended(self):
    if self.mode == 'Simple':
      if (self.players[1].score > 0 or self.players[0].score > 0 or self.board.is_board_full()):
        self.recording.close()
        return True
      else:
        return False
    else:
      if (self.board.is_board_full()):
        self.recording.close()
        return True
      else:
        return False

  def determine_winner(self):
    if (self.players[1].score > self.players[0].score):
      return self.players[1].color
    elif (self.players[1].score < self.players[0].score):
      return self.players[0].color
    else:
      return 'tie'

  def create_new_game(self):
    self.gui.clear_board()
    self.gui.clear_message()
    size = int(self.gui.board_size_entry.get()) if self.gui.board_size_entry.get() != '' else 8
    self.board.select_size(size)
    self.players[0].score = 0
    self.players[1].score = 0
    self.players[0].type = self.gui.selected_red_player_type.get()
    self.players[1].type = self.gui.selected_blue_player_type.get()
    self.players[0].symbol = self.gui.selected_red_move.get()
    self.players[1].symbol = self.gui.selected_blue_move.get()
    self.turn = self.players[0]
    self.gui.display_scores()
    self.gui.display_board()
    self.gui.show_stuff()
    self.recording = open(f'recordings/game_{datetime.datetime.now().strftime("%m%d%y%H%M%S")}.txt', 'a')
    self.recording.write(f'mode: {self.mode}, size: {self.board.size}\n')
    if(self.players[0].type == 'Computer'):
      self.computer_turn()

  def replay_game(self):
    self.gui.clear_board()
    self.gui.clear_message()
    try:
      self.recording = open(f"recordings/{self.gui.replay_entry.get()}")
    except:
      self.gui.display_message(f"Please enter a valid file name.")
      return
    self.mode, self.board.size = [part.split(": ")[1] for part in self.recording.readline().split(', ')]
    self.board.size = int(self.board.size)
    self.board.select_size(self.board.size)
    self.players[0].score = 0
    self.players[1].score = 0
    self.turn = self.players[0]
    self.players[0].type = 'Replay'
    self.players[1].type = 'Replay'
    self.gui.display_scores()
    self.gui.display_board()
    self.gui.show_stuff()
    self.replay_turn()

  def replay_turn(self):
    move = self.recording.readline().split(', ')
    if move[0] == '':
      return
    i = int(move[0])
    j = int(move[1])
    symbol = move[2][0]
    self.turn.change_symbol(symbol)
    self.place_move(i, j)

class sosBoard:
  def __init__(self, game, size):
    self.game = game
    self.size = size
    self.move_count = 0
    self.spaces = [[None for _ in range(self.size)] for _ in range(self.size)]

  def select_size(self, new_size):
    if new_size > 2:
      self.size = new_size
      self.spaces = [[None for _ in range(self.size)] for _ in range(self.size)]
      self.move_count = 0
    else:
      self.size = 8
      self.spaces = [[None for _ in range(self.size)] for _ in range(self.size)]
      self.game.gui.display_message("Error: Board size too small, must be 3 or more.")

  def set_move(self, i, j, symbol):
      self.spaces[i][j]['text'] = symbol.upper()
      self.move_count += 1

  def valid_move(self, i, j):
    return self.spaces[i][j]["text"] == ''

  def good_move(self, i, j, symbol):
    return self.detect_sos(i, j, symbol) >= 0

  def best_move(self):
    position = [0, 0]
    max_count = 0
    best_symbol = ''
    for i in range(self.size):
      for j in range(self.size):
        if(self.valid_move(i, j)):
          count_S = self.detect_sos(i, j, 'S')
          count_O = self.detect_sos(i, j, 'O')
          if (count_O > count_S):
            sos_count = count_O
            new_symbol = 'O'
          else:
            sos_count = count_S
            new_symbol = 'S'
          if(sos_count > max_count):
            max_count = sos_count
            position = [i, j]
            best_symbol = new_symbol
    return [position, max_count, best_symbol]

  def detect_sos(self, i, j, symbol):
    count = 0
    if symbol == 'O':
      if i > 0 and j > 0 and i < self.size - 1 and j < self.size - 1 and self.spaces[i + 1][j + 1]['text'] == 'S' and self.spaces[i - 1][j - 1]['text'] == 'S':
        count += 1
      if i > 0 and j > 0 and i < self.size - 1 and j < self.size - 1 and self.spaces[i + 1][j - 1]['text'] == 'S' and self.spaces[i - 1][j + 1]['text'] == 'S':
        count += 1
      if j > 0 and j < self.size - 1 and self.spaces[i][j + 1]['text'] == 'S' and self.spaces[i][j - 1]['text'] == 'S':
        count += 1
      if i > 0 and i < self.size - 1 and self.spaces[i + 1][j]['text'] == 'S' and self.spaces[i - 1][j]['text'] == 'S':
        count += 1
    if symbol == 'S':
      if i > 1 and j > 1 and i < self.size - 2 and j < self.size - 2 and self.spaces[i + 1][j + 1]['text'] == 'O' and self.spaces[i + 2][j + 2]['text'] == 'S':
        count += 1
      if j > 1 and i < self.size - 2 and self.spaces[i + 1][j - 1]['text'] == 'O' and self.spaces[i + 2][j - 2]['text'] == 'S':
        count += 1
      if j < self.size - 2 and self.spaces[i][j + 1]['text'] == 'O' and self.spaces[i][j + 2]['text'] == 'S':
        count += 1
      if i < self.size - 2 and self.spaces[i + 1][j]['text'] == 'O' and self.spaces[i + 2][j]['text'] == 'S':
        count += 1
      if i > 1 and j > 1 and self.spaces[i - 1][j - 1]['text'] == 'O' and self.spaces[i - 2][j - 2]['text'] == 'S':
        count += 1
      if i > 1 and j < self.size - 2 and self.spaces[i - 1][j + 1]['text'] == 'O' and self.spaces[i - 2][j + 2]['text'] == 'S':
        count += 1
      if j > 1 and self.spaces[i][j - 1]['text'] == 'O' and self.spaces[i][j - 2]['text'] == 'S':
        count += 1
      if i > 1 and self.spaces[i - 1][j]['text'] == 'O' and self.spaces[i - 2][j]['text'] == 'S':
        count += 1
    return count

  def detect_bad_move(self):
    if(False):
      True

  def is_board_full(self):
      return self.move_count >= self.size * self.size


def main():
  root = tk.Tk()
  game = sosGame(root)
  root.mainloop()

main()
