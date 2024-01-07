# Use an official Anaconda runtime as a parent image
FROM continuumio/anaconda3:2021.05

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y tesseract-ocr libtesseract-dev
RUN conda create -n name_env python=3.8
RUN echo "conda activate name_env" >> ~/.bashrc

# Activate conda environment and install dependencies
SHELL ["conda", "run", "-n", "name_env", "/bin/bash", "-c"]
COPY . /app
RUN pip install -r requirement.txt

# Make port 8089 available to the world outside this container
EXPOSE 8089

# Run server.py when the container launches
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "name_env", "python", "server.py"]
