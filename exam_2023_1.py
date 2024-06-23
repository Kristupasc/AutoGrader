

class Exam2023:
    def __init__(self):
        self.points = {}
        self.feedback = {}

    def question_5(self, grader):
        feedback = [] # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        # boolean to simply check if a point was given to avoid a lot of else statements for the feedback
        points_given = False

        points = 0
        # Check for emptiness (0.5p)
        empty_list = grader.run_code_on_input([[]])
        if empty_list is None:
            points += 0.5
            feedback.append("Code correctly handles empty lists (0.5p).")
        else:
            feedback.append("Code does not handle empty lists correctly (0p).")

        # Check for invalid types in the list (0.5p)
        if grader.statement_includes('if', 'isinstance'):
            invalid_types = grader.run_code_on_input([[1, 2.3, "str", 4]])
            if invalid_types is None:
                points += 0.5
                feedback.append("Code correctly handles invalid types in the list (0.5p).")
            else:
                feedback.append("Code does not handle invalid types in the list correctly (0p).")
        else:
            feedback.append("Code does not check for invalid types in the list (0p).")

        # if both validations are present, award extra 0.5p
        if points == 1:
            points += 0.5
            feedback.append("Code correctly handles both empty lists and invalid types in the list (0.5p).")
        else:
            feedback.append("Code does not handle both empty lists and invalid types in the list correctly (0p).")

        # CRITERION 2
        # Check if the code returns the correct output for a sample input
        sample_input = [[1, 2, 3, "a", "b", "c", 4, 5, 6]]
        expected_output = (['a', 'b', 'c'], [1, 2, 3, 4, 5, 6])
        # also, an expected output can be flipped
        expected_output_alt = ([1, 2, 3, 4, 5, 6], ['a', 'b', 'c'])
        sample_input2 = [["1", 2, 3, "2", 4, 5, 6, "d", 7, "8"]]
        expected_output2 = (['1', '2', 'd', '8'], [2, 3, 4, 5, 6, 7])
        expected_output2_alt = ([2, 3, 4, 5, 6, 7], ['1', '2', 'd', '8'])
        # check if the students code is correct. If it is, award 3.5 points
        if ((grader.check_single_output(sample_input, expected=expected_output) or
             grader.check_single_output(sample_input, expected=expected_output_alt))
                and (grader.check_single_output(sample_input2, expected=expected_output2) or
                     grader.check_single_output(sample_input2, expected=expected_output2_alt))):
            points += 3.5
            feedback.append("Code correctly separates the list into two sublists (3.5p).")
        else:
            feedback.append("Code does not correctly separate the list into two sublists. Checking individual cases.")
            # if it is not correct, check for each case
            # case1: for loop correctly check if elements are of type str or int to add into sublists
            # we first get the body of the if statement in the for loop
            for_has_if, for_if_body = grader.body_includes('for', 'if')
            if for_has_if:
                # if that if statement exists, check if it correctly checks for str or int
                if grader.statement_includes('if', 'isinstance', body=for_if_body):
                    if grader.statement_includes('if', 'str', body=for_if_body):
                        if grader.statement_includes('if', 'int', body=for_if_body):
                            points += 1
                            points_given = True
                            feedback.append("Code correctly checks if elements are of type str or int (1p).")
            if not points_given:
                feedback.append("Code does not correctly check if elements are of type str or int (0p).")
            points_given = False
            # case2: check if the code correctly appends the elements into the sublists
            for_append, for_append_body = grader.body_includes('for', 'append')
            # we check this by looking if the for loop body has two append statements
            if for_append:
                for_append_body = grader.convert_body_to_string(for_append_body[0])
                if for_append_body.count('append') > 1:
                    points += 1
                    points_given = True
                    feedback.append("Code correctly appends elements into the sublists (1p).")
            if not points_given:
                feedback.append("Code does not correctly append elements into the sublists (0p).")
            points_given = False

            simple_input = [[1, "str"]]
            result = grader.run_code_on_input(simple_input)
            try:
                # case3: check if the result is a tuple
                if isinstance(result, tuple):
                    points += 1
                    feedback.append("Code correctly returns a tuple (1p).")
                elif result is not None:
                    # if the result is a nested list, give 0.5p
                    if isinstance(result[0], list) and isinstance(result[1], list):
                        points += 0.5
                        feedback.append("Code returns a nested list instead of a tuple (0.5p out of 1p).")
            except Exception:
                # if something went wrong with getting the result, don't give points
                feedback.append("Code does not return a tuple (0p).")
                pass

        # save both the points and the feedback
        self.points[5] = points
        self.feedback[5] = feedback

    def question_6(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0
        # outputs can also be in a list of lists, where the first element is the input and the second is the expected output
        # this is useful if you want to check multiple test cases
        # to put the output for the tester, use grader.set_output(outputs).
        # to initiate the check, use grader.begin_output_analysis()
        outputs = [
            [[], None],
            [[1, 2, "wrong", 4], None],
            [[1, 2, 3, 4], 2],
            [[1, 2, 3, 10], 1]
        ]
        if (grader.body_includes('if', 'print') and grader.body_includes('if', 'return')) or (
                grader.body_includes('else', 'print') and grader.body_includes('else', 'return')):
            points += 0.5
            feedback.append("Code correctly prints and returns the result (0.5p).")
        else:
            feedback.append("Code does not correctly print and return the result (0p).")

        if grader.statement_includes('if', 'isinstance'):
            points += 0.5
            feedback.append("Code correctly checks for invalid types (0.5p).")
        else:
            feedback.append("Code does not correctly check for invalid types (0p).")
        if points == 1:
            points += 0.5
            feedback.append("Code correctly checks for invalid types and prints and returns the result (0.5p).")
        else:
            feedback.append("Code does not correctly check for invalid types and print and return the result (0p).")
        grader.set_output(outputs)
        if grader.begin_output_analysis():
            points += 4
            feedback.append("Code correctly calculates the number of elements above the average (4p).")
        else:
            outputs = [
                [[1, 2, 3, 10], 1]  # a simple check if the above average elements can be indeed calculated
            ]
            grader.set_output(outputs)
            if grader.begin_output_analysis():
                points += 3.5
                feedback.append("Code correctly calculates the number of elements above the average (3.5p).")
            else:
                feedback.append("Code does not correctly calculate the number of elements above the average (0p).")

        # save both the points and the feedback
        self.points[6] = points
        self.feedback[6] = feedback

    def question_7(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0
        #Criterion 1
        # check if the code correctly handles invalid types
        if grader.statement_includes('if', 'isinstance') and grader.statement_includes('if', 'str'):
            points += 0.5
            feedback.append("Code correctly checks for invalid types (0.5p).")
        else:
            feedback.append("Code does not correctly check for invalid types (0p).")
        # check if the code correctly handles empty lists
        if grader.run_code_on_input([""]) is None:
            points += 0.5
            feedback.append("Code correctly handles empty strings (0.5p).")
        else:
            feedback.append("Code does not correctly handle empty strings (0p).")
        # check if the code correctly handles lists with one element
        if grader.run_code_on_input(["One"]) is None:
            points += 0.5
            feedback.append("Code correctly handles lists with one element (0.5p).")
        else:
            feedback.append("Code does not correctly handle lists with one element (0p).")
        # check if the code correctly handles all three cases, award extra 0.5p
        if points == 1.5:
            points += 0.5
            feedback.append("Code correctly handles invalid types, empty strings, and lists with one element (0.5p).")
        else:
            feedback.append("Code does not correctly handle invalid types, empty strings, and lists with one element (0p).")

        #Criterion 2
        # check if the code correctly reverses a sentence with more than one word
        sample_input = ["Hello this is a Test"]
        expected_output = ["Test", "a", "is", "this", "Hello"]
        actual_output = grader.run_code_on_input(sample_input)
        if actual_output == expected_output:
            points += 4
            feedback.append("Code correctly reverses a sentence with more than one word (4p).")
        else:
            feedback.append("Code does not correctly reverse a sentence with more than one word. Checking individual cases.")
            points_before = points
            # check individual cases
            # check if the code correctly splits the sentence
            if actual_output is not None and len(actual_output) == len(expected_output):
                points += 1
                feedback.append("Code correctly splits the sentence (1p).")
                # check if the code correctly reverses the sentence
                # if the answer is split, we check if the first and last elements are correct
                try:
                    if actual_output[0] == expected_output[0] and actual_output[-1] == expected_output[-1]:
                        points += 1
                        feedback.append("Code correctly reverses the sentence (1p).")
                    else:
                        feedback.append("Code does not correctly reverse the sentence (0p).")
                except KeyError:
                    pass
                    feedback.append("Code does not correctly reverse the sentence (0p).")
            # however, if the student didn't split it, we check if at least they reversed it
            elif actual_output is not None and len(actual_output) == 1:
                feedback.append("Code does not split the sentence (0p).")
                if "Test a" in actual_output[0]:
                    # it is reversed
                    points += 1
                    feedback.append("Code correctly reverses the sentence (1p).")
                else:
                    feedback.append("Code does not correctly reverse the sentence (0p).")
            if points - points_before == 2:
                # case where they correctly return the reversed result
                points += 1
                feedback.append("Code correctly returns the reversed sentence (1p).")
            else:
                feedback.append("Code does not correctly return the reversed sentence (0p).")

        # save both the points and the feedback
        self.points[7] = points
        self.feedback[7] = feedback

    def question_8(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0
        # Criterion 1
        # correctly checks minimum length
        one_name_input = [["Name"]]
        if grader.run_code_on_input(one_name_input) is None:
            points += 0.5
            feedback.append("Code correctly handles lists with one element (0.5p).")
        else:
            feedback.append("Code does not correctly handle lists with one element (0p).")
        # correctly checks for invalid types in the list
        invalid_type_input = [["str2", 2, "str"]]
        if grader.run_code_on_input(invalid_type_input) is None:
            if grader.statement_includes('if', 'isinstance'):
                points += 0.5
                feedback.append("Code correctly checks for invalid types in the list (0.5p).")
            else:
                feedback.append("Code does not correctly check for invalid types in the list (0p).")
        else:
            feedback.append("Code does not correctly handle invalid types in the list (0p).")
        # award extra 0.5 points if both validations pass
        if points == 1:
            points += 0.5
            feedback.append("Code correctly handles lists with one element and invalid types in the list (0.5p).")
        else:
            feedback.append("Code does not correctly handle lists with one element and invalid types in the list (0p).")

        # Criterion 2
        # check if the code correctly removes duplicates
        sample_input = [["str1", "str2", "str1", "str2"]]
        expected_output = ["str1", "str2"]
        if grader.check_single_output(sample_input, expected_output):
            points += 2
            feedback.append("Code correctly removes duplicates from the list (2p).")
        else:
            feedback.append("Code does not correctly remove duplicates from the list. Checking individual cases.")
            # check each case
            # check if for loop exists that traverses through the list
            if grader.includes_for():
                points += 0.25
                feedback.append("Code traverses through the list (0.25p).")
            else:
                feedback.append("Code does not correctly traverse through the list (0p).")
            # check if the student checks if the element already exists in the resulting list
            # Could check if the if statement includes 'not in' statement, or just an 'in' statement, but
            # it might be too strict and specific
            if grader.body_includes('for', 'if'):
                points += 0.75
                feedback.append("Code checks if the element already exists in the resulting list (0.75p).")
            else:
                feedback.append("Code does not correctly check if the element already exists in the resulting list (0p).")
            # check if the resulting list is appended and returned correctly
            if grader.body_includes('for', 'append') and isinstance(grader.run_code_on_input(sample_input), list):
                points += 0.75
                feedback.append("Code appends elements into the resulting list and returns it (0.75p).")
            else:
                feedback.append("Code does not correctly append elements into the resulting list and return it (0p).")

        # save both the points and the feedback
        self.points[8] = points
        self.feedback[8] = feedback

    def question_9(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        points = 0
        # Criterion 1
        # Any solution taht correctly identifies the entries of input are valid months
        invalid_months_input = [[("January", 80), ("Mar", 110), ("April", 70), ("May", 60)]]
        valid_months_input = [[("January", 80), ("March", 110), ("April", 70), ("May", 60)]]
        if grader.run_code_on_input(invalid_months_input) is None:
            if grader.run_code_on_input(valid_months_input) is not None:
                points += 1
                feedback.append("Code checks if the entries are valid months (1p).")
            else:
                feedback.append("Code does not correctly check if the entries are valid months (0p).")
        else:
            feedback.append("Code does not correctly handle invalid months (0p).")

        # Criterion 2
        # any solution that correctly identifies to each quarter an entry from the input belongs to
        if len(grader.get_ifs()) >= 4:
            points += 1
            feedback.append("Code correctly assigns each entry to a quarter (1p).")
        else:
            feedback.append("Code does not correctly assign each entry to a quarter (0p).")

        # Criterion 3
        # any solution that compares the months regardless of character case
        sample_input = [[("JANUARY", 80), ("March", 110), ("ApRil", 70), ("May", 60)]]
        sample_input_2 = [[("January", 80), ("March", 110), ("April", 70), ("May", 60)]]
        sample_input_3 = [[("january", 80), ("march", 110), ("april", 70), ("may", 60)]]
        result = grader.run_code_on_input(sample_input)
        if result is not None and result == grader.run_code_on_input(
                sample_input_2) and result == grader.run_code_on_input(sample_input_3):
            points += 1
            feedback.append("Code compares the months regardless of character case (1p).")
        else:
            feedback.append("Code does not correctly compare the months regardless of character case (0p).")

        # Criterion 4
        # checking if the code returns a dictionary
        sample_input = [[("January", 80), ("November", 60)]]
        output = grader.run_code_on_input(sample_input)
        if grader.includes_return() and isinstance(output, dict):
            points += 1
            feedback.append("Code returns a dictionary (1p).")
        else:
            feedback.append("Code does not return a dictionary (0p).")

        # Criterion 5
        # any solution that correctly accumulates the rainfall of each quartile
        sample_input = [[("January", 80), ("March", 110), ("April", 70), ("May", 60)]]
        output = grader.run_code_on_input(sample_input)
        if isinstance(output, dict):
            try:
                values = list(output.values())
                if values[0] == 190 and values[1] == 130 and values[2] == 0 and values[3] == 0:
                    sample_input = [[("January", 80), ("March", 110), ("April", 70), ("May", 60), ("November", 300)]]
                    output = grader.run_code_on_input(sample_input)
                    values = list(output.values())
                    if values[0] == 190 and values[1] == 130 and values[2] == 0 and values[3] == 300:
                        points += 6
                        feedback.append("Code correctly accumulates the rainfall of each quartile (6p).")
            except IndexError:
                pass

        if points < 6:
            feedback.append("Code does not correctly accumulate the rainfall of each quartile (0p).")

        # save both the points and the feedback
        self.points[9] = points
        self.feedback[9] = feedback

    def question_10(self, grader):
        feedback = []  # Feedback will be used to provide more detailed feedback to the student
        # generally recommended to use the feedback for every criterion that you check

        # boolean to simply check if a point was given to avoid a lot of else statements for the feedback
        points_given = False

        points = 0

        empty_lists = [[], []]
        one_empty = [[(1, "Title"), (2, "Author"), (3, "Publisher")], []]
        one_empty_2 = [[], [(1, "Think Python"), (2, "Allen Downey"), (3, "Green Tea Press")]]
        unequal_size = [[(1, "Title"), (2, "Author"), (3, "Publisher")], [(1, "Think Python"), (2, "Allen Downey")]]
        sample_input = [[(1, "Title"), (2, "Author"), (3, "Publisher")],
                        [(1, "Think Python"), (2, "Allen Downey"), (3, "Green Tea Press")]]
        expected_output = {"Title": "Think Python", "Author": "Allen Downey", "Publisher": "Green Tea Press"}
        # VALIDATION CHECKS
        # check if empty lists are handled
        if grader.check_single_output(empty_lists, expected=None):
            # if they are, check if one empty list is handled
            if grader.check_single_output(one_empty, expected=None):
                # if it is, check if the other empty list is handled
                if grader.check_single_output(one_empty_2, expected=None):
                    # award a point
                    points_given = True
                    points += 1
                    feedback.append("Code correctly handles empty lists (1p).")

        if not points_given:
            feedback.append("Code does not correctly handle empty lists (0p).")

        # reset it for other checks
        points_given = False

        # check if unequal size lists are handled
        if grader.check_single_output(unequal_size, expected=None):
            # check if equal sizes are not returning None:
            if grader.run_code_on_input(sample_input):
                points += 1
                points_given = True
                feedback.append("Code handles lists of unequal size (1p).")

        if not points_given:
            feedback.append("Code does not correctly handle lists of unequal size (0p).")

        # if both previous criteria pass, check if the student prints for invalid arguments and returns
        if points == 2:
            if grader.body_includes('if', 'print') and grader.body_includes('if', 'return'):
                points += 1
                feedback.append("Code correctly prints and returns for invalid input (1p).")
            else:
                feedback.append("Code does not correctly print and return for invalid input (0p).")
        else:
            feedback.append("Code does not correctly handle invalid input (empty list and unequal lists) (0p).")

        # CRITERIA 2
        # check if the correct sample input returns the correct output
        if grader.check_single_output(sample_input, expected=expected_output):
            points += 2
            feedback.append("Code correctly returns the dictionary (2p).")
        else:
            feedback.append("Code does not correctly return the dictionary.")

        # check if we have a nested loop
        if grader.includes_nested_loop():
            # check if that nested loop has an if statement
            if grader.nested_body_includes('for', 'if') or grader.nested_body_includes('while', 'if'):
                points += 4
                feedback.append("Code uses a nested loop with an if statement (4p).")
            else:
                feedback.append("Code does not correctly use an if statement in the nested loop (0p).")
        else:
            feedback.append("Code does not correctly use a nested loop (0p).")

        # check if the code returns a dictionary with correct types
        result = grader.run_code_on_input(sample_input)
        if result and isinstance(list(result.keys())[0], str) and isinstance(list(result.values())[0], str):
            points += 3
            feedback.append("Code returns a dictionary with correct types (3p).")
        else:
            feedback.append("Code does not return a dictionary with correct types (0p).")

        # save both the points and the feedback
        self.points[10] = points
        self.feedback[10] = feedback


