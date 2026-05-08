# Word Alignment Project for Low Resource Languages

## Project Overview

This project focuses on conducting experiments and evaluation of word alignment for low resource languages using advanced Natural Language Processing (NLP) techniques and integrating the system into a Django based NLP Lab website.

The system performs multilingual translation and semantic word alignment between sentences using transformer-based language models.

The project mainly supports:
- English ↔ Hindi translation
- Semantic word alignment
- Cross-lingual embedding generation
- Alignment visualization through a web interface

The objective of this project is to study multilingual semantic relationships and improve understanding of low resource language processing using modern NLP architectures.

---

# Student Details

- Name: Bhanu Prakash
- Roll Number: 24075023
- Institute: IIT (BHU) Varanasi

---

# Objectives of the Project

The main objectives of the project are:

- To perform multilingual translation using NLLB-200
- To generate multilingual sentence embeddings using LaBSE
- To align semantically related words between source and target sentences
- To visualize alignment mappings through a Django web application
- To conduct experiments on low resource language processing

---

# Technologies Used

## Backend Technologies

- Python
- Django
- Django REST Framework

---

## NLP Models Used

### NLLB-200

NLLB-200 (No Language Left Behind) is used for multilingual translation between low resource languages.

Capabilities:
- Supports multilingual translation
- Handles low resource languages
- Transformer-based architecture

---

### LaBSE

LaBSE (Language Agnostic BERT Sentence Embedding) is used for multilingual semantic embedding generation.

Capabilities:
- Generates multilingual embeddings
- Captures semantic similarity
- Supports cross-lingual alignment

---

## Frontend Technologies

- HTML
- CSS
- JavaScript

---

## Python Libraries Used

- transformers
- sentence-transformers
- torch
- numpy
- django
- rest_framework

---

# Working Methodology

## Step 1 — User Input

The user enters a sentence in the Django web interface and selects the preferred language.

Supported Languages:
- English
- Hindi

Example:

English Input:

```text
I love natural language processing
```

Hindi Translation:

```text
मुझे प्राकृतिक भाषा प्रसंस्करण पसंद है
```

---

## Step 2 — Frontend Request

The frontend sends the user input to the Django backend using HTTP requests.

Main frontend files:
- `index.html`
- `main.js`
- `style.css`

---

## Step 3 — Backend Processing

The Django backend receives the request through views and routes the sentence to the NLP engine.

Main backend files:
- `views.py`
- `urls.py`

The backend coordinates:
- translation
- embedding generation
- word alignment

---

## Step 4 — Translation using NLLB-200

The NLLB-200 model translates the source sentence into the target language.

Translation Examples:

### English → Hindi

Input:

```text
I am learning NLP
```

Output:

```text
मैं NLP सीख रहा हूँ
```

---

### Hindi → English

Input:

```text
मुझे मशीन लर्निंग पसंद है
```

Output:

```text
I like machine learning
```

The model improves multilingual support for low resource language translation.

---

## Step 5 — Tokenization

Both source and translated sentences are tokenized into words.

Example:

Source:

```text
I love NLP
```

Tokens:

```text
["I", "love", "NLP"]
```

Translated:

```text
मुझे NLP पसंद है
```

Tokens:

```text
["मुझे", "NLP", "पसंद", "है"]
```

---

## Step 6 — Embedding Generation using LaBSE

LaBSE generates semantic embeddings for:
- source sentence
- translated sentence
- individual words

These embeddings capture semantic meaning across languages.

Example:
- "love" and "पसंद" receive similar embeddings
- semantically related words become closer in vector space

---

## Step 7 — Semantic Similarity Computation

Cosine similarity is computed between source and target word embeddings.

The system identifies semantically similar word pairs.

Example:

| English Word | Hindi Word |
|---|---|
| love | पसंद |
| NLP | NLP |

---

## Step 8 — Word Alignment

The alignment engine maps semantically related words between both languages.

Main alignment file:

```text
aligner.py
```

Responsibilities:
- compute similarity
- identify best matching words
- create alignment mappings

---

## Step 9 — Result Visualization

The aligned words and translated sentence are displayed on the frontend.

The frontend dynamically renders:
- translated sentence
- aligned words
- similarity mappings

using:
- JavaScript
- HTML
- CSS

---

# Project Architecture

```text
User Input
     ↓
Frontend Interface
     ↓
Django Views
     ↓
Translation Engine (NLLB-200)
     ↓
Embedding Generation (LaBSE)
     ↓
Semantic Similarity Computation
     ↓
Word Alignment Engine
     ↓
Frontend Visualization
```

---

# Project Structure

```text
word-alignment-project-explo/
│
├── alignment/
│   │
│   ├── migrations/
│   ├── templates/
│   ├── nlp_engine/
│   │   ├── translator.py
│   │   ├── aligner.py
│   │
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── serializers.py
│   └── apps.py
│
├── nlp_lab/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│   └── alignment/
│       ├── main.js
│       └── style.css
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation Guide

## Step 1 — Clone Repository

```bash
git clone https://github.com/prakash30906/word-alignment-project-explo.git
```

---

## Step 2 — Move into Project Directory

```bash
cd word-alignment-project-explo
```

---

## Step 3 — Create Virtual Environment

```bash
python -m venv venv
```

---

## Step 4 — Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

---

## Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 6 — Run Django Server

```bash
python manage.py runserver
```

---

## Step 7 — Open Browser

Visit:

```text
http://127.0.0.1:8000/
```

---

# Usage

1. Open the website
2. Enter sentence
3. Select language
4. Click translate/alignment button
5. View:
   - translated sentence
   - aligned words
   - semantic mappings

---

# Experimental Results

The system successfully:
- Performs multilingual translation
- Generates multilingual semantic embeddings
- Aligns semantically related words
- Supports low resource language processing
- Integrates NLP models into Django framework

---

# Advantages of the System

- Supports multilingual NLP
- Works with low resource languages
- Provides semantic alignment
- Interactive web interface
- Transformer-based architecture
- Modular Django implementation

---

# Future Scope

Future improvements may include:
- Support additional Indian languages
- Improve alignment accuracy
- Add alignment heatmaps
- Deploy using cloud infrastructure
- Optimize inference performance
- Integrate larger multilingual models

---

# Applications

This project can be useful in:
- Machine Translation
- Multilingual NLP Research
- Cross-lingual Information Retrieval
- Language Learning Systems
- Semantic Text Analysis
- NLP Educational Platforms

---

# Conclusion

This project demonstrates the integration of multilingual NLP models into a Django web application for low resource language processing.

Using NLLB-200 and LaBSE, the system performs:
- translation
- embedding generation
- semantic alignment
- multilingual visualization

The project provides a practical implementation of modern multilingual NLP techniques for educational and research purposes.

 
