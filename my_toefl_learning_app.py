import pandas as pd
import random

# Load the vocabulary Excel file
# Make sure TOEFL_Vocabulary.xlsx is in your working directory
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
        # Make sure we don't exceed list length
        end_index = min(start_index + num_words, total_words)
        break
    except ValueError:
        print("Please enter valid integer values.")

# Slice the DataFrame for the chosen range and shuffle the order
words_subset = df.iloc[start_index:end_index].sample(frac=1, random_state=random.randint(0, 1000))

def ask_question(row, df_choices):
    correct = row["Arabic Translation"]
    # Build list of wrong answers (exclude correct answer)
    wrong_options = df_choices[ df_choices["Arabic Translation"] != correct ]["Arabic Translation"].tolist()
    # If there are less than 4 available wrong options, use all
    num_wrong_needed = 4
    wrong_choices = random.sample(wrong_options, min(num_wrong_needed, len(wrong_options)))
    choices = wrong_choices + [correct]
    random.shuffle(choices)
    return choices

print("\nStarting the vocabulary quiz...\n")

# Use the full dataset (or you can use words_subset) as pool for wrong answers
for index, row in words_subset.iterrows():
    word = row["Word"]
    correct_answer = row["Arabic Translation"]
    example_sentence = row["Example Sentence"]
    
    # Prepare the initial set of choices
    choices = ask_question(row, df)
    # Keep track of which choices have been eliminated if answer is wrong.
    remaining_choices = choices.copy()
    
    answered_correctly = False
    while not answered_correctly:
        print(f"\nWhat is the Arabic translation for the word: '{word}'?")
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
        if chosen == correct_answer:
            print("Correct!")
            print(f"Example Sentence: {example_sentence}")
            answered_correctly = True
        else:
            print("Incorrect.")
            # Remove the wrong choice
            remaining_choices.pop(answer - 1)
            if len(remaining_choices) == 0:
                # Safety fallback; should not occur since correct remains in list
                print("No choices left. The correct answer was:", correct_answer)
                answered_correctly = True
            else:
                print("Please try again. Remaining choices:")
    
    # Ask if user wants to proceed to the next word
    proceed = input("Do you want to proceed to the next word? (y/n): ").lower()
    if proceed not in ("y", "yes"):
        print("Exiting the quiz. Good luck with your studies!")
        break

print("Quiz completed!")
