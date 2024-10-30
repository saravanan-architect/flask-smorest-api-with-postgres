# old version - use it to run  on docker locally
# FROM python:3.10
# EXPOSE 5000
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .  
# # first dot is current directory for our file system
# # second dot is current directory of workdir file system

# CMD ["flask", "run", "--host", "0.0.0.0"]



# new version - new version designed render.com docker and also for gunicorn 
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .  
# first dot is current directory for our file system
# second dot is current directory of workdir file system

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

