FROM python:3.10.9-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create and set workdir
WORKDIR /app/server

# copy local project
COPY . .

#update pip
# install requirements
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# make our entrypoint.sh executable
RUN chmod +x config/entrypoint.sh

EXPOSE 8000

# execute our entrypoint.sh file
ENTRYPOINT ["./config/entrypoint.sh"]