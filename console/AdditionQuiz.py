import time

from mindcalc.quiz import AdditionQuiz, Difficulty


def main():
    print("Choose a difficulty level: 1 for EASY, 2 for MEDIUM, 3 for HARD")
    difficulty = int(input("Your choice: "))

    if difficulty == 1:
        quiz = AdditionQuiz(3, 2, Difficulty.EASY)
    elif difficulty == 2:
        quiz = AdditionQuiz(4, 2, Difficulty.MEDIUM)
    else:  # defaults to HARD if other values are entered
        quiz = AdditionQuiz(4, 2, Difficulty.HARD)

    total_time_correct = 0
    total_time_wrong = 0
    num_correct = 0
    num_wrong = 0

    for _ in range(10):
        num1, num2 = quiz.get_numbers()
        print(f"What is the sum of {num1} and {num2}?")
        start_time = time.time()
        user_answer = float(input("> "))
        end_time = time.time()
        is_correct = quiz.check_answer(user_answer, start_time, end_time)
        elapsed_time = end_time - start_time

        if is_correct:
            print("Correct!")
            num_correct += 1
            total_time_correct += elapsed_time
        else:
            print(f"Wrong answer. The correct answer is {quiz.correct_answer}")
            num_wrong += 1
            total_time_wrong += elapsed_time

    avg_time_correct = total_time_correct / num_correct if num_correct > 0 else 0
    avg_time_wrong = total_time_wrong / num_wrong if num_wrong > 0 else 0

    print(f"Results:\nCorrect answers: {num_correct}\n"
          f"Wrong answers: {num_wrong}\n"
          f"Average time for correct answers: {avg_time_correct}\n"
          f"Average time for wrong answers: {avg_time_wrong}")


if __name__ == "__main__":
    main()