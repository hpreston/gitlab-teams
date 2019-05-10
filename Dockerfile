FROM python:2-onbuild
ADD ./tests /tests
EXPOSE 5000
CMD python app.py
