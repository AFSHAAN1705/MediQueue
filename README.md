# MediQueue: Hospital Patient Scheduling System

A professional simulation of Operating System CPU Scheduling Algorithms applied to a real-world Hospital Patient Queue scenario. This project demonstrates how different scheduling algorithms process patients in a queue, complete with a breathtaking React UI and live execution timeline (Gantt Chart).

## 🚀 Features

- **5 Scheduling Algorithms**: First Come First Serve (FCFS), Shortest Job First (SJF), Round Robin (RR), Priority Scheduling, and Shortest Remaining Time First (SRTF).
- **Interactive Premium UI**: Stunning Dark Mode Glassmorphic interface built with React and Tailwind CSS.
- **Smart Queue Management**: Features Starvation Prevention (Priority Aging) and an Algorithm Recommender based on active queue load.
- **Live Timeline**: Real-time Gantt Chart visualization of patient treatment execution blocks.
- **Secure Access**: Role-Based JSON Web Token (JWT) Authentication.

## 🛠️ Technology Stack

- **Backend**: Python, Flask, SQLAlchemy (SQLite), PyJWT
- **Frontend**: React.js, Vite, Tailwind CSS, Chart.js
- **Architecture**: Client-Server Monorepo

## ⚙️ How to Run Locally

This project is split into two parts: the Flask Backend and the React Frontend. You will need two separate terminal windows to run them simultaneously.

### 1. Start the Flask Backend
Open a terminal, navigate to the backend directory, and install the Python dependencies:
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```
*The backend will run on `http://localhost:5000`.*

### 2. Start the React Frontend
Open a second terminal, navigate to the frontend directory, and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```
*The frontend will run on `http://localhost:5173`.*

## 🔐 Demo Credentials

The system is secured with JWT authentication. Use any of the following mock credentials to log in:

| Role | Username | Password |
|------|----------|----------|
| Administrator | `admin` | `admin123` |
| Head Doctor | `doctor` | `doctor123` |
| Receptionist | `receptionist` | `rec123` |

## 📚 Educational Context
This project was built to demonstrate the practical application of the **Analysis and Design of Algorithms (ADA)** by translating abstract CPU scheduling concepts into a tangible, real-world software engineering product.
