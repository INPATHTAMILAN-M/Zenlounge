FROM python:3.10-slim

# Set the working directory
WORKDIR /app
# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code
COPY . .
# Expose the port
EXPOSE 8000 
# Start the FastAPI application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

