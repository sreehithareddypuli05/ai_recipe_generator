# 🍳 AI Recipe Generator (Django)

An AI-powered web application built using **Django** that generates personalized recipes based on user-provided ingredients, preferences, and dietary requirements.

---

## 📌 Features

* 🧠 AI-based recipe generation
* 🥗 Ingredient-based suggestions
* 🌱 Supports dietary preferences (Veg/Non-Veg/Vegan)
* 📱 Responsive user interface
* 🔐 User authentication (Login/Register)
* 💾 Save favorite recipes
* 📊 Admin dashboard

---

## 🛠️ Technologies Used

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript, Bootstrap
* **Database:** SQLite / PostgreSQL
* **AI Integration:** OpenAI API / HuggingFace API (Optional)/ollama
* **Version Control:** Git

---

## 📂 Project Structure

```
.
├── db.sqlite3
├── manage.py
├── recipe_project
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── recipes
    ├── admin.py
    ├── ai_service.py
    ├── apps.py
    ├── chat_views.py
    ├── forms.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── templates
    │   └── recipes
    │       ├── add_recipe.html
    │       ├── ai_chat.html
    │       ├── ai_generator.html
    │       ├── all_recipes.html
    │       ├── base.html
    │       ├── detail.html
    │       ├── home.html
    │       └── search.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai_recipe_generator.git
cd ai_recipe_generator
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

Open browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🤖 AI Configuration (Optional)

If using OpenAI API:

1. Get API key from [https://platform.openai.com](https://platform.openai.com)
2. Create `.env` file

```
OPENAI_API_KEY=your_api_key_here
```

3. Install dotenv

```bash
pip install python-dotenv
```

4. Load environment variables in `settings.py`

---

## 🧪 Usage

1. Register or Login
2. Enter ingredients
3. Select preferences
4. Click "Generate Recipe"
5. View AI-generated recipe
6. Save favorite recipes

---


## 📝 Requirements File (Sample)

```
Django>=4.0
openai
python-dotenv
requests
Pillow
```

---

## 🚀 Future Enhancements

* Voice-based input
* Mobile App Version
* Nutrition Analysis
* Multilingual Support
* Recommendation System

---

## ⚠️ Common Errors

| Issue                    | Solution          |
| ------------------------ | ----------------- |
| Server not starting      | Check migrations  |
| API error                | Verify API key    |
| Static files not loading | Run collectstatic |

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make changes
4. Commit changes
5. Push to GitHub
6. Create Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**sreehitha reddy puli**
B.Tech Computer Science Student
Email: [sreehithareddypuli@email.com](mailto:sreehithareddypuli@email.com)
GitHub: [https://github.com/sreehithareddypuli05](https://github.com/sreehithareddypuli05)

---

## ❤️ Acknowledgements

* Django Documentation
* ollama phi3
* Stack Overflow Community

---

> ⭐ If you like this project, give it a star on GitHub!
