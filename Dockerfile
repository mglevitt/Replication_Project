
FROM python:3

USER root

WORKDIR /dsc180/replication_project/docker/Replication_Project

RUN pip install pipenv

RUN pip install numpy
RUN pip install pandas
RUN pip install causal-learn

COPY . .

CMD [ "python", "./src/scripts/run.py" ]