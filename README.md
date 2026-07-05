# 🌍 RealityVerse – AI-Powered Ecosystem Control Dashboard

RealityVerse is an AI-powered multi-agent simulation platform that transforms real-world habits into the evolution of a virtual ecosystem. The project combines a modern React frontend with a FastAPI backend and multiple AI agents to visualize how daily activities influence different aspects of a digital world.

Developed as the capstone project for the **Google × Kaggle Agentic AI Course**, RealityVerse demonstrates how autonomous AI agents can collaborate to analyze user activities, simulate environmental changes, and provide intelligent insights.

---

## 📖 Project Overview

RealityVerse explores the idea of representing personal growth as a living digital ecosystem.

Every activity performed by the user contributes to the health and balance of different virtual biomes. Multiple AI agents analyze these activities from different perspectives such as productivity, wellness, finance, focus, and sustainability.

The platform visualizes the ecosystem through an interactive dashboard and a 3D planet, allowing users to observe how consistent habits affect their virtual world over time.

---

## ✨ Features

### 🌍 Interactive Dashboard
- Modern responsive dashboard interface
- Ecosystem equilibrium visualization
- Activity logging interface
- Recent activity timeline

### 🤖 Multi-Agent AI System
- Forest Governor Agent
- Ocean Governor Agent
- Finance Governor Agent
- Focus Governor Agent
- Butterfly Agent
- Observer Agent
- Reflection Agent
- Future Simulation Agent
- Central Coordinator Agent

### 📊 Habit Intelligence
- Log daily activities
- Assign impact values
- Generate ecosystem updates
- Monitor ecosystem metrics

### 🌌 Ecosystem Simulation
- Forest biome health
- Ocean current stability
- Crystal energy levels
- Citadel shield strength
- Global ecosystem equilibrium

### 🔗 Backend API
- FastAPI REST endpoints
- SQLite database
- AI agent orchestration
- Activity persistence

---

# 🛠️ Tech Stack

## Frontend
- React
- TypeScript
- Vite
- CSS3

## Backend
- FastAPI
- Python
- SQLite
- Pydantic
- Uvicorn

## AI
- Google Gemini API
- Multi-Agent Architecture

## Development
- Git
- GitHub
- VS Code

---

# 🏗️ Architecture

```
                    User
                      │
                      ▼
             React + Vite Frontend
                      │
                REST API Calls
                      │
                      ▼
               FastAPI Backend
                      │
          ┌───────────┴───────────┐
          │                       │
      SQLite DB             AI Coordinator
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
  Forest Agent             Ocean Agent              Finance Agent
        │                         │                         │
   Focus Agent           Butterfly Agent         Reflection Agent
                                  │
                           Future Simulation
```

---

# 📂 Project Structure

```
kaggle_capstone_project/
│
├── backend/
│   ├── agents/
│   ├── app/
│   ├── mcp/
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/DishaSangiri/kaggle_capstone_project.git
```

```
cd kaggle_capstone_project
```

---

## Backend

```
cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
DATABASE_URL=your_database_url
GEMINI_API_KEY=your_api_key
API_HOST=localhost
API_PORT=8000
MCP_HOST=localhost
MCP_PORT=8001
```

Run server

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```
cd frontend
```

Install

```bash
npm install
```

Run

```bash
npm run dev
```

Open

```
http://localhost:5173
```

---

# 📸 Screenshots

## Dashboard

> Add a screenshot here.

Example:

```
images/dashboard.png
```

---

## Planet View

> Add screenshot here.

---

## Activity Logging

> Add screenshot here.

---

## AI Governor Dashboard

> Add screenshot here.

---

# 🚀 Future Improvements

- Improve 3D planet rendering
- Add real-time WebSocket synchronization
- Deploy to cloud
- User authentication
- Multiple user profiles
- Historical analytics dashboard
- Mobile responsive optimization
- Advanced AI reasoning between agents
- Dynamic ecosystem events
- Enhanced visualization and animations

---

# 🎯 Capstone Objective

This project was developed as the capstone submission for the **Google × Kaggle Agentic AI Course**.

The objective was to design and implement a practical AI-powered application demonstrating autonomous agent collaboration in a real-world inspired scenario.

---

# 👩‍💻 Author

**Disha Sangiri**

B.Sc. Computer Science Student

GitHub:
https://github.com/DishaSangiri

---

# 📄 License

This project is intended for educational and demonstration purposes as part of the Google × Kaggle Agentic AI Capstone Project.
