from flask import Flask, request, render_template
import openai
from PyPDF2 import PdfReader
import os

# Initialize Flask app
app = Flask(__name__)


# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read PDF and extract text
def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text


# Function to generate questions
def generate_questions(pdf_text):
    # Construct the message for the chat model
    prompt = f"""Generate multiple-choice questions based on the following text:\n\n{pdf_text}\n
                 Format each question as:\n
                 Question 1: \n a) option 1\n b) option 2\n c) option 3\n d) option 4\ne) answer(eg: a)"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    questions_text = response['choices'][0]['message']['content']
    return parse_questions(questions_text)


def parse_questions(text):
    # Split the response into lines and clean up any empty lines
    question_list = text.strip().split('\n')
    questions = []

    i = 0
    while i < len(question_list):
        # Check for a question line
        if question_list[i].startswith("Question"):
            question = {}
            question['question'] = question_list[i].strip()

            # Ensure there are enough lines for the options and correct answer
            if i + 5 < len(question_list):
                question['option_a'] = question_list[i + 1].strip() if i + 1 < len(question_list) else ""
                question['option_b'] = question_list[i + 2].strip() if i + 2 < len(question_list) else ""
                question['option_c'] = question_list[i + 3].strip() if i + 3 < len(question_list) else ""
                question['option_d'] = question_list[i + 4].strip() if i + 4 < len(question_list) else ""

                # Extract the correct answer (after 'e)')
                correct_answer_line = question_list[i + 5].strip() if i + 5 < len(question_list) else ""
                print("Correct answer line:", correct_answer_line)

                if correct_answer_line.startswith("e)") and len(correct_answer_line) > 2:
                    # Look for the correct answer (it should be 'a)', 'b)', 'c)', or 'd)')
                    for option in ['a', 'b', 'c', 'd']:
                        if f"{option})" in correct_answer_line:
                            question['correct_answer'] = option  # Store only the letter
                            # print("Extracted correct answer letter:", question['correct_answer'])
                            break

                # Add the question to the list
                questions.append(question)

            i += 6  # Move to the next question
        else:
            i += 1  # Skip unexpected lines, continue parsing

    return questions


# Route to handle file upload and question generation
@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        return "No file part", 400
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected file", 400
    
    pdf_text = extract_pdf_text(pdf_file)
    questions = generate_questions(pdf_text)
    return render_template('exam.html', questions=questions, enumerate=enumerate)

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    correct_answers = 0
    incorrect_answers = 0
    total_questions = 0

    # Loop through the submitted form and compare with the correct answers
    for key in request.form:
        if key.startswith('question'):  # This is a question answer
            total_questions += 1
            question_number = key[len('question'):]  # Extract the question number

            # Get the user's submitted answer
            user_answer = request.form.get(f'question{question_number}')
            # Get the correct answer for the question
            correct_answer = request.form.get(f'correct_answer{question_number}')  # Retrieve the correct answer

            # Compare the answers
            if user_answer == correct_answer:
                correct_answers += 1
            else:
                incorrect_answers += 1

    # Calculate the score
    if total_questions > 0:
        score = (correct_answers / total_questions) * 100
    else:
        score = 0  # Avoid division by zero

    # Extract only the integer part of the score
    integer_score = int(score)  # Convert score to integer, discarding the decimal part

    # Pass data to the result template
    return render_template(
        'result.html',
        total_questions=total_questions,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        score=integer_score,  # Pass the integer part of the score
    )
# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)
