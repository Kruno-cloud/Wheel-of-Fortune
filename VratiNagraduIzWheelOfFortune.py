import sys
from PyQt5.QtWidgets import QApplication
from Igranje_WheelOfFortune import Igranje
import WheelOfFortune  

def main():
    app = QApplication(sys.argv)
    igranje_window = Igranje(["player1", "player2"])  # Replace with your actual list of usernames
    igranje_window.show()

    # Call a function in pygame_script to retrieve the nagrada value
    nagrada = pygame_script.get_nagrada()

    # Use the retrieved nagrada value in your PyQt5 window
    igranje_window.process_nagrada(nagrada)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()