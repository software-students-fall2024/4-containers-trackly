![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
[![Run ML Tests](https://github.com/software-students-fall2024/4-containers-trackly/actions/workflows/ML-Test.yml/badge.svg)](https://github.com/software-students-fall2024/4-containers-trackly/actions/workflows/ML-Test.yml)
![Test-Web](https://github.com/software-students-fall2024/4-containers-trackly/actions/workflows/web-test.yml/badge.svg)](https://github.com/software-students-fall2024/4-containers-trackly/actions/workflows/web-test.yml))

# Containerized App Exercise

## Project Name

Trackly

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Task Board](#task-board)
8. [Team Members](#team-members)
9. [Acknowledgements](#acknowledgements)

### Project Description 

Trackly is your virtual study companion that uses eye-tracking technology to monitor focus and help you stay on task. By ensuring you maintain consistent attention, Trackly keeps you accountable and maximizes your productivity. 

### Features

- Eye-Tracking: Uses camera input to monitor eyes to determine focus
- Productivity Report: Generates session statistic
- User-Friendly: Intuitive application with appealing visuals
- Modular Architechture: Organized codebase for machine learning, web app, and database
- Environment: Runs seamlessly in containerized environments using Docker

### Technologies Used

- Languages: Python (Flask and ML models), Javascript, HTML
- Frameworks & Libraries: Flask, TensorFlow, OpenCV
- Databases: MongoDB
- Tools: Docker, pipenv, FFmpeg
- CI/CD: Github actions

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/software-students-fall2024/4-containers-trackly.git
cd 4-containers-trackly
```

### 2. Install pipenv

```
pip install pipenv
```

### 3. Install dependencies

```
pipenv install
```

### 4. Activate the shell

```
pipenv shell
```

### 5. Build and run docker containers

```
docker compose up --build -d
```

### 6. Stop docker containers

```
docker compose down
```

### Usage
1. Build and launch app using instructions above for setup
2. Access Trackly at http://localhost:5001
3. Start session and monitor productivity through the web app using the camera module
4. View session details

## Project Structure

```text
.
├── machine_learning_client
│   ├── camera_module.py
│   ├── client.py
│   ├── database.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── readme.txt
│   ├─ requirments.text 
│   └── SOON:test_client or test_module.py
├── mongoddb
│   └── Dockerfile
├── web-app
│   ├── static
│   │   ├── css
│   │   │   └── index.css
│   │   └── app.js
│   ├── templates
│   ├── ├─ start-focusing.html
│   │   └── home.html
│   ├── app.py
│   ├── Docker-compose.yml
│   ├── Dockerfile
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── readme.txt
│   ├── requirements.txt
│   └── SOON:test_app.py
├── .gitignore
├── docker-compose.yml
├── instructions.md
├── LICENSE
└── README.md
```

## Task Boards
[The Task board for our team](https://github.com/orgs/software-students-fall2024/projects/109)

## Team Members
- [Hugo Bray (hwb4547)](https://github.com/BringoJr)
- [Ethan Cheng (ehc7678)](https://github.com/ethanhcheng)
- [Nuzhat Bushra(ntb5562)](https://github.com/ntb5562)
- [Tamara Bueno (tb2803)](https://github.com/TamaraBuenoo)

## Acknowledgements 

We used online tutorials and forums. We got a LOT of help from the tutor. And we'd like to dedicated this section as a Thank you to Shambhavi for dedicating extra time to help us. <3
