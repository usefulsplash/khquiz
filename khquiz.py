# khquiz.py

import random
from string import ascii_lowercase

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS = {
    "Sora's original beta design was based off of what character": [
        "Mickey Mouse",
        "Cloud Strife",
        "Oswald the Lucky Rabbit",
        "Donald Duck",
    ],
    "What is the name of Kairi's nobody": ["Namine", "Kairix", "Larxene", "Krixia"],
    "Which character has had three different voice actors": [
        "Master Xehanort",
        "Riku",
        "Marluxia",
        "Tron",
    ],
}


def run_quiz():
    questions = prep_questions(QUESTIONS, num_questions=NUM_QUESTIONS_PER_QUIZ)

    num_correct = 0
    for num, (question, alternatives) in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_question(question, alternatives)

    print(f"\nYou got {num_correct} correct out of {num} questions")


# preprocessing -> preps QUESTIONS data structure to use for main loop
def prep_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions.items()), k=num_questions)


# randomizes choices, calls get_answer for user input, then checks if they are correct or not
def ask_question(question, alternatives):
    correct_answer = alternatives[0]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answer = get_answer(question, ordered_alternatives)
    if answer == correct_answer:
        print("Correct!")
        return 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")
        return 0


# accepts question text and its choices, labels them, then returns user's answer
def get_answer(question, alternatives):
    print(f"{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    for label, alternative in labeled_alternatives.items():
        print(f"    {label}) {alternative}")

    while (answer_label := input("\nYour Answer: ")) not in labeled_alternatives:
        print(
            f"Invalid choice, please use one of the following: {', '.join(labeled_alternatives)}"
        )

    return labeled_alternatives[answer_label]


if __name__ == "__main__":
    run_quiz()
