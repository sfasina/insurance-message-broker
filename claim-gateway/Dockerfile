# download python base image
FROM python:3.12-slim

# creating working folder in docker image
WORKDIR /app

#copy requirements.txt to docker image and install 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all files to docker image
COPY . .

# starting uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
