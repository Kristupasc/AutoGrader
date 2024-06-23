

class ExamExample:
    """
    Class that can be copy pasted when creating a new exam. This is a foundation. For each question, you should
    create a method that will grade the question. The method should take a grading object as an argument. The grading
    object is used to check the student's code. The grading object has a method for each criterion that you want to check.
    The method should return the points that the student should get for that criterion. The grading object also has a
    feedback attribute that you can use to provide more detailed feedback to the student. The feedback should be a list
    of strings. The feedback will be displayed to the student if the student's code does not pass the criterion.
    The function should be named: question_<number> where <number> is the number of the question.
    """
    def __init__(self):
        self.points = {}
        self.feedback = {}

    def question_5(self, grader):
        feedback = [] # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0

        # save both the points and the feedback
        self.points[5] = points
        self.feedback[5] = feedback

    def question_6(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0

        # save both the points and the feedback
        self.points[6] = points
        self.feedback[6] = feedback

    def question_7(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0

        # save both the points and the feedback
        self.points[7] = points
        self.feedback[7] = feedback

    def question_8(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0

        # save both the points and the feedback
        self.points[8] = points
        self.feedback[8] = feedback

    def question_9(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0

        # save both the points and the feedback
        self.points[9] = points
        self.feedback[9] = feedback

    def question_10(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check
        points = 0


        # save both the points and the feedback
        self.points[10] = points
        self.feedback[10] = feedback


