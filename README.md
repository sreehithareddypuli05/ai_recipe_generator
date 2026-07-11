# 🍽️ AI Recipe Generator

An intelligent recipe recommendation system that suggests recipes based on the ingredients provided by the user. The project leverages Natural Language Processing (NLP) and Machine Learning to retrieve the most relevant recipes from a large dataset, making meal planning faster and easier.

---

## 🚀 Features

- 🔍 Search recipes using available ingredients
- 🤖 AI-powered recipe recommendation engine
- 📋 Displays recipe name, ingredients, cooking steps, and preparation time
- ⚡ Fast semantic search using FAISS indexing
- 🧠 NLP-based ingredient matching with Sentence Transformers
- 🌐 Simple and responsive web interface built with Django

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python
- Django

### Machine Learning & NLP
- Sentence Transformers
- FAISS
- Scikit-learn
- Pandas
- NumPy

### Database
- SQLite3

---

## 📁 Project Structure

```text
AI-Recipe-Generator/
│
├── datasets/
│   ├── cleaned/
│   │   ├── cleaned_recipes.csv
│   │   ├── cleaned_recipes.pkl
│   │   └── train_recipe_model.py
│   │
│   ├── models/
│   │   ├── recipe_embeddings.pkl
│   │   ├── recipe_index.faiss
│   │   └── recipes.pkl
│   │
│   └── raw/
│       ├── RAW_interactions.csv
│       └── RAW_recipes.csv
│
├── notebooks/
├── recipe_project/
├── recipes/
├── scripts/
├── requirements.txt
├── manage.py
├── db.sqlite3
├── .gitignore
├── .gitattributes
└── README.md
```

---

## 📊 Workflow

```
Raw Dataset
      │
      ▼
Data Cleaning & Preprocessing
      │
      ▼
Generate Recipe Embeddings
      │
      ▼
Create FAISS Search Index
      │
      ▼
Train Recommendation Model
      │
      ▼
Django Web Application
      │
      ▼
Recipe Recommendations
```

---

## 📥 Dataset

The dataset is not included in this repository because of its large size.

Download the dataset from the link below:

**Google Drive:**  
👉 **<Paste Your Google Drive Link Here>**

After downloading, extract the folder into the project directory:

```text
AI-Recipe-Generator/
└── datasets/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sreehithareddypuli05/AI-Recipe-Generator.git
```

Navigate to the project directory.

```bash
cd AI-Recipe-Generator
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv311
```

Activate the environment.

**Windows**

```bash
venv311\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Download the Dataset

Download the dataset using the Google Drive link provided above and place it inside the **datasets** folder.

---

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🧠 How It Works

1. The user enters one or more ingredients.
2. The input is converted into semantic embeddings using Sentence Transformers.
3. FAISS performs a similarity search against the indexed recipe embeddings.
4. The most relevant recipes are retrieved.
5. Recipe details are displayed through the Django web interface.

---

## 📦 Major Libraries

- Django
- Sentence Transformers
- FAISS
- NumPy
- Pandas
- Scikit-learn
- Torch

---

## 🔮 Future Enhancements

- User Authentication
- Personalized Recipe Recommendations
- Voice-Based Ingredient Search
- Nutrition Analysis
- AI Meal Planner
- Shopping List Generator
- Recipe Image Generation
- Favorite Recipes
- Recipe Rating & Reviews

---

## 👩‍💻 Author

**Sreehitha Reddy Puli**

**GitHub:**  
https://github.com/sreehithareddypuli05

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.
