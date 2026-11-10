FROM python:3.9-slim

# Set the working directory in the container
<<<<<<< HEAD
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Document the port used by Flask
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
=======


# Install dependencies

# Copy the rest of the application code

# Run the app

>>>>>>> 827206eddeb2971072677769d8373c62a009215a
