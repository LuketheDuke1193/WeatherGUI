import MySQLdb
import csv
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename='WeatherGUILog.log', level=logging.DEBUG)

def Log_Reg_Startup():
    host = "*********"
    user = "admin"
    db = "WeatherData"
    try:
        my_db = MySQLdb.connect(host="*********", user="admin",
                                passwd="*********", db="WeatherData")
        c = my_db.cursor()
        c.execute("""SELECT max(timestamp) as date, temperature, humidity, averageSpeed AS windspeed, CASE WHEN rainRate > 0
         THEN 1 ELSE 0 END AS raining FROM WeatherData.Readings;""")
        measurement = c.fetchall()
    except MySQLdb.Error:
        logging.debug(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - Error gathering tuple from WeatherData.Readings database for ML model.')
        pass
    timestamp = measurement[0][0]
    date = (timestamp - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M")
    temperature = measurement[0][1]
    humidity = measurement[0][2]
    windspeed = measurement[0][3]
    raining = measurement[0][4]
    fields = np.array([[temperature,humidity,windspeed,raining]])


    print(os.listdir())
    data = pd.read_csv('weatherdata.csv') #Bringing in weather dataset.
    print(data.head(450))
    print(data.describe())
    print(data.count().sort_values())
    data = data.drop(['date'], axis=1)
    print(data.shape)

    #drop potential null values.
    data = data.dropna()
    print(data.shape)

    y = data.rainsoon #Set Y to independent variable (Rain soon?)
    data = data.drop(['rainsoon'], axis=1) #remove it from regular dataset.
    scale = MinMaxScaler(feature_range=(0, 1)) #scale data from 0 to 1
    x = scale.fit_transform(data)

    #split data from X and Y 25/75  for a train set and a test set of data.
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/4, random_state=27)

    #transpose data
    x_train = x_train.T
    y_train = y_train.T
    x_test = x_test.T
    y_test = y_test.T

    #plug data into regression
    logreg = LogisticRegression()
    logreg.fit(x_train.T, y_train.T)

    print('Current Accuracy: {}'.format(logreg.score(x_test.T, y_test.T)))
    current_accuracy = logreg.score(x_test.T, y_test.T) * 100
    output = []
    output.append(current_accuracy)
    #output.append("Testing testing testing.")

    #fields = fields.reshape(1, -1)
    fields = scale.fit_transform(fields)
    fields = fields.T
    prediction = logreg.predict(fields.T).item(0)
    if prediction == 0:
        prediction_text = "It will not rain in the next 15 minutes."
        output.append(prediction_text)
    else:
        prediction_text= "It will rain in the next 15 minutes."
        output.append(prediction_text)

    return output

