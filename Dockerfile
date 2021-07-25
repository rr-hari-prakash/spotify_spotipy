FROM python:3.7-slim

RUN mkdir /spotify_spotipy

COPY requirements.txt /spotify_spotipy

WORKDIR /spotify_spotipy

RUN pip install -r requirements.txt

COPY . /spotify_spotipy

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
