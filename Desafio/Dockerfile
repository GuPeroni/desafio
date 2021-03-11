FROM python:3.9.0


COPY . C:\Users\gusta\Desktop\Desafio
WORKDIR C:\Users\gusta\Desktop\Desafio


RUN pip3 install app
RUN pip3 install uvicorn
RUN pip3 install psycopg2
RUN pip3 install requests
RUN pip3 install json
RUN pip3 install pytest

CMD ["python3", "api_crud.py"]