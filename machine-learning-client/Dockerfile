# Use a base Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

COPY . /app
# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libgl1-mesa-glx \
    libxrender1 \
    libsm6 \
    libxext6 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libx11-xcb1 libxcb-xinerama0 libxkbcommon-x11-0 \
    xvfb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir opencv-python-headless

# Set environment variable for Qt plugins
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/local/lib/python3.10/site-packages/cv2/qt/plugins

# Install pipenv
RUN pip install flask

RUN pip install --no-cache-dir pipenv

RUN pipenv install opencv-python-headless
# Copy Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install Python dependencies from Pipfile using pipenv
RUN pipenv install --deploy --ignore-pipfile

RUN pip install -r requirements.txt

# Define the default command to run the client
CMD ["python", "client.py"] 

# "client.py"
