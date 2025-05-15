# 🧠 LegalMateAI

**Your AI-Powered Legal Contract Review Assistant**

LegalMateAI is an intelligent, agent-based application designed to assist legal professionals, startups, and legaltech teams in reviewing contracts efficiently. It uses a multi-agent system powered by Crew AI to analyze legal documents, extract critical clauses, identify potential risks, simplify legal jargon, and generate comprehensive summaries — all through an intuitive Gradio interface.

---

## 🚀 Features

- 📑 **Clause Extractor** – Identifies and extracts key clauses (e.g., Indemnity, Termination, Liability).
- ⚠️ **Risk Analyzer** – Flags potentially risky clauses using LLMs and legal heuristics.
- ✍️ **Simplifier** – Converts legalese into plain English for broader understanding.
- 🧾 **Summary Writer** – Provides a concise, business-friendly summary of the contract.
- 🖥️ **Gradio Interface** – Clean and interactive web interface to upload and analyze documents.

---

## 🧠 Agentic AI Architecture

LegalMateAI uses [**Crew AI**](https://github.com/joaomdmoura/crewAI) to define and orchestrate specialized agents:

| Agent | Task |
|-------|------|
| **Clause Extractor** | Parses and extracts key legal clauses |
| **Risk Analyzer** | Evaluates extracted clauses for risk |
| **Simplifier** | Rewrites clauses in plain English |
| **Summary Writer** | Generates executive summary of the contract |

---

## 🧰 Tech Stack

- **Backend AI Orchestration:** [Crew AI](https://github.com/joaomdmoura/crewAI)
- **LLMs:** OpenAI GPT-4 (or compatible)
- **Frontend:** Gradio
- **PDF/Text Parsing:** pdfplumber, PyMuPDF (or Unstructured)
- **Storage:** Optional (MongoDB / local JSON for MVP)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/arghads9177/legal-mate-ai.git
cd legal-mate-ai
```

### 2. Create a Virtual Environment
```bash
conda create -m lmaenv python=3.11
conda activate lmaenv/
```
### 3. Install Requirements
```bash
pip install -r requirements.txt
```
## 🛠️ Usage

### 1. Start the App
```bash
python app.py
```
### 2. Open in Browser
Navigate to http://localhost:7860 to use the Gradio interface.

### 3. Upload Contract
-  Upload a **.pdf** or paste contract text.
- Click **"Analyze"** to trigger agents.
- View:

  - Extracted Clauses
  - Risk Report
  - Simplified Explanations
  - Executive Summary

## 🎯 Target Users

- LegalTech Startups
- Legal Process Outsourcing Firms
- Law Firms
- Enterprise Legal Teams
- Startups without in-house legal counsel

## 📄 License
This project is licensed under the [MIT License](https://github.com/arghads9177/legal-mate-ai/blob/master/LICENSE).

