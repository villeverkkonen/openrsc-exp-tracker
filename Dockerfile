FROM nikolaik/python-nodejs

WORKDIR /code/client

COPY ./client .

RUN npm install

RUN npm run build

WORKDIR /code/backend

COPY ./backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./backend .

EXPOSE 8005

CMD ["python", "-u", "main.py"]