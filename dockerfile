FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies separately
WORKDIR /Muktae
COPY requirements.txt /Muktae/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /Muktae

# Expose the port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0" ]
