# Web Scraping, Content Management & Chatbot System

This project consists of a **Django backend** (API and WebApp) and a **React frontend** with web scraping, content management, and chatbot functionalities.

## Folder Structure
```
project-root/
|-- backend/
|   |-- api/
|   |-- webapp/
|   |-- manage.py
|   |-- requirements.txt
|-- frontend/
|   |-- src/
|   |-- public/
|   |-- package.json
|-- .gitignore
|-- README.md
```

## Setup Instructions

### Backend Setup (Django API)
1. **Clone the Repository:**
   ```sh
   git clone 'https://github.com/SathishMadhiyalagan/ChatBot-WebScraper.git'
   cd project-root/backend
   ```
2. **Set up Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # (Windows: venv\Scripts\activate)
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply Migrations:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Run the Server:**
   ```sh
   python manage.py runserver
   ```

### Frontend Setup (React)
1. Open a **new terminal** and navigate to `frontend/`:
   ```sh
   cd project-root/frontend
   ```
2. **Install Dependencies:**
   ```sh
   npm install
   ```
3. **Run the Development Server:**
   ```sh
   npm start
   ```

## API Endpoints

### WebApp Routes (`webapp/urls.py`)
| Route                | Method | Description                 |
|----------------------|--------|-----------------------------|
| `/web/`             | GET    | Web Scraper Home Page      |
| `/web/contentRag`   | POST   | Save Content               |

### API Routes (`api/urls.py`)
| Route              | Method | Description             |
|--------------------|--------|-------------------------|
| `/api/`           | GET    | API Home Page          |
| `/api/query`      | POST   | Handle Chatbot Query   |


## Notes
- The **backend** runs on `http://127.0.0.1:8000/`
- The **frontend** runs on `http://localhost:3000/`
- API calls are handled using `fetch` or `axios` in React
- Ensure the virtual environment is activated before running Django commands

---
**Author:** Sathish Madhiyalagan  
🚀 Happy Coding!

