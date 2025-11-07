# Name & Email Standardization – FastAPI + SQLite

Practical project learn string concepts and methods in Python, using **FastAPI** and **SQLite**.

---

## 📦 Requirements & Setup

You first need to install a virtual environment by running:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then, install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy regex python-multipart email-validator
```

---

## 🚀 Run the App

If your main file is located at `app/main.py`, start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```

Access the interactive API documentation (Swagger UI) at:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 String Concepts Covered

### 🔹 Basic String Manipulation

- **Capitalization:** `title()`, `lower()`
- **Removing extra spaces:** `split()`, `join()`
- **Character replacement:** `replace()`

### 🔹 Regular Expressions (RegEx)

- Removing special characters  
- Substituting patterns  
- Format validation  

### 🔹 Text Normalization

- Removing accents (diacritics)  
- Standardizing formats  

---

## ⚙️ Features

### 🧾 Name Standardization

- Capitalizes each word  
- Handles Portuguese prepositions properly (`de`, `da`, `do`, `das`, `dos`)  
- Removes extra spaces  

### 📧 Email Standardization

- Converts standardized name into an email format (`first.last@company.com.br`)  
- Removes accents and special characters  
- Lowercases everything  
- Adds a default domain (`@company.com.br`)  

### 💾 SQLite Database Integration

- Saves standardized data in `users.db`  
- Enforces unique email addresses  
- Allows listing of stored records  

---

## 🔗 API Endpoints

| **Method** | **Endpoint**  | **Description**                                      |
|-------------|---------------|------------------------------------------------------|
| GET         | `/`           | Welcome message                                     |
| POST        | `/users/`     | Create a new user (standardizes name/email)         |
| GET         | `/users/`     | List all users                                      |

---

## 🧪 Usage Examples

### ▶️ Create a New User

> **Note:** The API currently requires an `email` field in the request body for validation,  
> but it automatically **generates a standardized email** from the name provided.

```bash
curl -X POST "http://localhost:8000/users/"   -H "Content-Type: application/json"   -d '{
    "name": "João da Silva Santos",
    "email": "placeholder@example.com"
  }'
```

#### 🧾 Sample Response 1

```json
{
  "id": 1,
  "name": "João da Silva Santos",
  "email": "joao.da.silva.santos@company.com.br",
  "details": {
    "original_name": "João da Silva Santos",
    "standardized_name": "João da Silva Santos",
    "generated_email": "joao.da.silva.santos@company.com.br"
  }
}
```

---

### 📋 List Users

```bash
curl "http://localhost:8000/users/"
```

#### 🧾 Sample Response 2

```json
[
  {
    "id": 1,
    "name": "João da Silva Santos",
    "email": "joao.da.silva.santos@company.com.br"
  }
]
```

---

## ✨ Standardization Examples

| **Original Name** | **Standardized** | **Generated Email** |
|--------------------|------------------|----------------------|
| JOÃO da SILVA santos | João da Silva Santos | joao.da.silva.santos@company.com.br |
| Maria das Dores | Maria das Dores | maria.das.dores@company.com.br |
| José dos SANTOS Filho | José dos Santos Filho | jose.dos.santos.filho@company.com.br |
