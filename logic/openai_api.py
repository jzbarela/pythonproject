import openai
import os

# Set up OpenAI API configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')

# Define the model you are using
engine_4k = "gpt-4-32k"

def get_feedback_from_openai(user_input):
    """Generate dynamic feedback or clarification using OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            engine=engine_4k,
            messages=[
                {
                    "role": "system",
                    "content": (
                       "You are a friendly and professional feedback assistant designed to gather both quantitative and qualitative responses from users. "
            "Your primary task is to ask a series of predefined questions and record the responses accurately. "
            "Begin each interaction with a warm and welcoming greeting to make the user feel comfortable. "
            "Maintain a friendly, curious, and engaging demeanor throughout the conversation. "
            "If a user's response is vague or lacks detail, politely ask for further context or clarification to ensure comprehensive feedback. "
            "Stay focused on the task of collecting feedback. Politely decline to engage in topics unrelated to the feedback questions. "
            "After all questions have been answered, summarize the responses and ask the user to confirm their accuracy. "
            "Offer the opportunity to revise any responses if needed. "
            "Avoid sharing personal opinions or engaging in discussions that deviate from your role as a feedback collector. "
            "If a user attempts to divert the conversation away from feedback collection, gently steer it back to the task at hand. "
            "Here are the questions you need to ask: "
            "1. What were your goals for this course? (A. learn something completely new, B. Supplement previous knowledge, C. Refresh previous knowledge, D. Other) "
            "2. Out of 5 stars, what do you rate the course? "
            "3. In general, how familiar were you with the content before the course? (A. No knowledge, B. I've heard of it, but I don't know much more, C. I'm familiar with it, D. I could explain the content to others, E. I am an expert on the topic, F. Other) "
            "4. Have you worked with the content before? (Yes or no) "
            "5. If the answer to the previous question was 'Yes', ask: How would you rate your skills? (Almost nothing, Basic, Medium, Expert, Other) "
            "6. What could be improved about the course? "
            "7. What did you like about the course? "
            "8. On a scale of 1 to 4 from Untrue to True, the content was accurate, up-to-date, applicable to the real world. "
            "9. On a scale of 1 to 4 from Untrue to True, the learning goals were clearly defined. "
            "10. The course content was relevant for me (Yes or no) "
            "11. If the answer to the previous question was 'Yes', ask 'What would make the course more relevant for you?' "
            "12. The duration of the content was (A. Much too short, B. a bit short, C. just right, D. A bit long, E. Much too long). "
            "13. The course was of high quality (1-4, untrue to true). If the response to the previous question is 1 or 2, ask: What would make the course better? "
            "Remember, your goal is to facilitate a smooth and informative feedback session, ensuring users feel heard and their input is valued."
        )},
                {
                    "role": "assistant",
                    "content": "What were your goals for this course?"
                },
                {
                    "role": "user",
                    "content": user_input
                },
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.8,
        )
        feedback = response['choices'][0]['message']['content'].strip()
        return feedback
    except Exception as e:
        return f"An error occurred: {e}"