![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Test-ML]()
![Test-Web]()

# Containerized App Exercise

## Project Name

Trackly

### Project Description 

Trackly is your virtual study companion that uses eye-tracking technology to monitor focus and help you stay on task. By ensuring you maintain consistent attention, Trackly keeps you accountable and maximizes your productivity. 

### Project structure

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
## Task boards
[The Task board for our team](https://github.com/orgs/software-students-fall2024/projects/109)

## Team Members
- [Hugo Bray (hwb4547)](https://github.com/BringoJr)
- [Ethan Cheng (ehc7678)](https://github.com/ethanhcheng)
- [Nuzhat Bushra(ntb5562)](https://github.com/ntb5562)
- [Tamara Bueno (tb2803)](https://github.com/TamaraBuenoo)

## Acknowledgements 

We used online tutorials and forums. We got a LOT of help from the tutor. And we'd like to dedicated this section as a Thank you to Shambhavi for dedicating extra time to help us. <3
