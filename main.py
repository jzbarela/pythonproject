import os
from dotenv import load_dotenv
import openai
import logging

from logic.feedback import FeedbackHandler
from utils.file_operations import save_responses_to_csv

# Setup logging
logging.basicConfig(level=logging.INFO, filename='chatbot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI configuration from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')

# Validate OpenAI configuration
if not OPENAI_API_KEY or not OPENAI_API_BASE:
    raise ValueError("OpenAI API key or base URL not found in environment variables.")

# Configure OpenAI API
openai.api_type = "azure"  # Or "openai" depending on your setup
openai.api_version = "2023-05-15"  # Update if needed
openai.api_base = OPENAI_API_BASE
openai.api_key = OPENAI_API_KEY

# Define the OpenAI engine to use
engine = "gpt-4" 

def generate_assistant_response(conversation_history, max_tokens=150):
    """
    Generate a response from the assistant using OpenAI's ChatCompletion API.
    
    Args:
        conversation_history (list): List of message dictionaries representing the conversation.
        max_tokens (int): Maximum number of tokens in the assistant's response.
        
    Returns:
        str: The assistant's generated message.
    """
    try:
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=conversation_history,
            max_tokens=max_tokens,
            n=1,
            temperature=0.7,
        )
        assistant_message = response['choices'][0]['message']['content'].strip()
        logging.info(f"Assistant Response: {assistant_message}")
        return assistant_message
    except Exception as e:
        logging.error(f"Error generating assistant response: {e}")
        return "I'm sorry, I encountered an error processing your request."

def validate_answer(question, answer):
    """
    Validate the user's answer based on the question type.
    
    Args:
        question (dict): The question dictionary.
        answer (str): The user's answer.
        
    Returns:
        bool: True if the answer is valid, False otherwise.
    """
    answer = answer.strip().lower()
    q_type = question["type"]
    
    if q_type == "multiple_choice":
        # Assuming 'options' are the allowed letters and 'option_texts' contain the full text
        option_keys = [opt.lower() for opt in question.get("options", [])]
        option_values = [v.lower() for v in question.get("option_texts", {}).values()]
        valid_answers = option_keys + option_values
        return answer in valid_answers

    elif q_type == "yes_no":
        return answer in ["yes", "no", "y", "n"]

    elif q_type == "rating":
        try:
            rating = int(answer)
            return question["scale"][0] <= rating <= question["scale"][1]
        except ValueError:
            return False

    elif q_type == "open_ended":
        return len(answer) > 0

    else:
        return False

def sanitize_input(input_str):
    """
    Sanitize user input to prevent CSV Injection attacks.

    Args:
        input_str (str): The user's input.

    Returns:
        str: Sanitized input.
    """
    if input_str.startswith(('=', '+', '-', '@')):
        return f"'{input_str}"
    return input_str

def main():
    feedback_handler = FeedbackHandler()
    
    # Initialize conversation history with a comprehensive system prompt
    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are a friendly and engaging assistant helping the user complete a feedback survey. "
                "Ask one question at a time from the provided list, wait for the user's response, and adapt if they are confused. "
                "Do not introduce new questions. After all questions are answered, thank the user and say goodbye."
            )
        }
    ]
    
    print("Welcome to the Feedback Bot! Type 'exit' to quit.\n")
    logging.info("Survey started.")
    
    while not feedback_handler.all_questions_answered():
        question = feedback_handler.get_next_question()
        if question is None:
            break

        # Construct assistant prompt with the question and options
        assistant_prompt = question['text']
        
        # Include options if available
        if question["type"] == "multiple_choice" and "option_texts" in question:
            options = "\n".join([f"{key}. {value}" for key, value in question["option_texts"].items()])
            assistant_prompt += f"\nOptions:\n{options}"
        elif question["type"] == "yes_no":
            assistant_prompt += " (Yes or No)"
        elif question["type"] == "rating" and "scale" in question:
            assistant_prompt += f" (Please rate from {question['scale'][0]} to {question['scale'][1]})"

        # Add assistant's question to conversation history
        conversation_history.append({"role": "assistant", "content": assistant_prompt})
        logging.info(f"Asking Question ID {question['id']}: {assistant_prompt}")

        # Prompt user input
        user_input = input(f"Bot: {assistant_prompt}\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Bot: Goodbye!")
            logging.info("Survey terminated by user.")
            return

        # Sanitize user input to prevent CSV Injection
        sanitized_input = sanitize_input(user_input)
        
        # Add sanitized user's response to conversation history
        conversation_history.append({"role": "user", "content": sanitized_input})

        # Validate user input
        valid = validate_answer(question, sanitized_input)
        retries = 0
        MAX_RETRIES = 3

        while not valid and retries < MAX_RETRIES:
            # Generate a helpful assistant response using OpenAI
            assistant_response = generate_assistant_response(conversation_history)
            print(f"Bot: {assistant_response}\nYou: ", end='')

            # Get user's new input
            user_input = input().strip()
            if user_input.lower() == 'exit':
                print("Bot: Goodbye!")
                logging.info("Survey terminated by user during input validation.")
                return

            # Sanitize new user input
            sanitized_input = sanitize_input(user_input)

            # Add sanitized user's new input to conversation history
            conversation_history.append({"role": "user", "content": sanitized_input})
            valid = validate_answer(question, sanitized_input)
            retries += 1

        if not valid:
            # After maximum retries, move to the next question
            print("Bot: Let's move on to the next question.\n")
            logging.info(f"Max retries reached for Question ID {question['id']}. Moving to next question.")
        else:
            # Record the valid answer
            feedback_handler.record_answer(question["id"], sanitized_input)
            logging.info(f"Recorded Answer for Question ID {question['id']}: {sanitized_input}")

            # Provide a fixed acknowledgment to prevent duplication and confusion
            acknowledgment = "Thank you for your response!"
            conversation_history.append({"role": "assistant", "content": acknowledgment})
            print(f"Bot: {acknowledgment}\n")
            logging.info(f"Acknowledgment sent for Question ID {question['id']}.")

    # After all questions are answered, provide a closing message
    closing_message = "Thank you for completing the survey. Have a great day!"
    conversation_history.append({"role": "assistant", "content": closing_message})
    print(f"\nBot: {closing_message}")
    logging.info("Survey completed successfully.")
    
    # Save responses to CSV using the utility function
    responses = feedback_handler.get_all_answers()
    save_responses_to_csv(responses)

if __name__ == "__main__":
    main()
