import pandas as pd
import random
from bidi.algorithm import get_display  # Fixes Arabic text display

# Load the vocabulary Excel file
df = pd.read_excel("TOEFL_Vocabulary.xlsx")

# Get user input for number of words and starting index
total_words = len(df)
print(f"The vocabulary list contains {total_words} words.")

while True:
    try:
        num_words = int(input("How many words do you want to learn? "))
        if num_words <= 0:
            print("Please enter a positive number.")
            continue
        start_index = int(input("Enter the starting index (0-indexed): "))
        if start_index < 0 or start_index >= total_words:
            print("Starting index out of range. Try again.")
            continue
        end_index = min(start_index + num_words, total_words)
        break
    except ValueError:
        print("Please enter valid integer values.")

# Slice the DataFrame for the chosen range and shuffle the order
words_subset = df.iloc[start_index:end_index].sample(frac=1, random_state=random.randint(0, 1000))

def ask_question(row, df_choices):
    correct = row["Arabic Translation"]
    correct_fixed = get_display(correct)  # Fix Arabic text display

    # Get wrong answers
    wrong_options = df_choices[df_choices["Arabic Translation"] != correct]["Arabic Translation"].tolist()
    wrong_choices = random.sample(wrong_options, min(4, len(wrong_options)))  # 4 wrong answers
    wrong_choices_fixed = [get_display(word) for word in wrong_choices]  # Fix Arabic text display
    
    choices = wrong_choices_fixed + [correct_fixed]
    random.shuffle(choices)
    return choices, correct_fixed

print("\nStarting the vocabulary quiz...\n")

for _, row in words_subset.iterrows():
    word = row["Word"]
    correct_answer = row["Arabic Translation"]
    example_sentence = row["Example Sentence"]

    choices, correct_fixed = ask_question(row, df)

    remaining_choices = choices.copy()
    answered_correctly = False

    while not answered_correctly:
        print(f"\nWhat is the Arabic translation for: '{word}'?")
        for i, option in enumerate(remaining_choices, 1):
            print(f"{i}. {option}")

        try:
            answer = int(input("Your choice (enter number): "))
            if answer < 1 or answer > len(remaining_choices):
                print("Invalid option. Please choose a valid number.")
                continue
        except ValueError:
            print("Please enter a number.")
            continue

        chosen = remaining_choices[answer - 1]
        if chosen == correct_fixed:
            print("✅ Correct!")
            print(f"Example Sentence: {example_sentence}")
            answered_correctly = True
        else:
            print("❌ Incorrect. Try again.")
            remaining_choices.pop(answer - 1)
            if len(remaining_choices) == 1:
                print(f"The correct answer was: {correct_fixed}")
                answered_correctly = True

    proceed = input("Do you want to proceed to the next word? (y/n): ").lower()
    if proceed not in ("y", "yes"):
        print("Exiting the quiz. Keep practicing!")
        break

print("Quiz completed!")
