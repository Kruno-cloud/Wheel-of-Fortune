import sqlite3
import sys
import random
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Pojam import Pojam



class WheelOfFortune(QWidget):
    def __init__(self):
 
    def get_player_info(self):
        num_players, ok = QInputDialog.getInt(self, "Number of Players", "Enter the number of players:", 1, 1)
        if ok:
            players = []
            for i in range(num_players):
                player_name, ok = QInputDialog.getText(self, f"Player {i + 1}", f"Enter Player {i + 1}'s name:")
                if ok:
                    players.append({"name": player_name, "score": 0})
            self.play_game(players)
    def play_game(self, players):
        category = self.choose_category()
        word_to_guess = self.choose_word(category).lower()
        guessed_letters = []
        self.info_label.setText(f"Category: {category}")
        current_puzzle = self.display_puzzle(word_to_guess, guessed_letters)
        self.info_label.setText(current_puzzle)
        current_player = 0
        while current_puzzle != word_to_guess:
            guess, ok = QInputDialog.getText(self, f"{players[current_player]['name']}", "Guess a letter or the entire word:")
            if ok:
                if len(guess) == 1:
                    if guess in guessed_letters:
                        QMessageBox.information(self, "Invalid Guess", "You already guessed that letter!")
                    elif guess in word_to_guess:
                        guessed_letters.append(guess)
                        current_puzzle = self.display_puzzle(word_to_guess, guessed_letters)
                        self.info_label.setText(current_puzzle)
                    else:
                        current_player = (current_player + 1) % len(players)
                else:
                    if guess == word_to_guess:
                        QMessageBox.information(self, "Congratulations!", f"{players[current_player]['name']} guessed the word!")
                        players[current_player]['score'] += 1
                        break
                    else:
                        current_player = (current_player + 1) % len(players)
        self.show_results(players)
    def choose_category(self):
        categories = ["SPORT", "MITOLOGIJA", "NAŠI FILMOVI", "POVIJESNE FIGURE", "POSLOVICE", "AUTOMOBILI", "HOLLYWOODSKE ZVIJEZDE", "GAMING", "EUROPSKI GRADOVI"]
        category, ok = QInputDialog.getItem(self, "Choose a Category", "Select a category:", categories, 0, False)
        if ok:
            return category
    def choose_word(self, category):
        category_words = {
            "SPORT": ["soccer", "basketball", "tennis", "swimming", "volleyball"],
            "MITOLOGIJA": ["zeus", "poseidon", "apollo", "athena", "hercules"],
            "NAŠI FILMOVI": ["kokoška", "crna mamba", "dijete rosemary", "maratonci trče počasni krug"],
            "POVIJESNE FIGURE": ["albert einstein", "leonardo da vinci", "napoleon bonaparte", "cleopatra"],
            "POSLOVICE": ["where there's smoke there's fire", "better late than never", "actions speak louder than words"],
            "AUTOMOBILI": ["honda", "ford", "toyota", "chevrolet", "volkswagen"],
            "HOLLYWOODSKE ZVIJEZDE": ["brad pitt", "angelina jolie", "tom hanks", "scarlett johansson"],
            "GAMING": ["minecraft", "fortnite", "world of warcraft", "among us"],
            "EUROPSKI GRADOVI": ["paris", "london", "rome", "berlin", "prague"] #Baza
        }
        return random.choice(category_words[category])
    def display_puzzle(self, word, guesses):
        displayed_word = ""
        for letter in word:
            if letter in guesses:
                displayed_word += letter
            else:
                displayed_word += "_"
        return displayed_word
    def show_results(self, players):
        result_message = "Game Over!\nScores:\n"
        for player in players:
            result_message += f"{player['name']}: {player['score']}\n"
        self.result_display.setPlainText(result_message)
        self.result_display.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WheelOfFortune()
    window.show()
    sys.exit(app.exec_())

