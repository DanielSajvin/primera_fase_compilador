import sys
from PyQt5.QtWidgets import QApplication
from lexer import MainMenuPrincipal  # Importar la clase desde lexer.py


def main():
    app = QApplication(sys.argv)
    window = MainMenuPrincipal()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
