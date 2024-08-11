FROM public.ecr.aws/lambda/python:3.12
WORKDIR ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY .env ./
COPY data/vector_db/ ./data/vector_db/
COPY templates/ ./templates/
CMD ["app.handler"]