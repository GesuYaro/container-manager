FROM python:3.10
ADD test_executor.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./test_executor.py"]
