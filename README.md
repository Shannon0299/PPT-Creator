AI Academic Content Generator
This project is the backend service for an application designed to automate the creation of educational content, such as PowerPoint presentations and quizzes, using generative AI.

Overview
As an academic content developer, your goal is to streamline the creation process. This application provides an API endpoint that takes a topic and other parameters, generates structured content using an AI model (like Google's Gemini), and formats that content into a downloadable .pptx file.

Tech Stack
Backend: FastAPI (a high-performance Python web framework)

Server: Uvicorn (an ASGI server to run FastAPI)

AI: Google Gemini API (via the google-generativeai Python SDK)

PowerPoint Generation: python-pptx

Project Structure
.
├── .gitignore          # Files to ignore in Git
├── LICENSE             # Your project's license
├── README.md           # This file
├── requirements.txt    # Python dependencies
│
├── frontend/           # (Placeholder) For a separate React/Vue/Svelte frontend
│
├── static/             # For a simple built-in HTML/CSS/JS frontend
│   └── index.html
│
├── templates/          # To store .pptx templates
│   └── default_template.pptx
│
└── src/                # Main application source code
    ├── __init__.py     # Makes 'src' a Python package
    ├── main.py         # FastAPI app, API endpoints
    ├── ai_generator.py # Logic for calling Gemini API
    └── ppt_builder.py  # Logic for building the .pptx file

Setup & Installation
Clone the repository:

git clone <your-repo-url>
cd ai-content-generator

Create and activate a virtual environment:

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Set up your AI credentials:
This project uses the Gemini API. You'll need an API key.

Get your key from Google AI Studio.

Set it as an environment variable:

# Windows (Command Prompt)
set GEMINI_API_KEY="YOUR_API_KEY"

# Windows (PowerShell)
$env:GEMINI_API_KEY="YOUR_API_KEY"

# macOS/Linux
export GEMINI_API_KEY="YOUR_API_KEY"

Run the application:

uvicorn src.main:app --reload

Your server will be running at http://127.0.0.1:8000. You can access the API documentation at http://127.0.0.1:8000/docs.

How to Use
Send a POST request to the http://127.0.0.1:8000/generate-ppt endpoint with a JSON body like this:

{
  "topic": "The Basics of Photosynthesis",
  "slide_count": 5
}

The API will return a .pptx file in response.
