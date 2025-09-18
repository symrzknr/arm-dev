FROM python:3.13-slim

WORKDIR /home/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./.streamlit ./.streamlit

CMD ["streamlit", "run", "src/main.py", "--server.port=8501"]