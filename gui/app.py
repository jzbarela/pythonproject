import tkinter as tk
from tkinter import messagebox, scrolledtext
from logic.feedback import FeedbackHandler
from logic.openai_api import get_feedback_from_openai
from utils.file_operations import save_responses_to_csv

class FeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Feedback")
        self.feedback_handler = FeedbackHandler()

        self.name_label = tk.Label(root, text="Thanks for providing feedback on the course! Please enter your name:")
        self.name_label.pack(pady=10)

        self.name_entry = tk.Entry(root, width=50)
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Feedback", command=self.start_feedback)
        self.start_button.pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.user_input = tk.Entry(root, width=60)
        self.user_input.pack(pady=5)
        self.user_input.bind("<Return>", self.send_message)

        self.current_question = 0
        self.responses = []
        self.user_name = ""

    def start_feedback(self):
        self.user_name = self.name_entry.get().strip()
        if not self.user_name:
            messagebox.showerror("Error", "Please enter a name.")
            return

        self.name_entry.config(state='disabled')
        self.start_button.config(state='disabled')
        self.display_message("Bot", self.feedback_handler.ask_question(self.current_question))

    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if user_message:
            self.display_message("You", user_message)
            self.user_input.delete(0, tk.END)
            self.responses.append(user_message)
            self.current_question += 1
            if self.current_question < len(self.feedback_handler.questions):
                feedback = get_feedback_from_openai(user_message)
                self.display_message("Bot", feedback)
                self.display_message("Bot", self.feedback_handler.ask_question(self.current_question))
            else:
                save_responses_to_csv('feedback_responses.csv', self.user_name, self.feedback_handler.questions, self.responses)
                self.display_message("Bot", "Thank you for your feedback! Your responses have been saved.")
                self.user_input.config(state='disabled')

    def display_message(self, sender, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)