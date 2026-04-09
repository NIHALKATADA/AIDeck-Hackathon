<div align="center">
  <h1>🤖 AIDeck | AI File Agent</h1>
  <p><strong>Transform a single prompt into boardroom-ready presentations and datasets in seconds.</strong></p>

  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit" alt="Streamlit"></a>
  <a href="https://groq.com/"><img src="https://img.shields.io/badge/AI_Engine-Groq_Llama_3-F55036" alt="Groq"></a>
  <a href="https://python.org/"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</div>

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🎯 About the Project

*Built for [Insert Hackathon Name here]*

Creating structured, formatted presentations and datasets manually is a massive time sink. **AIDeck** is an intelligent visual agent designed to automate this workflow. By leveraging the ultra-low latency of the Groq API and the reasoning capabilities of Llama 3.3, AIDeck acts as your personal research and design assistant. 

Simply type a topic, choose your detail level, and let the agent draft, format, and export native `.pptx` and `.xlsx` files ready for your next meeting.

<div align="center">
  <img width="1918" height="977" alt="Screenshot 2026-04-10 000210" src="https://github.com/user-attachments/assets/eb0732e9-e105-459e-9baf-f29ebce2dfbb" />

</div>

---

## ✨ Key Features

- 🧠 **Zero-to-Deck Generation:** Converts a minimal 2-word prompt into a fully structured, multi-slide 16:9 presentation.
- 🎛️ **Smart Context Levels:** Employs advanced prompt constraints to dynamically shift output between *Concise* (executive summaries), *Standard*, and *Detailed* (technical readouts).
- 🎨 **Dynamic UI Previews:** Live-render and edit the AI's output in the browser using custom CSS cards before committing to an export. Includes multiple Cover Slide aesthetic layouts (Modern Circle, Split Accent, Top Banner).
- 💾 **Native File Export:** Bypasses markdown and generates raw, native Microsoft Office files (`.pptx` and `.xlsx`) built programmatically on the fly.
- ⚡ **Anti-Caching Architecture:** Implements session-state versioning to defeat ghost memory and ensure clean UI updates upon AI refinement.

---

## 🛠️ Tech Stack

**Frontend / UI:**
- [Streamlit](https://streamlit.io/) (Interactive web framework)
- Custom HTML/CSS injection (Live slide rendering)

**AI / Backend:**
- [Groq API](https://groq.com/) (Ultra-fast LLM inference)
- `llama-3.3-70b-versatile` (Core reasoning model)
- Strict JSON Schema Enforcement

**Data Processing & Export:**
- `python-pptx` (PowerPoint generation)
- `pandas` & `openpyxl` (Data manipulation and Excel generation)
- `pydantic` (Data validation and type checking)

---

## 🚀 Getting Started

Follow these steps to set up a local development environment.

### 1. Prerequisites
- **Python 3.9+** installed on your machine.
- A free API key from [Groq Cloud](https://console.groq.com/keys).

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/AIDeck-Hackathon.git](https://github.com/YOUR_USERNAME/AIDeck-Hackathon.git)
cd AIDeck-Hackathon
