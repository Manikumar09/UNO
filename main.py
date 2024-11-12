import random
import tkinter as tk
from tkinter import messagebox

# Constants
COLORS = ["Red", "Yellow", "Green", "Blue"]
SPECIAL_CARDS = ["+2", "Reverse", "Skip"]
WILD_CARDS = ["Wild", "+4"]

# Card structure
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}" if self.color else f"{self.value}"

# Deck setup
def create_deck():
    deck = []
    # Add number cards (0-9 twice for each color)
    for color in COLORS:
        for number in range(10):
            deck.append(Card(color, str(number)))
            if number != 0:
                deck.append(Card(color, str(number)))  # Two copies of each number except 0
        # Add special cards
        for special in SPECIAL_CARDS:
            deck.append(Card(color, special))
            deck.append(Card(color, special))  # Two copies of each special card

    # Add wild cards
    for wild in WILD_CARDS:
        for _ in range(4):  # Four of each wild card
            deck.append(Card(None, wild))

    random.shuffle(deck)
    return deck

class UNOGame:
    def __init__(self, root):
        self.root = root
        self.root.title("UNO Game")
        self.deck = create_deck()
        self.players = []
        self.current_card = None
        self.direction = 1
        self.turn = 0
        self.num_players = tk.IntVar()

        # Game setup UI
        self.setup_frame = tk.Frame(root)
        self.setup_frame.pack()
        
        tk.Label(self.setup_frame, text="Enter the number of players:").pack()
        self.player_entry = tk.Entry(self.setup_frame, textvariable=self.num_players)
        self.player_entry.pack()
        self.start_button = tk.Button(self.setup_frame, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        # Initialize players
        try:
            num_players = int(self.num_players.get())
            if num_players < 2:
                raise ValueError("At least 2 players are required.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return
        
        self.players = [{"name": f"Player {i+1}", "hand": []} for i in range(num_players)]
        
        # Deal cards
        for player in self.players:
            player["hand"].extend(self.draw_cards(7))
        
        # Set the initial card
        self.current_card = self.deck.pop()
        while self.current_card.value in WILD_CARDS:
            self.deck.insert(0, self.current_card)
            self.current_card = self.deck.pop()

        # Hide setup UI and initialize the main game UI
        self.setup_frame.pack_forget()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        
        # Display current card
        self.current_card_label = tk.Label(self.main_frame, text=f"Current Card: {self.current_card}")
        self.current_card_label.pack()

        # Show player’s hand
        self.show_player_hand()

    def draw_cards(self, num):
        cards = []
        for _ in range(num):
            if self.deck:
                cards.append(self.deck.pop())
            else:
                messagebox.showinfo("UNO", "Deck is out of cards!")
        return cards

    def show_player_hand(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        player = self.players[self.turn]
        tk.Label(self.main_frame, text=f"{player['name']}'s Turn. Your Hand:").pack()
        
        # Display each card as a button
        for index, card in enumerate(player["hand"], start=1):
            button = tk.Button(self.main_frame, text=f"{card} ({index})", command=lambda c=card: self.play_card(c))
            button.pack()

        # Draw button if no playable cards
        tk.Button(self.main_frame, text="Draw Card", command=self.draw_card).pack()

        # Update current card display
        self.current_card_label = tk.Label(self.main_frame, text=f"Current Card: {self.current_card}")
        self.current_card_label.pack()

    def play_card(self, card):
        player = self.players[self.turn]

        if card.color == self.current_card.color or card.value == self.current_card.value or card.color is None:
            player["hand"].remove(card)
            self.current_card = card
            self.handle_special_card(card)

            # Check for win condition
            if not player["hand"]:
                messagebox.showinfo("UNO", f"{player['name']} has won the game!")
                self.root.quit()
            else:
                # Proceed to next player
                self.next_turn()
        else:
            messagebox.showerror("Invalid Move", "You cannot play this card.")

    def draw_card(self):
        player = self.players[self.turn]
        player["hand"].extend(self.draw_cards(1))
        self.next_turn()

    def handle_special_card(self, card):
        next_player = self.players[(self.turn + self.direction) % len(self.players)]
        if card.value == "+2":
            next_player["hand"].extend(self.draw_cards(2))
            messagebox.showinfo("UNO", f"{next_player['name']} draws 2 cards!")
        elif card.value == "+4":
            next_player["hand"].extend(self.draw_cards(4))
            self.current_card.color = random.choice(COLORS)
            messagebox.showinfo("UNO", f"{next_player['name']} draws 4 cards! Color changed to {self.current_card.color}")
        elif card.value == "Reverse":
            self.direction *= -1
            messagebox.showinfo("UNO", "Play direction reversed!")
        elif card.value == "Skip":
            messagebox.showinfo("UNO", f"{next_player['name']} is skipped!")
            self.turn = (self.turn + self.direction) % len(self.players)

    def next_turn(self):
        self.turn = (self.turn + self.direction) % len(self.players)
        self.show_player_hand()

# Run the game
root = tk.Tk()
game = UNOGame(root)
root.mainloop()
