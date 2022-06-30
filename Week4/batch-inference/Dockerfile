FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "score.py", "./" ]

RUN pipenv install --system --deploy

ENTRYPOINT ["python", "score.py"]