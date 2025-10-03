# Use a secure, slim Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
# --no-cache-dir keeps the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (including the api folder)
COPY . .

# Set a dummy environment variable; real values come from docker-compose
ENV SUPABASE_URL=dummy_url
ENV SUPABASE_KEY=dummy_key

# Command to run the application when the container starts
# The script will use the local testing block we added in api/index.py
CMD ["python", "api/index.py"]