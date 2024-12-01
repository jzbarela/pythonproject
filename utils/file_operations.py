# utils/file_operations.py

import csv
from datetime import datetime

def save_responses_to_csv(responses, filename='survey_responses.csv'):
    """
    Save survey responses to a CSV file.

    Args:
        responses (dict): Dictionary of question texts and answers.
        filename (str): Name of the CSV file.
    """
    # Add a timestamp to each response for better tracking
    responses_with_timestamp = {'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    responses_with_timestamp.update(responses)
    
    headers = list(responses_with_timestamp.keys())
    answers = list(responses_with_timestamp.values())

    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write headers only if file is empty
            if file.tell() == 0:
                writer.writerow(headers)
            writer.writerow(answers)
        print(f"Responses saved to {filename}.")
    except Exception as e:
        print(f"Error saving responses to CSV: {e}")