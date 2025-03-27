FROM python:3.12 
RUN mkdir /app 
WORKDIR /app 
COPY * . 
RUN pip install -r requirements.txt 
# ENV PYTHONPATH 
EXPOSE 3000
CMD ['python','main.py']