FROM python:latest
RUN apt update
RUN git clone https://github.com/SubornaN/kuralabs_deployment_5.git
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8081
ENTRYPOINT ["python", "application.py"]