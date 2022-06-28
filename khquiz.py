# khquiz.py

import random
from string import ascii_lowercase

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS = {
    "Sora's original beta design was based off of what character": [
        "Mickey Mouse", "Cloud Strife", "Oswald the Lucky Rabbit", "Donald Duck"
    ],
    "What is the name of Kairi's nobody": [
        "Namine", "Kairix", "Larxene", "Krixia"
    ],
    "Which character has had three different voice actors": [
        "Master Xehanort", "Riku", "Marluxia", "Tron"
    ],
}

num_questions = min(NUM_QUESTIONS_PER_QUIZ, len(QUESTIONS))
questions = random.sample(list(QUESTIONS.items()), k=num_questions)

num_correct = 0
for num, (question, alternatives) in enumerate(questions, start=1):
    print(f"\nQuestion {num}:")
    print(f"{question}?")
    correct_answer = alternatives[0]
    labeled_alternatives = dict(
        zip(ascii_lowercase, random.sample(alternatives, k=len(alternatives)))
    )
    for label, alternative in labeled_alternatives.items():
        print (f"   {label}) {alternative}")

    while(answer_label := input("\nYour Answer? ")) not in labeled_alternatives:
        print(f"Invalid choice, please use one of the following: {', '.join(labeled_alternatives)}")

    answer = labeled_alternatives[answer_label]
    if answer == correct_answer:
        num_correct += 1
        print("Correct!")
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")

print(f"\nYou got {num_correct} correct out of {num} questions")