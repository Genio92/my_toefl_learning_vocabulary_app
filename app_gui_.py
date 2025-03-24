import sys
import pandas as pd
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QRadioButton, QGroupBox, QButtonGroup, QSpinBox
)
from PyQt5.QtGui import QFont

class VocabTrainer(QWidget):
    def __init__(self):
        super().__init__()

        # Load Excel File
        self.df = pd.read_excel("TOEFL_Vocabulary.xlsx")

        # UI Elements
        self.setWindowTitle("TOEFL Vocabulary Trainer")
        self.setGeometry(100, 100, 500, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("TOEFL Vocabulary Trainer")
        self.title_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.title_label)

        # Word Count Selection
        self.word_count_label = QLabel("How many words do you want to learn?")
        layout.addWidget(self.word_count_label)
        self.word_count_input = QSpinBox()
        self.word_count_input.setRange(1, len(self.df))
        layout.addWidget(self.word_count_input)

        # Starting Index Selection
        self.start_index_label = QLabel("Enter the starting index (0-based):")
        layout.addWidget(self.start_index_label)
        self.start_index_input = QSpinBox()
        self.start_index_input.setRange(0, len(self.df) - 1)
        layout.addWidget(self.start_index_input)

        # Start Button
        self.start_button = QPushButton("Start Learning")
        self.start_button.clicked.connect(self.start_quiz)
        layout.addWidget(self.start_button)

        # Word Display
        self.word_label = QLabel("")
        self.word_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.word_label)

        # Answer Choices
        self.group_box = QGroupBox("Select the correct Arabic meaning:")
        self.radio_layout = QVBoxLayout()
        self.button_group = QButtonGroup()

        self.radio_buttons = []
        for i in range(5):
            btn = QRadioButton("")
            self.radio_buttons.append(btn)
            self.button_group.addButton(btn, i)
            self.radio_layout.addWidget(btn)

        self.group_box.setLayout(self.radio_layout)
        layout.addWidget(self.group_box)

        # Submit Button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def start_quiz(self):
        num_words = self.word_count_input.value()
        start_index = self.start_index_input.value()
        end_index = min(start_index + num_words, len(self.df))

        self.words_subset = self.df.iloc[start_index:end_index].sample(frac=1).reset_index(drop=True)
        self.current_index = 0
        self.next_question()

    def next_question(self):
        for btn in self.radio_buttons:
            btn.setEnabled(True)  # Re-enable all buttons before a new question
        if self.current_index >= len(self.words_subset):
            QMessageBox.information(self, "Finished!", "You have completed the quiz!")
            return

        row = self.words_subset.iloc[self.current_index]
        self.correct_answer = row["Arabic Translation"]
        self.example_sentence = row["Example Sentence"]
        word = row["Word"]

        self.word_label.setText(f"What's the Arabic meaning of: {word}")

        # Get wrong answers
        wrong_options = self.df[self.df["Arabic Translation"] != self.correct_answer]["Arabic Translation"].tolist()
        wrong_choices = random.sample(wrong_options, min(4, len(wrong_options)))
        choices = wrong_choices + [self.correct_answer]
        random.shuffle(choices)

        # Assign answers to buttons
        for i, btn in enumerate(self.radio_buttons):
            btn.setText(choices[i])
            btn.setChecked(False)

    def check_answer(self):
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "No Selection", "Please select an answer!")
            return

        selected_text = self.radio_buttons[selected_id].text()
        if selected_text == self.correct_answer:
            QMessageBox.information(self, "Correct!", f"✅ Correct!\nExample: {self.example_sentence}")
            self.current_index += 1
            self.next_question()
        else:
            QMessageBox.warning(self, "Wrong!", "❌ Incorrect. Try again!")
            self.radio_buttons[selected_id].setDisabled(True)

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VocabTrainer()
    window.show()
    sys.exit(app.exec_())
