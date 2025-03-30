# Use Python as base image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy only requirements.txt first for caching
COPY frontend/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire frontend folder into /app
COPY frontend /app

# Expose the correct port
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
