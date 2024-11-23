import tkinter as tk

class GameGUI:
  def __init__(self, game, root):
    self.game = game
    self.root = root
    self.root.title("SOS Game")


    self.create_window()

  def create_window(self):
    self.selected_mode = tk.StringVar(value="Simple")

    self.mode_label = tk.Label(self.root, text="Mode:")
    self.mode_label.grid(row=1, column=0)
    self.simple_radio = tk.Radiobutton(self.root, text="Simple", variable=self.selected_mode, value="Simple", command=self.game.select_mode)
    self.simple_radio.grid(row=1, column=1)
    self.general_radio = tk.Radiobutton(self.root, text="General", variable=self.selected_mode, value="General", command=self.game.select_mode)
    self.general_radio.grid(row=1, column=2)

    self.board_size_label = tk.Label(self.root, text="Board size:")
    self.board_size_label.grid(row=2, column=0)
    self.board_size_entry = tk.Entry(self.root, width=3)
    self.board_size_entry.grid(row=2, column=1)
    self.board_size_button = tk.Button(self.root, text="New Game", command=self.game.create_new_game)
    self.board_size_button.grid(row=2, column=2)

    self.state_label = tk.Label(self.root, text=f"Mode: {self.game.mode}, size: {self.game.board.size}")
    self.state_label.grid(row=3, column=0, columnspan=2)
    self.player_label = tk.Label(self.root, text=f"Player: {self.game.turn.color}")
    self.player_label.grid(row=3, column=2)

    self.selected_red_move = tk.StringVar(value="S")
    self.selected_red_player_type = tk.StringVar(value="Human")
    self.red_label = tk.Label(self.root, text="Red:")
    self.red_label.grid(row=4, column=0)
    self.red_human_radio = tk.Radiobutton(self.root, text="Human", variable=self.selected_red_player_type, value="Human", command=self.update_red_player_type)
    self.red_human_radio.grid(row=4, column=1)
    self.red_comp_radio = tk.Radiobutton(self.root, text="Computer", variable=self.selected_red_player_type, value="Computer", command=self.update_red_player_type)
    self.red_comp_radio.grid(row=4, column=2)
    self.red_s_radio = tk.Radiobutton(self.root, text="S", variable=self.selected_red_move, value="S", command=self.update_red_symbol)
    self.red_s_radio.grid(row=5, column=1)
    self.red_o_radio = tk.Radiobutton(self.root, text="O", variable=self.selected_red_move, value="O", command=self.update_red_symbol)
    self.red_o_radio.grid(row=5, column=2)

    self.selected_blue_move = tk.StringVar(value="S")
    self.selected_blue_player_type = tk.StringVar(value="Human")
    self.blue_label = tk.Label(self.root, text="Blue:")
    self.blue_label.grid(row=6, column=0)
    self.blue_human_radio = tk.Radiobutton(self.root, text="Human", variable=self.selected_blue_player_type, value="Human", command=self.update_blue_player_type)
    self.blue_human_radio.grid(row=6, column=1)
    self.blue_comp_radio = tk.Radiobutton(self.root, text="Computer", variable=self.selected_blue_player_type, value="Computer", command=self.update_blue_player_type)
    self.blue_comp_radio.grid(row=6, column=2)
    self.blue_s_radio = tk.Radiobutton(self.root, text="S", variable=self.selected_blue_move, value="S", command=self.update_blue_symbol)
    self.blue_s_radio.grid(row=7, column=1)
    self.blue_o_radio = tk.Radiobutton(self.root, text="O", variable=self.selected_blue_move, value="O", command=self.update_blue_symbol)
    self.blue_o_radio.grid(row=7, column=2)

    self.message_label = tk.Label(self.root, text="")
    self.message_label.grid(row=8, column=0, columnspan=3)

    self.red_score_label = tk.Label(self.root, text=f"Red: {self.game.players[0].score}")
    self.red_score_label.grid(row=9, column=0)
    self.blue_score_label = tk.Label(self.root, text=f"Blue: {self.game.players[1].score}")
    self.blue_score_label.grid(row=9, column=1)

    self.replay_label = tk.Label(self.root, text="Replay file name:")
    self.replay_label.grid(row=10, column=0)
    self.replay_entry = tk.Entry(self.root, width=20)
    self.replay_entry.grid(row=10, column=1)
    self.replay_button = tk.Button(self.root, text="Replay", command=self.game.replay_game)
    self.replay_button.grid(row=10, column=2)

    self.display_board()

  def show_stuff(self):
    self.state_label.config(text=f"Mode: {self.game.mode}, size: {self.game.board.size}")

  def display_turn(self):
    self.player_label.config(text=f"Player: {self.game.turn.color}")

  def display_scores(self):
    self.red_score_label.config(text=f"Red: {self.game.players[0].score}")
    self.blue_score_label.config(text=f"Blue: {self.game.players[1].score}")

  def display_message(self, message):
    self.message_label.config(text=f"{message}")

  def clear_message(self):
    self.message_label.config(text=f"")

  def display_board(self):
    for i in range(self.game.board.size):
      for j in range(self.game.board.size):
        button = tk.Button(self.root, text ="", width=3, height=1, command=lambda i=i, j=j: self.game.place_move(i, j))
        button.grid(row=i, column=j+3)
        self.game.board.spaces[i][j] = button

  def clear_board(self):
    for i in range(self.game.board.size):
      for j in range(self.game.board.size):
        self.game.board.spaces[i][j].destroy()

  def update_red_symbol(self):
    self.game.players[0].change_symbol(self.selected_red_move.get())
  def update_blue_symbol(self):
    self.game.players[1].change_symbol(self.selected_blue_move.get())
  def update_red_player_type(self):
    self.game.players[0].change_type(self.selected_red_player_type.get())
  def update_blue_player_type(self):
    self.game.players[1].change_type(self.selected_blue_player_type.get())
