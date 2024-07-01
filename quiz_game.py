import random

# Determing questions of every level
questions = {
    "easy": [
        {"question": "What is the capital of Italy?", "answer": "Rome"},
        {"question": "What is 3 + 5?", "answer": "8"},
        {"question": "What is the primary color of a banana?", "answer": "Yellow"},
        {"question": "What animal is known as man's best friend?", "answer": "Dog"},
        {"question": "What is the capital of Canada?", "answer": "Ottawa"},
        {"question": "How many continents are there on Earth?", "answer": "7"}
    ],
    "medium": [
        {"question": "What is the smallest planet in our solar system?", "answer": "Mercury"},
        {"question": "Who wrote 'Pride and Prejudice'?", "answer": "Jane Austen"},
        {"question": "What is the square root of 81?", "answer": "9"},
        {"question": "What is the chemical symbol for silver?", "answer": "Ag"},
        {"question": "Who painted 'Starry Night'?", "answer": "Vincent van Gogh"},
        {"question": "What is the capital of Brazil?", "answer": "Brasília"}
    ],
    "hard": [
        {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"},
        {"question": "Who developed the laws of motion?", "answer": "Isaac Newton"},
        {"question": "What is the integral of 2x?", "answer": "x^2 + C"},
        {"question": "What is the capital of Switzerland?", "answer": "Bern"},
        {"question": "Who wrote 'War and Peace'?", "answer": "Leo Tolstoy"},
        {"question": "What is the acceleration due to gravity on Earth?", "answer": "9.8 m/s^2"}
    ]
}
# function to select the difficulty level
def difficulty_level():
    while True:
        difficulty = input("Select difficulty (easy, medium, hard): ").lower()
        if difficulty in questions:
            return difficulty
        else:
            print("Invalid difficulty level. Please choose again.")
# function to ask the questions 
def questioning(question_data):
    question = question_data["question"]
    answer = question_data["answer"]
    user_answer = input(f"{question} ")
    
    if user_answer.strip().lower() == answer.strip().lower():
        print("Correct!")
        return True
    else:
        print(f"Incorrect! The correct answer was {answer}.")
        return False
# function to play the quiz game
def quiz_play():
    print("Welcome to the Quiz Game!")
    score = 0
    difficulty = difficulty_level()
    selected_questions = questions[difficulty]
    random.shuffle(questions)

    for question_data in questions:
        if questioning(question_data):
            score += 1

    print(f"Game over! Your final score is: {score} out of {len(selected_questions)}")

if __name__ == "__main__":
    quiz_play()
