# DecisionTwin AI – Synthetic User Generation and Product Validation Platform

**Tagline:** *Simulate Decisions. Predict Outcomes. Build Better Futures.*

## Overview

DecisionTwin AI is an AI-powered synthetic user generation and product validation platform. It creates realistic synthetic personas and simulates how different user types may respond to products, services, ideas, and business concepts.

The platform helps users explore customer needs, pain points, adoption barriers, survey responses, interview insights, product ratings, and research reports before making product decisions.

## Key Features

- **Synthetic User Generation** – Generate diverse personas based on a target audience and research input.
- **Persona Survey** – Ask survey questions and collect simulated responses from generated personas.
- **Interview Mode** – Interact with personas and generate research-oriented interview insights.
- **Scenario Creator** – Create product or business scenarios for simulation.
- **Simulation** – Run decision simulations using synthetic users.
- **Results Dashboard** – View simulation outcomes and user-response insights.
- **Product Rating** – Generate a product score based on simulated feedback.
- **Research Insights** – Summarize positive points, concerns, needs, pain points, barriers, opportunities, and conclusions.
- **Research Report Generation** – Generate a downloadable research report.

## Technology Stack

### Frontend
- React.js
- Vite
- JavaScript
- HTML5
- CSS3
- React Router

### Backend
- Python
- Flask
- REST APIs

### AI / Data
- Ollama / local LLM integration
- Synthetic persona generation
- AI-based survey and interview simulation
- MongoDB

### Development Tools
- Git
- GitHub
- Visual Studio Code
- Postman

## Project Structure

```text
DecisionTwin-AI/
├── backend/
│   ├── app.py
│   ├── generator.py
│   ├── report_generator.py
│   └── reports/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── Styles/
│   └── ...
├── .gitignore
├── LICENSE
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/preethika65/DecisionTwin-AI.git
cd DecisionTwin-AI
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies if a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

Start the Flask backend:

```bash
python app.py
```

### 3. Frontend setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local Vite URL shown in the terminal.

## Environment Variables

Do not commit API keys, passwords, database credentials, or other secrets.

Store sensitive configuration in a `.env` file. The `.gitignore` file is configured to exclude `.env`.

## Workflow

```text
Product / Research Input
          ↓
   Synthetic Personas
          ↓
   Survey / Interview
          ↓
     Simulation
          ↓
   AI-Based Analysis
          ↓
 Results + Product Rating
          ↓
   Research Report
```

## Project Goal

The goal of DecisionTwin AI is to provide an accessible way to test product ideas and understand possible customer reactions through synthetic user simulations, helping teams identify opportunities and potential adoption barriers before real-world validation.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
