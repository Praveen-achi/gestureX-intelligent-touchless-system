# GestureX: Intelligent Touchless HCI System

[![Docker CI/CD](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Jenkins CI/CD](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

GestureX is an intelligent, touchless Human-Computer Interaction (HCI) system that translates hand gestures captured through computer vision into instant desktop actions. Built with OpenCV, MediaPipe, and Streamlit, it is containerized with Docker and fully automated using a Jenkins CI/CD pipeline.

---

## 🖐 Supported Gestures & Actions

| Gesture | Finger Pattern | Mapped System Action |
| :--- | :---: | :--- |
| `FIST` | `(0, 0, 0, 0, 0)` | Open Notepad |
| `V_SIGN` | `(0, 1, 1, 0, 0)` | Open Camera |
| `OPEN_PALM` | `(1, 1, 1, 1, 1)` | Open Calculator |
| `THUMBS_UP` | `(1, 0, 0, 0, 0)` | Open Web Browser (Google) |
| `ONE` | `(0, 1, 0, 0, 0)` | Open MS Paint |
| `THREE` | `(0, 1, 1, 1, 0)` | Open Command Prompt / Terminal |
| `FOUR` | `(0, 1, 1, 1, 1)` | Open File Explorer |
| `GUN_SIGN` | `(1, 1, 0, 0, 0)` | Open YouTube |
| `ROCK_SIGN` | `(1, 0, 0, 0, 1)` | Open Spotify |
| `MIDDLE_ONLY` | `(0, 0, 1, 0, 0)` | Open Settings |

---

## 🚀 Quickstart with Docker

### 1. Build and Run using Docker CLI
```bash
# Build the Docker image
docker build -t gesturex-system:latest .

# Run the container
docker run -d --name gesturex_container -p 8501:8501 gesturex-system:latest
```

### 2. Run using Docker Compose
```bash
docker compose up -d --build
```
Access the application at: **[http://localhost:8501](http://localhost:8501)**

---

## ⚙️ Jenkins CI/CD Pipeline

The included `Jenkinsfile` orchestrates an automated 6-stage DevOps pipeline:

1. **SCM Checkout**: Clones the latest commit from the Git repository.
2. **Python Syntax Validation**: Validates the syntax across all modules in an isolated container.
3. **Automated Unit Tests**: Runs the `pytest` test suite covering gesture mapping logic, landmark processing, and action triggers.
4. **Docker Build**: Packages the application into a Docker image tagged with build numbers.
5. **Container Smoke Test**: Spawns a test container and checks the `_stcore/health` endpoint for successful startup.
6. **Deployment**: Deploys the container to the host or cluster with automatic restarts.

---

## 💻 Local Development Setup

```bash
# Clone the repository
git clone https://github.com/Praveen-achi/gestureX-intelligent-touchless-system.git
cd gestureX-intelligent-touchless-system

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest -v tests/

# Start Streamlit application
streamlit run app.py
```
