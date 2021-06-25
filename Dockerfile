FROM python:3.6
# Create app directory
WORKDIR /usr/app

# Install app dependencies
RUN apt-get update
RUN apt install -y libgl1-mesa-glx poppler-utils tesseract-ocr libtesseract-dev 

COPY ./requirements.txt ./requirements.txt
COPY ./files ./files
COPY ./redacted ./redacted

# Install pythong dependencies
RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader punkt

# Bundle app source
COPY ./src ./src
CMD [ "python3", "src/main.py" ]
