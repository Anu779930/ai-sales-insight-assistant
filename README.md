# 🤖 AI Sales Insight Assistant

**Author:** Venkata Sai Anusha Kommasani  
**Date:** October 2025  
**Tools:** Python · Pandas · Typer · Rich  

---

## 🧠 Project Overview
The **AI Sales Insight Assistant** is a Python-based conversational analytics tool that transforms natural-language sales questions into actionable insights.  
It acts as an **AI-powered analytics copilot**, interpreting questions like “Profit by region last year” or “Total sales last month in CA.”  
This project merges **AI reasoning** with **data analytics**, ideal for Data Analysts, Business Analysts, and AI Automation roles.

---

## 🎯 Objectives
- Convert plain English questions into structured analytics  
- Detect time windows automatically (`last month`, `this year`, etc.)  
- Filter by region, category, and product  
- Compute sales and profit dynamically  
- Build the foundation for AI-driven dashboards  

---

## 🧩 Features

### 🗣️ Natural-Language Querying
Ask questions like:
- "total sales last month in CA"  
- "profit by region last year"  
- "sales by month this year"  
- "top 3 categories by sales in 2017"

### 📅 Intelligent Time Filters
Supports:
- last month  
- this year  
- last year  
- specific years (2017, 2025)

### 📍 Smart Filters
- Detects U.S. states and abbreviations (CA → California)  
- Recognizes category, product, and region filters  

### 📊 Grouping and Ranking
Groups by:
- Region  
- State  
- Category  
- Product  
- Month  

Handles Top-N queries like *top 5 products* or *top 3 categories*.  

### 💾 Robust CSV Handling
- Auto-detects encoding (UTF-8, Latin-1, etc.)  
- Cleans and normalizes column names  
- Parses date fields intelligently  
- Adds derived columns (Year, Month, MonthName)  

---

## ⚙️ Technologies Used
| Tool | Purpose |
|------|----------|
| Python 3.10+ | Core programming |
| pandas | Data analytics |
| Typer | Command-line interface |
| Rich | Styled console output |
| Superstore Dataset | Real-world sales data |

---
## 📁 Folder Structure

**Project Directory**

ai-sales-insight-assistant/
│
├── data/
│   └── Sample - Superstore.csv
│
├── src/
│   ├── chatbot.py         → CLI interface
│   └── query_engine.py    → Core analytics logic
│
├── requirements.txt
└── README.md

---

## 🧮 Example Queries & Outputs

**Profit by Region**  
Command:  
`python -m src.chatbot "profit by region last year"`  
Output:  
`Profit (2016-01-01 → 2016-12-31) by Region — West: $24,051.61; East: $20,141.60; Central: $19,899.16; South: $17,702.81.`  

**Sales in California**  
Command:  
`python -m src.chatbot "total sales last month in CA"`  
Output:  
`Sales in California (2017-11-01 → 2017-11-30) — $11,701.08.`  

**Top 3 Categories**  
Command:  
`python -m src.chatbot "top 3 categories by sales in 2017"`  
Output:  
`Sales (2017-01-01 → 2017-12-31) by Product — Canon imageCLASS 2200 Advanced Copier: $35,699.90; Martin Yale Chadless Opener Electric Letter Opener: $11,825.90; GBC DocuBind TL300 Electric Binding System: $10,943.28.`  

**Monthly Sales Trend**  
Command:  
`python -m src.chatbot "sales by month this year"`  
Output:  
`Sales (2017-01-01 → 2017-12-30) by MonthName — Jan: $64,734.31; Feb: $50,011.49; Mar: $74,774.08; Apr: $39,072.00; May: $40,882.45; Jun: $47,742.33; Jul: $54,382.09; Aug: $75,675.30; Sep: $74,164.61; Oct: $65,501.16; Nov: $89,306.24; Dec: $56,969.20.`  

---

## 🧾 Requirements

pandas  
typer  
rich 

Install with:  
`pip install -r requirements.txt`

---

## ⚙️ Setup Instructions
1. Clone the repository  
   `git clone https://github.com/Anu779930/ai-sales-insight-assistant.git`  
   `cd ai-sales-insight-assistant`  
2. Create and activate virtual environment  
   - Windows: `.venv\Scripts\activate`  
   - Mac/Linux: `source .venv/bin/activate`  
3. Install dependencies  
   `pip install -r requirements.txt`  
4. Run queries  
   `python -m src.chatbot "profit by region last year"`

---

## 💡 Analytical Capabilities
| Query | Insight |
|-------|----------|
| Profit by Region | Identify most profitable areas |
| Sales by Month | Detect seasonal trends |
| Top Products | Highlight best sellers |
| Category Performance | Compare across product lines |
| State KPIs | Evaluate local sales |

---

## 🌟 Future Enhancements
- Add quarterly and rolling 30/90-day trends  
- Integrate with AgentForce AI / Salesforce Einstein  
- Build a Streamlit dashboard  
- Add voice or chatbot interface  
- Connect to live CRM/SQL pipelines  

---

## 🧠 Conceptual Flow
User Query → NLP Parsing → Intent Extraction → Data Aggregation → Insight Output  

---

## 🧑‍💼 Real-World Applications
- Enterprise sales analysis  
- AI-powered business intelligence  
- Automated KPI reporting  
- CRM analytics (Salesforce/HubSpot)  
- Predictive AI dashboards  

> Ideal for showcasing skills in Data Analytics, AI Automation, and Business Intelligence.  

---

## 👩‍💻 Author
**Venkata Sai Anusha Kommasani**  
📍 Minnetonka, Minnesota  
🎓 M.S. in Information Systems & Technologies — University of North Texas  
💼 Data Analyst | Data Engineer | AI Automation Enthusiast  

**Connect:**  
[LinkedIn](https://www.linkedin.com/in/venkata-sai-anusha/) · [GitHub](https://github.com/Anu779930)

---

## 🏷️ Keywords
`#DataAnalytics` `#AIProjects` `#Python` `#AgentForceAI` `#BusinessIntelligence`  
`#PowerBI` `#SalesAnalytics` `#Automation` `#NaturalLanguageProcessing`

---

## 📚 License
MIT License — open source and free to modify.


