# 🤖 AdaptiveSkill AI
## Multi-Agent AI Learning, Evaluation & Onboarding Platform

---
# 📌 Overview

AdaptiveSkill AI is an enterprise-ready multi-agent AI platform designed for technical onboarding, AI-assisted learning, automated evaluation, and intelligent assessment workflows.

The platform uses reusable AI skills that dynamically adapt to new and unseen data instead of relying on hardcoded workflows.

The system supports:

- AI-assisted coding guidance
- Technical onboarding
- Dynamic technical evaluation
- Intelligent document summarization
- Interactive quiz generation
- Dataset analysis & visualization
- Audio learning summaries

This architecture enables scalable onboarding and technical learning workflows across different domains and datasets.

---

# 🧠 Dynamic AI Skill Architecture

The platform is built using reusable AI skills capable of generalizing across new data dynamically.

Instead of fixed examples or hardcoded logic, the agents adapt to:

- New onboarding documents
- New coding problems
- New evaluation rubrics
- New datasets
- New participant submissions
- New SQL queries
- New technical domains

This enables scalable enterprise onboarding and AI-assisted evaluation systems with minimal manual configuration.

---

# 🚀 Platform Features

## 1️⃣ Coding Tutor Skill

The Coding Tutor Agent provides contextual AI-assisted technical learning.

### Capabilities

- Explain coding concepts
- Explain Python and SQL
- Explain data science concepts
- Explain datasets
- Debug technical issues
- Support onboarding workflows

### Example Topics

- Python
- SQL
- CI/CD
- Data Science
- Missing Values
- Outlier Detection
- DevOps

---

## 2️⃣ Summary Skill

The Summary Agent summarizes uploaded technical content intelligently.

### Supported Content

- Technical notes
- Source code
- Onboarding documents
- Markdown files
- Text files

### Supported Formats

- TXT
- MD
- PY
- CSV

---

## 3️⃣ Evaluator Skill

The Evaluator Agent performs enterprise-style technical assessment and evaluation.

### Supported Inputs

#### Problem Statement
- Typed input
- PDF upload
- TXT upload
- HTML upload
- DOCX upload

#### Evaluation Rubric
- Typed rubric
- CSV rubric
- XLSX rubric
- PDF rubric
- TXT rubric

#### Participant Submission
- Python files
- SQL files
- HTML files
- CSV/XLSX analysis
- Typed solutions

#### Optional Dataset Upload
- CSV
- XLSX

---

## Evaluation Areas

- Correctness
- Optimization
- Readability
- Error Handling
- Best Practices

---

## Example Enterprise Use Cases

- Technical onboarding assessment
- Coding bootcamp evaluation
- SQL query review
- Assignment evaluation
- AI-assisted screening
- Dataset analysis review

---

## 4️⃣ Interactive Quiz Generation Skill

The Quiz Generator dynamically creates AI-generated technical quizzes.

### Features

- Multiple-choice questions
- Dynamic topic generation
- Answer validation
- Explanation support
- Automatic scoring

### Supported Topics

- Python
- SQL
- DevOps
- Machine Learning
- Spring Boot
- Data Science

---

## 5️⃣ Dataset Visualization Skill

Supports intelligent dataset analysis and visualization.

### Supported Features

- Missing value analysis
- Outlier detection
- Dataset preview
- Statistical summaries

### Supported Formats

- CSV
- XLSX

---

## 6️⃣ Audio Learning Skill

The Audio Summary Agent converts AI-generated explanations into concise audio learning summaries.

### Features

- Text-to-speech
- Key-point extraction
- Audio playback
- Accessibility support

---

# 🏗️ System Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
Multi-Agent Controller
  ↓
------------------------------------------------
| Coding Tutor Skill                           |
| Summary Skill                                |
| Evaluator Skill                              |
| Quiz Generator Skill                         |
| Visualization Skill                          |
| Audio Learning Skill                         |
------------------------------------------------
  ↓
OpenAI GPT Models
```

---

# 📂 Project Structure

```text
project/
│
├── README.md
├── app.py
├── requirements.txt
│
├── agents/
│   ├── __init__.py
│   ├── coding_tutor_agent.py
│   ├── summary_agent.py
│   ├── evaluator.py
│   ├── quiz_generator_agent.py
│   ├── visualization_agent.py
│   └── audio_summary_agent.py
```

---

# ⚙️ Technology Stack

## Frontend
- Streamlit

## AI / LLM
- OpenAI GPT-4o-mini

## Data Processing
- Pandas
- NumPy

## Visualization
- Matplotlib

## Audio
- gTTS

## File Processing
- PyPDF2
- openpyxl

---

# 🔧 Installation

## Clone Repository

```bash
git clone <repository_url>
cd project
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 🔐 Environment Configuration

Configure OpenAI API Key using Streamlit Secrets.

## Streamlit Secrets

```toml
OPENAI_API_KEY="your_api_key"
```

---

# 📋 Sample Evaluation Workflow

## Problem Statement

```text
Write a Python function to create a list containing squares of elements from a given list.
```

---

## Rubric

| Criteria | Marks |
|---|---|
| Correctness | 10 |
| Optimization | 10 |
| Readability | 10 |
| Best Practices | 10 |
| Output Accuracy | 10 |

---

## Submission

```python
def square_list(L):

    return [x ** 2 for x in L]


L = [1,2,3,4]

print(square_list(L))
```

---

## Evaluation Output

```text
Correctness: 10/10
Optimization: 10/10
Readability: 9/10
Best Practices: 9/10
Output Accuracy: 10/10

Final Score: 48/50
```

---

# 📊 Example Quiz Workflow

1. Select Quiz Generator
2. Enter topic (Example: Python)
3. Generate quiz
4. Answer MCQs
5. Submit quiz
6. Receive explanations and score

---

# 📈 Enterprise Benefits

## Scalability
The platform dynamically adapts to new onboarding data, datasets, rubrics, and technical domains.

## Reusability
Reusable AI skills reduce the need for hardcoded workflows.

## Faster Technical Onboarding
Automates learning assistance and technical evaluation.

## AI-Assisted Evaluation
Reduces manual reviewer effort.

## Extensibility
New AI skills and workflows can be integrated easily.

---

# 🔮 Future Enhancements

Potential future improvements include:

- User authentication
- Persistent chat history
- RAG-based document retrieval
- Vector database integration
- LMS integration
- Multi-user collaboration
- Progress tracking dashboards
- Fine-tuned evaluation models
- Adaptive learning paths

---

# ✅ Key Highlights

✅ Multi-Agent AI Architecture  
✅ Dynamic Skill-Based Workflows  
✅ Enterprise Evaluation Engine  
✅ AI Coding Assistance  
✅ Interactive Quiz Generation  
✅ Audio Learning Support  
✅ Dataset Visualization  
✅ PDF / Excel / SQL Support  
✅ Streamlit-Based UI  
✅ OpenAI Integration

---

# 🎯 Business Value

AdaptiveSkill AI helps organizations:

- Accelerate onboarding
- Improve technical learning
- Automate assessments
- Reduce manual evaluation effort
- Scale AI-assisted training workflows
- Enable reusable AI learning capabilities

---

# 📞 Conclusion

AdaptiveSkill AI demonstrates a scalable enterprise-ready multi-agent AI ecosystem capable of supporting onboarding, technical learning, automated evaluation, and AI-assisted assessment workflows across multiple technical domains.

The platform is modular, reusable, extensible, and designed for dynamic adaptation to new datasets, onboarding materials, rubrics, and technical workflows.
