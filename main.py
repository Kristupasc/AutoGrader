from exam_2023_1 import Exam2023
from run_grader import RunGrader


def run_grader():
    """
    Runs the grader. Change the file path to the data file to run the grader for a different exam.
    The questions list may also differ.
    """
    file = "data/2023-10-20 ICS-Test3-Opp1 (2023.1) solutions and results per question per candidate.xlsx"
    g = RunGrader(file, Exam2023, [5, 6, 7, 8, 9, 10])
    g.begin()
    g.grade()
    g.process_results()
    g.export_results()
    return g


g = run_grader()
