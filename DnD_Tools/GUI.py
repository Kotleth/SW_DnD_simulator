import copy
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, \
    QPushButton, QDialog, QLabel, QComboBox, QCompleter, QTextBrowser, QHBoxLayout
from PySide6.QtCore import Signal, Slot, Qt

from additions import CharacterClassList
from character import UnitList, Unit
from generic_actions import start_battle

# units_by_id_dict: [int, Unit] = {}
team_even_dict: [int, Unit] = {}
team_odd_dict: [int, Unit] = {}
team_1_list = []
team_2_list = []
occupied_team_even_id = 0
occupied_team_odd_id = 1


class BattleWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.new_team1_mate = None
        self.new_team2_mate = None

        self.team_even: list[Unit] = []
        self.team_odd: list[Unit] = []

        self.setWindowTitle("Battle simulator")
        self.setGeometry(900, 100, 500, 900)

        layout = QVBoxLayout()

        # Create a dialog in the middle
        dialog = QDialog()
        dialog_layout = QVBoxLayout(dialog)

        self.battle_history = QTextBrowser(self)
        dialog_layout.addWidget(self.battle_history)
        self.battle_history.append("BATTLE STATUS:")

        dialog_buttons_layout = QHBoxLayout()

        # Team 1 append button
        append_member_team_1 = QPushButton("Append to team 1")
        dialog_buttons_layout.addWidget(append_member_team_1)
        append_member_team_1.clicked.connect(self.team_1_append)

        # Team 2 append button
        append_member_team_2 = QPushButton("Append to team 2")
        dialog_buttons_layout.addWidget(append_member_team_2)
        append_member_team_2.clicked.connect(self.team_2_append)

        dialog_layout.addLayout(dialog_buttons_layout)
        layout.addWidget(dialog)
        char_lists_layer = QHBoxLayout()

        # Combo box for choosing member for team
        self.team_combo = QComboBox()
        self.team_combo.addItems(list(UnitList.units_dict.keys()))

        start_battle_layout = QHBoxLayout()

        # Create button to start battle
        self.start_battle_button = QPushButton("Start battle")
        dialog_buttons_layout.addWidget(self.start_battle_button)
        self.start_battle_button.clicked.connect(self.start_battle)

        pop_buttons_layout = QHBoxLayout()

        # Team 1 remove button
        self.remove_member_team_1 = QPushButton("Pop Team Even")
        dialog_buttons_layout.addWidget(self.remove_member_team_1)
        self.remove_member_team_1.clicked.connect(self.pop_team_1)

        # Team 2 remove button
        self.remove_member_team_2 = QPushButton("Pop Team Odd")
        dialog_buttons_layout.addWidget(self.remove_member_team_2)
        self.remove_member_team_2.clicked.connect(self.pop_team_2)

        pop_buttons_layout.addWidget(self.remove_member_team_1)
        pop_buttons_layout.addWidget(self.remove_member_team_2)
        dialog_layout.addLayout(pop_buttons_layout)

        show_team_layout = QHBoxLayout()

        # Show teams
        self.show_teams_button = QPushButton("Show teams members")
        dialog_buttons_layout.addWidget(self.show_teams_button)
        self.show_teams_button.clicked.connect(self.show_team)

        char_lists_layer.addWidget(self.team_combo)
        dialog_layout.addLayout(char_lists_layer)

        show_team_layout.addWidget(self.show_teams_button)
        dialog_layout.addLayout(show_team_layout)

        start_battle_layout.addWidget(self.start_battle_button)
        dialog_layout.addLayout(start_battle_layout)

        self.setLayout(layout)

    def show_message(self, *messages):
        for message in messages:
            self.battle_history.append(message)

    def start_battle(self):
        battle_report_list = start_battle(team_even=self.team_even, team_odd=self.team_odd)
        self.battle_history.clear()
        self.show_message("\tBATTLE BEGINS!\n")
        print(battle_report_list)
        for message in battle_report_list:
            self.show_message(message)
        self.show_message("\n\tBATTLE ENDS!")
        [unit.long_rest() for unit in self.team_even + self.team_odd]

    def show_team(self):
        max_length = max(len(self.team_even), len(self.team_odd))
        _team_even = [unit.name for unit in self.team_even]
        _team_odd = [unit.name for unit in self.team_odd]

        # Pad the shorter list with None values
        _team_even += [''] * (max_length - len(_team_even))
        _team_odd += [''] * (max_length - len(_team_odd))
        self.battle_history.append(f"\nTeam even \t Team odd")
        for even_member, odd_member in zip(_team_even, _team_odd):
            self.battle_history.append(f"{even_member}\t{odd_member}")

    def pop_team_1(self):
        if team_even_dict:
            self.battle_history.append(f"Remove from Team Even: {team_even_dict.pop(max(team_even_dict.keys())).name}")
            self.team_even.pop()
        else:
            self.battle_history.append("Team Even is empty!")

    def pop_team_2(self):
        if team_odd_dict:
            self.battle_history.append(f"Remove from Team Odd: {team_odd_dict.pop(max(team_odd_dict.keys())).name}")
            self.team_odd.pop()
        else:
            self.battle_history.append("Team Odd is empty!")

    def team_1_choose(self, index):
        self.new_team1_mate = self.team_combo.itemText(index)
        print(f"Selected item: {self.new_team1_mate}")

    def team_1_append(self):
        global occupied_team_even_id
        new_unit = copy.copy(UnitList.units_dict[self.team_combo.currentText()])
        self.team_even.append(new_unit)
        team_even_dict[occupied_team_even_id] = new_unit
        new_unit.unit_id = occupied_team_even_id
        self.battle_history.append(f"\nAdded to Team Even:\nId: {occupied_team_even_id}\tName: {team_even_dict[occupied_team_even_id].name}")
        team_1_list.append(occupied_team_even_id)
        occupied_team_even_id += 2

    def team_2_append(self):
        global occupied_team_odd_id
        new_unit = copy.copy(UnitList.units_dict[self.team_combo.currentText()])
        self.team_odd.append(new_unit)
        team_odd_dict[occupied_team_odd_id] = new_unit
        new_unit.unit_id = occupied_team_odd_id
        self.battle_history.append(f"\nAdded to Team Odd:\nId: {occupied_team_odd_id}\tName: {team_odd_dict[occupied_team_odd_id].name}")
        team_2_list.append(occupied_team_odd_id)
        occupied_team_odd_id += 2


