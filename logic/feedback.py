class FeedbackHandler:
    def __init__(self):
        # Assign the loaded questions to self.questions
        self.questions = self.load_questions()
        self.answers = {}
        self.current_index = 0

    def load_questions(self):
        """
        Load and return the list of survey questions.
        
        Returns:
            list: A list of dictionaries, each representing a survey question.
        """
        questions = [
            {
                "id": 1,
                "text": "What were your goals for this course?",
                "type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
                "option_texts": {
                    "A": "Learn something completely new",
                    "B": "Supplement previous knowledge",
                    "C": "Refresh previous knowledge",
                    "D": "Other"
                }
            },
            {
                "id": 2,
                "text": "Out of 5 stars, what do you rate the course?",
                "type": "rating",
                "scale": [1, 5]
            },
            {
                "id": 3,
                "text": "In general, how familiar were you with the content before the course?",
                "type": "multiple_choice",
                "options": ["A", "B", "C", "D", "E", "F"],
                "option_texts": {
                    "A": "No knowledge",
                    "B": "I've heard of it, but I don't know much more",
                    "C": "I'm familiar with it",
                    "D": "I could explain the content to others",
                    "E": "I am an expert on the topic",
                    "F": "Other"
                }
            },
            {
                "id": 4,
                "text": "What did you like best about the course?",
                "type": "open_ended"
            },
            {
                "id": 5,
                "text": "Can you provide an example of how you applied what you learned in this course?",
                "type": "open_ended"
            },
            {
                "id": 6,
                "text": "How would you rate the instructor's ability to explain the material?",
                "type": "multiple_choice",
                "options": ["A", "B", "C", "D", "E"],
                "option_texts": {
                    "A": "Poor",
                    "B": "Fair",
                    "C": "Good",
                    "D": "Excellent",
                    "E": "Outstanding"
                }
            },
            {
                "id": 7,
                "text": "On a scale of 1 to 10, how challenging did you find the course content? (1 being not challenging at all and 10 being extremely challenging)",
                "type": "rating",
                "scale": [1, 10]
            },
            {
                "id": 8,
                "text": "How well were you able to apply what you learned?",
                "type": "multiple_choice",
                "options": ["A", "B", "C", "D", "E", "F"],
                "option_texts": {
                    "A": "Not at all",
                    "B": "A little bit",
                    "C": "Moderately well",
                    "D": "Very well",
                    "E": "Exceptionally well",
                    "F": "Other"
                }
            },
            {
                "id": 9,
                "text": "Have you worked with the content before?",
                "type": "yes_no"
            },
            {
                "id": 10,
                "text": "What could be improved about the course?",
                "type": "open_ended"
            },
            {
                "id": 11,
                "text": "The content was accurate, up-to-date, applicable to the real world. (1-4, Untrue to True)",
                "type": "rating",
                "scale": [1, 4]
            },
            {
                "id": 12,
                "text": "The learning goals were clearly defined. (1-4, Untrue to True)",
                "type": "rating",
                "scale": [1, 4]
            },
            {
                "id": 13,
                "text": "The course content was relevant for me.",
                "type": "yes_no"
            },
            {
                "id": 14,
                "text": "The duration of the content was",
                "type": "multiple_choice",
                "options": ["A", "B", "C", "D", "E"],
                "option_texts": {
                    "A": "Much too short",
                    "B": "A bit short",
                    "C": "Just right",
                    "D": "A bit long",
                    "E": "Much too long"
                }
            },
            {
                "id": 15,
                "text": "The course was of high quality (1-4, Untrue to True).",
                "type": "rating",
                "scale": [1, 4]
            }
        ]
        return questions

    def get_all_answers(self):
        """
        Returns a dictionary mapping question texts to user answers.
        This format is compatible with save_responses_to_csv.
        
        Returns:
            dict: A dictionary with question texts as keys and user answers as values.
        """
        return {q['text']: self.answers.get(q['id'], '') for q in self.questions}

    def get_next_question(self):
        """
        Retrieves the next question to be asked.
        
        Returns:
            dict or None: The next question dictionary or None if all questions have been answered.
        """
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def record_answer(self, question_id, answer):
        """
        Records the user's answer to a given question.
        
        Args:
            question_id (int): The ID of the question.
            answer (str): The user's answer.
        """
        self.answers[question_id] = answer
        self.current_index += 1

    def all_questions_answered(self):
        """
        Checks if all survey questions have been answered.
        
        Returns:
            bool: True if all questions are answered, False otherwise.
        """
        return self.current_index >= len(self.questions)