FROM python:3.14-slim

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    curl \
    # software-properties-common \
    git

RUN rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/mcfoi/pocketn-nni-manager .

WORKDIR /usr/src/app

ENV STREAMLIT_DATA_DIR=/usr/src/app

# Copy WHEEL file into image and install it
COPY dist/* .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit startup script used by ENTRYPOINT
COPY streamlit_app.py ./
COPY ./datadir ${STREAMLIT_DATA_DIR}

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/usr/src/app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableStaticServing=true"]