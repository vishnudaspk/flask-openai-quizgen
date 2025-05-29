# flask-openai-quizgen

An AI-powered Flask web application that generates multiple-choice questions (MCQs) from uploaded PDF files using OpenAI's GPT-4 API.

## 🚀 Features

- Upload any PDF file
- Automatically extracts content from PDF
- Uses OpenAI's GPT-4 to generate quiz questions
- Renders questions in a clean exam-style UI
- Submit answers and receive a score with feedback

## 🛠️ Built With

- **Python 3**
- **Flask** - web framework
- **OpenAI GPT-4** - language model to generate questions
- **PyPDF2** - to read and extract text from PDF files
- **Jinja2** - for rendering HTML templates

## 📷 Screenshots

<!-- Add screenshots of `index.html`, `exam.html`, `result.html` -->


## 🧪 How It Works

1. User uploads a PDF file via the homepage.
2. PDF is parsed and text is extracted.
3. Text is sent to OpenAI GPT-4 to generate MCQs.
4. MCQs are rendered in a browser form.
5. User submits answers, and app evaluates and scores them.

## 🧰 Installation

```bash
git clone https://github.com/yourusername/flask-openai-quizgen.git
cd flask-openai-quizgen
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a .env file or set your API key directly:

bash
Copy
Edit
export OPENAI_API_KEY=your_key_here
Run the app:

bash
Copy
Edit
python app.py
Visit http://127.0.0.1:5000 in your browser.

📦 Dependencies
Include a requirements.txt file:

txt
Copy
Edit
Flask
openai
PyPDF2
python-dotenv
Generate it (if needed):

bash
Copy
Edit
pip freeze > requirements.txt
