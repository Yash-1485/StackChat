# 💬 StackChat

**StackChat** is a modern, full-stack real-time chat application with video calling, friend requests, and sleek UI built for seamless communication. Designed for students, teams, and communities.

---

## 🚀 Tech Stack

### 🖥️ Frontend
- React.js
- Tailwind CSS
- Stream Chat SDK (UI Components + Video Calling)
- Zustand (Global State for theme, etc.)
- React Query (Data fetching & caching)
- Lucide Icons

### 🧠 Backend
- Django (with Django REST Framework)
- JWT Authentication (custom implementation)

### 🔒 Auth
- Full JWT auth: signup, login, logout, onboarding
- Protected routes
- Stream token generation using authenticated Django users

---

## ✨ Features

- ✅ User Signup/Login
- ✅ JWT-based Authentication
- ✅ Profile & Onboarding
- ✅ Add Friends / Accept Requests
- ✅ One-to-One Real-time Chat
- ✅ Video Calling via Stream API
- ✅ Theme Toggle (Light/Dark)
- ✅ Fully responsive UI
- ✅ Chat loader, toast notifications, clean UI transitions

---

## 🖼️ Screenshots

> _(Include some screenshots here showing login, chat, video call, friend list, etc.)_

---

## 🛠️ Setup Instructions

### 🔧 Backend (Django)

1. Clone the repo and move into the Django backend directory:
    ```bash
    git clone https://github.com/Yash-1485/StackChat.git
    cd StackChat/backend
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the backend root:
    ```
    SECRET_KEY=your-django-secret-key
    DEBUG=True
    STREAM_API_KEY=your-stream-api-key
    STREAM_SECRET_KEY=your-stream-secret-key
    ```

5. Run migrations and start server:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

---

### 🌐 Frontend (React)

1. Move into the frontend directory:
    ```bash
    cd ../frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Create a `.env` file:
    ```
    VITE_STREAM_API_KEY=your-stream-api-key
    VITE_BACKEND_URL=http://localhost:8000  # or your hosted Django backend
    ```

4. Start the development server:
    ```bash
    npm run dev
    ```

---

## 🙌 Credits

- [GetStream Chat SDK](https://getstream.io/chat/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Lucide Icons](https://lucide.dev/)
- Inspired by modern chat experiences like WhatsApp, Discord, and Slack

---

## 📦 Future Improvements

- ✅ Group Chat Support
- ✅ Notifications via Firebase
- ✅ Settings Page
- ✅ Profile Edit and Image Upload
- ✅ Message Reactions / Typing Indicators
- ✅ Socket.IO-based fallback (for custom backend)

---

## 📄 License

This project is open-source and available under the MIT License.

---

> Built with ❤️ by Yash Parekh
