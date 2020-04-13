FROM python:3

ADD CB_Covid19_Flask.py /
ADD ./templates/chatbot.html /
ADD chatbot_model.h5 /
ADD classes.pkl /
ADD words.pkl /
ADD covid19_dataset.json /

CMD [ "python", "./CB_Covid19_Flask.py" ]