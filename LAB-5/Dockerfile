# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /

# Install Flask
RUN pip install Flask==2.3.3

# Copy the current directory contents into the container at /
COPY / .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]