FROM python:3.9-slim        # start from a Python base image
WORKDIR /app                # set working directory inside container
COPY requirements.txt .     # copy requirements first
RUN pip install -r requirements.txt   # install Flask
COPY . .                    # copy all app files
EXPOSE 5000                 # the app runs on port 5000
CMD ["python", "app.py"]    # command to start the app