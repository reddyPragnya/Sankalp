# CodeXR: AI Coding Assistant

[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

CodeXR is an **AI-powered coding assistant** built for AR/VR developers. It leverages **Google's Gemini API** and a custom knowledge base to provide tailored, in-depth solutions. The app features a **RAG (Retrieval-Augmented Generation)** system for accuracy and a dedicated mode for debugging common development errors.

---

## ✨ Key Features

- **Structured Code Generation**: Step-by-step solutions with ready-to-use code snippets.  
- **RAG-Lite System**: Local, private knowledge base of official AR/VR docs ensures relevant, up-to-date responses.  
- **Error Debugging Mode**: Paste error logs to receive a diagnosis and a step-by-step fix plan.  

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.9+ ([Download](https://www.python.org/downloads/))  

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CodeXR.git
cd CodeXR
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```
Replace "YOUR_API_KEY_HERE" with your Gemini API key.

## 🧠 Building the Knowledge Base (RAG System)

### 1. Scrape and Chunk Documentation

```bash
python scrape_and_chunk_docs.py
```

### 2. Vectorize and Store

```bash
python vectorize_and_store.py
```
> **Note:** The first run downloads the Sentence Transformer model (`all-MiniLM-L6-v2`), which may take a few minutes.


## 💻 Usage

### Run the Streamlit App

```bash
streamlit run main.py
```

### Modes

- **Code Generation Mode**: Ask questions like  
  *“How do I implement teleport locomotion in Unity VR?”*  
  → AI provides structured solutions from the knowledge base.

- **Error Debugging Mode**: Paste error messages or code snippets.  
  → AI diagnoses the problem and suggests a step-by-step solution.

---

## ⚠️ Note

This project currently supports **demo queries only**.  
Dynamic queries are **not yet supported** and may not return results as expected.