class CharacterWindow(QDialog):

    character_pass = Signal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Character creation")
        self.setGeometry(500, 100, 400, 300)

        layout = QVBoxLayout()

        # Create 9 text input boxes
        char_stats = ['NAME', 'CLASS', 'LVL', 'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        self.text_inputs = []
        for i in range(9):
            label = QLabel(char_stats[i], self)
            if i in range(2, 10):
                text_input = QComboBox(self)
                self.text_inputs.append(text_input)
                layout.addWidget(label)
                layout.addWidget(text_input)
                if char_stats[i] == 'LVL':
                    for j in range(1, 21):
                        text_input.addItem(str(j))
                else:
                    for j in range(1, 31):
                        text_input.addItem(str(j))
                    text_input.setCurrentText(str(10))
                text_input.setFixedWidth(100)
                text_input.setFixedHeight(30)
            else:
                text_input = QLineEdit(self)
                if i == 1:
                    class_completer = QCompleter(CharacterClassList.character_classes_dict.keys())
                    class_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
                    text_input.setCompleter(class_completer)
                self.text_inputs.append(text_input)
                layout.addWidget(label)
                layout.addWidget(text_input)
                text_input.setFixedWidth(200)
                text_input.setFixedHeight(30)

        button = QPushButton("Create", self)
        button.clicked.connect(self.character_create)
        layout.addWidget(button)

        self.setLayout(layout)

    def character_create(self):
        if self.text_inputs[1].text().lower() in CharacterClassList.character_classes_dict.keys():
            self.character_pass.emit([x.text() if type(x) == QLineEdit else x.currentText() for x in self.text_inputs])
        else:
            window.action_browser.append(f"No such class as {self.text_inputs[1].text().lower().title()}")
            print(f"No such class as {self.text_inputs[1].text().lower().title()}")


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_received = []
        self.char_creation_window = None
        self.battle_window = None

        self.setWindowTitle("D&D Simulator")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create a button to open the side window
        open_button = QPushButton("Open Character Creation", self)
        open_button.clicked.connect(self.open_character_creation)
        layout.addWidget(open_button)
        self.action_browser = QTextBrowser(self)
        layout.addWidget(self.action_browser)

        self.log_button = QPushButton("Open Battle Simulator", self)
        self.log_button.clicked.connect(self.log_action)
        layout.addWidget(self.log_button)

        central_widget.setLayout(layout)

    def open_character_creation(self):
        self.action_browser.append("Opened character creation")
        self.char_creation_window = CharacterWindow()
        self.char_creation_window.character_pass.connect(self.receive_character)
        self.char_creation_window.show()

    def log_action(self):
        self.action_browser.append("It's time to D-D-D-D-D-D-D-D-D-Duel!!!")
        self.battle_window = BattleWindow()
        self.battle_window.show()

    def receive_character(self, character_description):
        self.data_received = character_description
        CharacterClassList.character_classes_dict[self.data_received[0]] = self.data_received
        self.action_browser.append(f"Created a character named: {self.data_received[0]}")


def open_app():
    # TODO temporary solution.
    global window
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
