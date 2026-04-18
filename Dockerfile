FROM python:3.12-alpine
RUN pip install flask
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY templates/ templates/
RUN echo "hoot{j1nj4_t3mpl4t3_pwn3d}" > /flag
CMD ["python", "app.py"]
