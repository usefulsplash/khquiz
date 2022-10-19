# khquiz.py

import re
import sys
import random
from string import ascii_lowercase
import pathlib

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 10
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"


def run_quiz():
    questions = prep_questions(QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ)
    hardmode = 0
    if sys.argv[1] == "--hardmode":
        hardmode = 1
    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        if hardmode:
            num_correct += ask_hardmode(question)
        else:
            num_correct += ask_question(question)

    print(f"\nYou got {num_correct} correct out of {num} questions")


# preprocessing -> preps QUESTIONS data structure to use for main loop
def prep_questions(path, num_questions):
    questions = tomllib.loads(path.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)


# randomizes choices, calls get_answer for user input, then checks if they are correct or not
def ask_question(question):
    correct_answers = question["answers"]
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answer = get_answers(
        question=question["question"],
        alternatives=ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    if correct := (set(answer) == set(correct_answers)):
        print("Correct!")
        if "explanation" in question:
            print(f"\nEXPLANATION:\n{question['explanation']}")
    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answers))

    return correct

# in hardmode there is no multiple choice prompt
def ask_hardmode(question):
    correct_answer = question["answers"]
 
    print(question["question"] + "?")
    answer = input(f"\nYour answer: ")

    if(len(correct_answer) > 1):   
        answer = re.split(' |& |, | and', answer)
    else: 
        answer = [answer] # convert answer from str to list with one item

    if answer == correct_answer:
        print("Correct!")
        if "explanation" in question:
            print(f"\nEXPLANATION:\n{question['explanation']}")
        return True
    else:
        is_or_are = " is" if len(correct_answer) == 1 else "s are"
        print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answer))
    return False


# accepts question text and its choices, labels them, then returns user's answer
def get_answers(question, alternatives, num_choices=1, hint=None):
    print(f"{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    if hint:
        labeled_alternatives["?"] = "Hint"

    for label, alternative in labeled_alternatives.items():
        print(f"    {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        answer = input(f"\nYour answer{plural_s}: ")
        answers = set(answer.replace(",", " ").split())

        # handles hints
        if hint and "?" in answers:
            print(f"\nHINT: {hint}")
            continue

        # handles invalid answers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any((invalid := answer) not in labeled_alternatives for answer in answers):
            print(
                f"{invalid!r} is not a valid choice. "
                f"Please use {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers]


if __name__ == "__main__":
    run_quiz()
