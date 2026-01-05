# LLM-Based-Cyberbullying-Detection-with-Human-in-the-Loop-Evaluation

## Overview
This project presents an **LLM-based Trust & Safety system** for detecting cyberbullying and evaluating model behavior in sensitive, high-stakes environments. The system combines **Large Language Models (LLMs)** with **Human-in-the-Loop (HITL) evaluation** to assess not only detection performance, but also **ethical AI attributes** such as empathy, cultural sensitivity, and robustness.

---

## Objectives
- Detect cyberbullying across multiple demographic and contextual categories
- Compare multiple LLM variants using structured human feedback
- Quantitatively evaluate Trust & Safety performance using human-centered metrics
- Analyze model bias and robustness in socially sensitive NLP tasks

---

## Features
- LLM-based cyberbullying detection using supervised learning
- Multi-class classification (age, gender, ethnicity, religion, non-bullying)
- Prompt-engineered contextual and non-judgmental responses
- Human-in-the-Loop (HITL) feedback collection
- A/B testing framework for model comparison
- Quantitative evaluation using Likert-scale metrics

---

## System Architecture
1. **Input Layer**  
   Ingests user-generated text from a chat-based interface.

2. **LLM Classification Layer**  
   A GPT-based model classifies content as cyberbullying or non-cyberbullying and identifies the abuse category.

3. **Response Generation Layer**  
   Uses prompt engineering to generate context-aware, empathetic interventions.

4. **Human-in-the-Loop Evaluation**  
   Users rate model responses on structured evaluation metrics.

5. **Analysis Layer**  
   Aggregates results to analyze bias, robustness, and Trust & Safety performance.

---

## Data
- **Dataset**: Cyberbullying Classification Dataset (Kaggle)
- **Size**: 47,000+ labeled social media posts
- **Classes**:
  - Age-based abuse
  - Gender-based abuse
  - Ethnicity-based abuse
  - Religion-based abuse
  - Non-cyberbullying / Other
- **Format**: JSONL (for LLM fine-tuning)

---

## Evaluation Methodology
- **Evaluation Type**: Human-centered A/B testing
- **Models Compared**: 2 LLM variants (tuned vs. untuned)
- **Metrics** (Likert scale: 1–5):
  - Empathy
  - Cultural Sensitivity
  - Helpfulness
  - Trust & Safety
  - Overall User Experience

Evaluation results were used to analyze:
- Model bias
- Behavioral robustness
- Ethical AI performance in Trust & Safety contexts

---

## Key Findings
- Untuned LLMs showed higher perceived empathy and cultural sensitivity in several scenarios
- Culturally tuned models exhibited more controlled but less flexible behavior
- Human-in-the-Loop evaluation proved critical for identifying limitations not captured by automated metrics alone

---

## Technologies Used
- Large Language Models (LLMs)
- GPT-based fine-tuning
- Natural Language Processing (NLP)
- Supervised Learning
- Prompt Engineering
- Human-in-the-Loop (HITL) Systems
- A/B Testing
- Trust & Safety Machine Learning
- Ethical AI Evaluation

---

## Use Cases
- Trust & Safety AI systems
- Content moderation pipelines
- Responsible AI research
- Applied NLP and LLM evaluation
- Social computing and online safety applications

---

## Disclaimer
This project is a research prototype developed for academic and experimental purposes and is not intended for production deployment.
