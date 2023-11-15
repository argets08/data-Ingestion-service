# Use an official Python runtime as a parent image
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1  
  
# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .
COPY ./pyproject.toml ./poetry.lock* ./  
# Install any needed packages specified in requirements.txt
RUN pip install poetry  
RUN poetry install  
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV PORT=8001

# Run FastAPI server on port 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]