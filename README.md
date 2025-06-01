
# Multi-Agent File Processing System

This project is a **multi-agent system** that processes files in various formats (PDF, JSON, Emails) and classifies them based on **intent and urgency**. The system can operate in two modes:
- 🖥️ **Command-Line Interface (CLI)**
- 🌐 **Streamlit Web App**

## 📦 Features
- 🗂️ Supports **PDF, JSON, Email (.eml, .msg, .emlx, .pst)** files.
- 🤖 Classifies file **intent** (e.g., Invoice, RFQ, Complaint) and **urgency** using a remote AI API.
- 🧠 Maintains **shared memory** (SQLite database) to avoid reprocessing files.
- 🔍 Displays processed data and enables traceability.
- 🌈 User-friendly **CLI** and **Streamlit** interface.

## 🏗️ Project Structure
```
├── Agents/
│   ├── agent_router.py          # Routes files to appropriate agents
│   ├── ExtractAgent.py          # Extracts content from files
│   ├── FileTypeAgent.py         # Determines file type
│   ├── IntentAgent.py           # Classifies intent using an AI API
│   └── UrgencyAgent.py          # Classifies urgency using an AI API
├── database/
│   └── db.py                    # SQLite database handling
├── utils/
│   └── decorators.py            # Optional decorators (e.g., caching)
├── main.py                      # CLI application
├── app.py                       # Streamlit web app
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 Installation

1️⃣ Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-file-router.git
cd multi-agent-file-router
```

2️⃣ Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

4️⃣ Add your **API Key** to a `.env` file:
(Add your huggingface api key as this project uses huggingface models from api.)
```
API_KEY=your_api_key_here
API_URL = 'https://api-inference.huggingface.co/models/facebook/bart-large-mnli'
CANDIDATE_LABELS_INTENT = 'Request For Quotation,invoice, complaint, regulation, meeting, order, spam'
CANDIDATE_LABELS_URGENCY = 'High Urgency,Low Urgency,Medium Urgency'
```

## 🚀 Usage

### 🖥️ **Command-Line Mode**
```bash
python main.py
```
- Prompts user to upload a file.
- Classifies file intent & urgency.
- Saves results to a local SQLite database (`file.db`).
- Allows viewing stored data or processing another file.

### 🌐 **Streamlit Web App**
```bash
streamlit run app.py
```
- Upload a file through the web interface.
- Displays extracted data and classification.
- Stores data in the database.
- Optional: View stored data via the "Show Stored Data" button.

## ⚠️ Notes
- 📁 SQLite (`file.db`) is used to store processed data. Can be reset as needed.
- 🔐 Ensure your `.env` file contains valid API keys.
- 🌐 The Streamlit app uses an in-memory approach for file uploads; no files are saved on disk (optional).
- 💾 Both versions can coexist, and the database persists between them.

## 📝 License
This project is open-source and free to use for educational purposes.  
See `LICENSE` for details.

## 🤝 Acknowledgments
- **Parixit** – Developer  
- Inspired by multi-agent systems and file processing AI.
