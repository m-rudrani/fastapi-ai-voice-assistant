# Use official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Set environment variables
ENV DATABASE_URL=sqlite:///./interactions.db

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
