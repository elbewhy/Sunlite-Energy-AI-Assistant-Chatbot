💡 Sunlite Energy AI Assistant Chatbot (Flask & Gemini)This project is a simple, yet powerful, web-based AI assistant, branded as the Sunlite Energy AI Assistant Chatbot. It is built with Python (Flask) and the Google Gemini API. It uses a "Retrieval-Augmented Generation (RAG)"-like approach by grounding the large language model (LLM) with content from a local faq.txt file. This ensures the assistant's responses are accurate and relevant, specifically drawing from Sunlite Energy's knowledge base to answer customer and user queries effectively.✨ FeaturesGemini-Powered: Leverages the gemini-2.5-flash model for fast, intelligent conversations.Knowledge Grounding (RAG): Uses the content of faq.txt and a detailed prompt template (prompt_template.txt) to guide the AI's answers, making it a highly effective tool for customer service or organizational help regarding Sunlite Energy products and services.Language Detection: Automatically detects the user's input language and restricts interaction to English (en) and specific Nigerian languages/dialects (ha, yo, ig, pidgin) to ensure appropriate handling for local users.Simple Web Interface: A lightweight frontend built with Flask templates.🛠️ PrerequisitesBefore you begin, ensure you have the following installed:Python 3.8+A Google Gemini API Key.🚀 Installation and SetupFollow these steps to get your chatbot running locally.1. Clone the Repository & Install DependenciesIt's highly recommended to use a Python virtual environment.Bash# Clone the repository (replace URL with your own)
git clone <your-repo-url>
cd chatbot

# Create and activate a virtual environment
python -m venv vvenv
source venv/bin/activate 

# Install required Python packages (You will need a requirements.txt file)
pip install Flask google-genai python-dotenv langdetect
# OR
# pip install -r requirements.txt
2. Configure Environment VariablesCreate a file named .env in the root directory and add your Gemini API key:# .env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
3. Configure Chatbot KnowledgeThe core knowledge base relies on these two files:File NameDescriptionfaq.txtThis file should contain the specific, detailed knowledge about Sunlite Energy products, services, policies, and common questions. The quality and clarity of content here directly impact the AI's response accuracy.prompt_template.txtThis is the master template used to instruct the Gemini model, setting its persona (e.g., "Act as the official Sunlite Energy Assistant") and providing context, including the content of faq.txt.▶️ UsageTo start the Flask server, run the app.py file:Bashpython app.py
The application will start on http://127.0.0.1:5000/.Open your web browser and navigate to this address to start chatting with the Sunlite Energy Assistant.Language Detection NoticeThe chatbot is configured to only process messages detected as:English (en)Hausa (ha)Yoruba (yo)Igbo (ig)Nigerian Pidgin (pidgin)📂 Project Structurechatbot/
├── static/           # CSS and JavaScript files for the frontend
├── templates/        # HTML templates (e.g., index.html)
├── .env              # Environment variables (MUST BE IGNORED by Git)
├── app.py            # Main Flask application and chat logic
├── faq.txt           # Knowledge base for grounding the AI
├── prompt_template.txt # System prompt template for the Gemini API call
└── readme.md         # This file