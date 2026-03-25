Here is a README.md you can put in your project root and customize with your name/GitHub.

text
# 🧠 Resume Screening AI System

An AI-powered **resume screening** tool that automatically ranks resumes based on how well they match a given job description using **NLP embeddings** and **cosine similarity**. The system supports both a **CLI pipeline** and an optional **Streamlit web interface** for interactive use. Similar systems use sentence-transformer embeddings and cosine similarity for semantic resume–JD matching. [web:51][web:54][web:55][web:58]

---

## 🚀 Features

- Upload or load multiple resumes (PDF / DOCX / TXT).
- Load or paste a job description.
- Clean and preprocess all texts.
- Generate dense embeddings using a **Sentence-Transformer** model (e.g. `all-MiniLM-L6-v2`). [web:51][web:54]
- Compute **cosine similarity** between each resume and the job description. [web:51][web:58]
- Rank resumes by relevance and display **Top K** candidates.
- Simple **Streamlit UI** to run everything in the browser. [web:55][web:59]

---

## 📂 Project Structure

```bash
resume-screening-ai/
│
├── data/
│   ├── resumes/
│   │   ├── resume_1.txt
│   │   ├── resume_2.txt
│   │   └── ...
│   └── job_descriptions/
│       └── jd_software_engineer.txt
│
├── models/
│   └── README.md
│
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── embedder.py
│   ├── ranker.py
│   └── main.py
│
├── app.py
├── requirements.txt
└── README.md
This layout follows common open-source resume-screening and NLP app structures. [web:8][web:52][web:58]

🛠️ Installation
Clone the repository (or create the folder):

bash
git clone <your-repo-url> resume-screening-ai
cd resume-screening-ai
Create virtual environment:

bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
The project uses sentence-transformers, torch, scikit-learn, streamlit, PyPDF2, python-docx, and nltk. [web:37][web:43]

Download NLTK resources (first time only):

bash
python
>>> import nltk
>>> nltk.download("punkt")
>>> nltk.download("stopwords")
>>> exit()
📊 How It Works
Data loading

Resumes are loaded from data/resumes/ (PDF/DOCX/TXT) using PyPDF2, python-docx, or plain text I/O. [web:53][web:57]

Job description is loaded from data/job_descriptions/ (TXT for simplicity).

Preprocessing

Lowercasing, URL and digit removal, punctuation stripping, tokenization and stopword removal with NLTK. [web:48][web:58]

Embedding

Texts are converted into dense vectors using a pretrained Sentence-Transformer such as all-MiniLM-L6-v2. [web:51][web:54]

Similarity & Ranking

Compute cosine similarity between job description embedding and each resume embedding. [web:51][web:58]

Sort resumes by similarity score in descending order to get the most relevant candidates. [web:51][web:54]

Interface

CLI: python -m src.main --top_k 5

Web UI: streamlit run app.py [web:31][web:38][web:44]

🧪 Running the Project
1) Command-line mode
Make sure you are in the project root and the virtualenv is activated.

bash
python -m src.main --top_k 5
Loads all resumes from data/resumes/.

Uses the first .txt job description in data/job_descriptions/.

Prints the Top 5 ranked resumes with similarity scores.

You can optionally pass a specific job description:

bash
python -m src.main --top_k 3 --jd data/job_descriptions/jd_software_engineer.txt
Running Python modules from the command line like this is a common pattern for CLI tools. [web:36][web:39][web:42]

2) Streamlit web app
Start the app:

bash
streamlit run app.py
Streamlit will open http://localhost:8501 in your browser. [web:31][web:38]

Upload Files tab

Upload multiple resumes and one JD.

Click “Run Screening (Uploads)” to see ranked candidates.

Use Existing Data tab

Select resumes from data/resumes/ and a JD from data/job_descriptions/.

Choose Top K and click “Run Screening (Existing Data)”.

Streamlit is widely used to quickly build data/ML dashboards and demos. [web:31][web:44][web:59]

📁 Sample Data
data/resumes/resume_1.txt – Sample Software Engineer resume.

data/resumes/resume_2.txt – Sample Data Scientist / ML Engineer resume.

data/job_descriptions/jd_software_engineer.txt – Example JD for a Python/ML/NLP role.