# 💰 SmartPocket – AI-Powered Budgeting Assistant for Kids

SmartPocket is a lightweight, AI-powered budgeting web application designed to help children learn responsible money management in a simple, practical, and engaging way. Parents define a budget and duration, while children track daily spending and receive AI-guided advice to avoid overspending and develop healthy financial habits.

🌐 **Live Prototype:**  
👉 https://smartpocket.streamlit.app

---

## 📌 Problem Statement

Children in the present generation often struggle with managing money wisely. Easy access to instant purchases encourages impulsive spending, while most existing finance apps are either too complex, adult-oriented, or dependent on authentication systems and databases.

There is a need for a simple, safe, and educational budgeting tool that helps children understand budgeting, saving, and smart spending.

---

## 🎯 Project Objectives

- Teach children the concept of daily budgeting  
- Encourage delayed gratification and saving  
- Show real-world consequences of overspending  
- Provide AI-based guidance before purchases  
- Keep the system simple and hackathon-friendly  

---

## ✨ Key Features

### 👨‍👩‍👧 Parent-Defined Budget
- Parent sets total budget and number of days
- Automatic daily allowance calculation

### 🛒 Daily Expense Tracking
- Children log daily expenses
- Unspent money carries forward
- Overspending on one day reduces future daily allowances

### 🤖 AI Spending Assistant
- Child-friendly AI chatbot
- Helps children decide whether to spend money
- Suggests saving strategies and alternatives
- Encourages balanced spending (not overspending or oversaving)

### 👤 Multi-User Support (No Passwords)
- Simple username-based login
- Each user has isolated budget data
- No complex authentication or passwords

### 💾 Persistent Storage (No Database)
- User data stored locally in JSON files
- Budget data persists across sessions and days

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Frontend | Streamlit |
| Backend Logic | Python |
| AI Model | Llama-3.1-8B-Instruct |
| AI Provider | Featherless AI (Hugging Face Router) |
| Storage | Local JSON files |
| Authentication | Username-only (Streamlit session) |

---

## 🧠 AI Integration

The AI assistant uses a controlled prompt strategy to ensure:
- Short, clear, child-friendly responses
- No repetition or excessive praise
- Practical and balanced financial advice

The system integrates with Featherless AI inference endpoints for reliable and fast text generation.

---

## 🔐 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Install Dependencies

```bash
pip install streamlit requests
```

### Clone the Repository

```bash
git clone https://github.com/SoumithG26/MoneyBuddy.git
cd MoneyBuddy
```

### Configure Environment Secrets

Create the following file:

```
.streamlit/secrets.toml
```

Add your Hugging Face API token:

```toml
HF_TOKEN = "your_huggingface_token_here"
```

⚠️ Do not hardcode or commit API tokens.

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 🧪 Example Workflow

1. Parent sets a budget of ₹3000 for 30 days  
2. The app calculates the daily allowance automatically  
3. Child logs daily expenses  
4. Overspending today reduces future allowances  
5. Child consults the AI assistant before purchases  
6. Budget data persists across days and logins  

---

## 🏆 Why SmartPocket?

- No database required  
- No complex authentication 
- Strong educational and social impact 
- Helps user take decisions for expenditure

---

## 🚧 Limitations & Future Enhancements

- Expense history and analytics visualization  
- Parent and child role separation  
- Cloud-based persistence for scalability  
- Goal-based saving challenges  
- Multi-language support  

---

## 📜 License

This project is open-source and intended for educational and hackathon use.

---

## 🙌 Acknowledgements

- Streamlit for rapid application development  
- Hugging Face & Featherless AI for AI inference  
- Llama-3.1-8B model  

---

⭐ If you find this project useful, consider starring the repository!
