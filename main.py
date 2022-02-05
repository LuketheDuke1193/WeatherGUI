import sys
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from datetime import datetime, timedelta
import ForecastData
import numpy as np
import MLModel as ml
import logging

from MainWindow import Ui_CustomConstructionWeather

logging.basicConfig(filename='WeatherGUILog.log', level=logging.DEBUG)
logging.debug(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - Starting Main Window Weather Application')


class MainWindow(QtWidgets.QMainWindow, Ui_CustomConstructionWeather):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.current_date = datetime.now()
        self.start_date = self.current_date
        #self.currentbutton = self.TemperatureButton
        self.graphwidget.setBackground('w')
        self.graphwidget.setTitle("Temperatures Forecasted")
        self.graphwidget.showGrid(x=True, y=True)
        self.TemperatureButton.clicked.connect(lambda: self.plot_Temperatures(self.current_date))
        self.WindspeedButton.clicked.connect(lambda: self.plot_Windspeed(self.current_date))
        self.PrecipitationButton.clicked.connect(lambda: self.plot_Precipitation(self.current_date))
        self.prevtimebutton.clicked.connect(lambda: self.prev_timespan(self.currentbutton))
        self.nexttimebutton.clicked.connect(lambda: self.next_timespan(self.currentbutton))
        self.currentbutton.clicked.connect(lambda: self.current_timespan(self.currentbutton))
        self.ShowLinesBox.clicked.connect(lambda: self.plot_Temperatures(self.current_date))
        self.plot_Temperatures(self.current_date)
        output = ml.Log_Reg_Startup()
        print(output)
        self.rainpredictionlabel.setText(output[1])
        self.accuracyLabel.setText(str(output[0]) + "%")
        self.updatebutton.clicked.connect(lambda: ml.Log_Reg_Startup())

    def plot(self, hour, temperature):
        pen = pg.mkPen(color=(255,0,0), width=2)
        self.graphwidget.plot(hour, temperature, pen=pen, symbol='+', symbolsize=2)

    def plot_Temperatures(self, date):
        self.ShowLinesBox.setVisible(True)
        self.graphwidget.addLegend()
        styleY = {'color':'r', 'font-size':'15pt'}
        stylex = {'color':'b', 'font-size':'15pt'}
        self.graphwidget.setLabel('left', 'Temperature (F)', **styleY)
        self.graphwidget.setLabel('bottom', 'Hours From Forecast Time', **stylex)
        self.currentbutton = self.TemperatureButton
        self.graphwidget.clear()
        if self.ShowLinesBox.isChecked():
            forecast = ForecastData.Get_Forecasts(date)
            self.graphwidget.setTitle("Temperatures Forecasted from " + str(forecast.get_date()))
            pen = pg.mkPen(color=(255, 0, 0), width=2)
            temp_list1 = forecast.list[0].temp_list()
            self.graphwidget.plot(temp_list1, name = "KY3", pen=pen, symbol='+', symbolsize=2)
            pen = pg.mkPen(color=(0, 0, 255), width=2)
            temp_list2 = forecast.list[1].temp_list()
            self.graphwidget.plot(temp_list2, name = "NWS", pen=pen, symbol='+', symbolsize=2)
            pen = pg.mkPen(color=(0, 255, 0), width=2)
            temp_list3 = forecast.list[2].temp_list()
            self.graphwidget.plot(temp_list3, name = "Accuweather", pen=pen, symbol='+', symbolsize=2)
            ct_list = self.central_tendency(temp_list1, temp_list2, temp_list3)
            pen = pg.mkPen(color=(0, 0, 0), width=2.5, style=QtCore.Qt.DashLine)
            self.graphwidget.plot(ct_list, name = "Central Tendency", pen=pen, symbol='+', symbolsize=2)
            real_forecast = ForecastData.Get_Realized_Data(date)
            temp_list4 = real_forecast.temp_list()
            pen = pg.mkPen(color=(255, 0, 255), width=3, style=QtCore.Qt.DashLine)
            self.graphwidget.plot(temp_list4, name="Realized Data", pen=pen, symbol='+', symbolsize=2)
        else:
            forecast = ForecastData.Get_Forecasts(date)
            self.graphwidget.setTitle("Temperatures Forecasted from " + str(forecast.get_date()))
            temp_list1 = forecast.list[0].temp_list()
            self.graphwidget.plot(temp_list1, name = "KY3", pen=None, symbolBrush = (255,0,0), symbol='t1', symbolsize=2)
            temp_list2 = forecast.list[1].temp_list()
            self.graphwidget.plot(temp_list2, name = "NWS", pen=None, symbolBrush = (0,0,255), symbol='t2', symbolsize=2)
            temp_list3 = forecast.list[2].temp_list()
            self.graphwidget.plot(temp_list3, name = "Accuweather", pen=None, symbolBrush = (0,255,0), symbol='t3', symbolsize=2)
            ct_list = self.central_tendency(temp_list1, temp_list2, temp_list3)
            self.graphwidget.plot(ct_list, name = "Central Tendency", pen=None, symbolBrush = (0,0,0), symbol='o', symbolsize=2)
            real_forecast = ForecastData.Get_Realized_Data(date)
            temp_list4 = real_forecast.temp_list()
            self.graphwidget.plot(temp_list4, name="Realized Data", pen=None, symbolBrush = (255,0,255), symbol='star', symbolsize=2)



    def plot_Windspeed(self, date):
        self.graphwidget.addLegend()
        self.currentbutton = self.WindspeedButton
        self.graphwidget.clear()
        forecast = ForecastData.Get_Forecasts(date)
        self.graphwidget.setTitle("Wind Speeds Forecasted from " + str(forecast.get_date()))
        styleY = {'color':'r', 'font-size':'15pt'}
        stylex = {'color':'b', 'font-size':'15pt'}
        self.graphwidget.setLabel('left', 'Windspeed (MPH)', **styleY)
        self.graphwidget.setLabel('bottom', 'Hours From Forecast Time', **stylex)
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        wind_list1 = forecast.list[0].wind_list()
        self.graphwidget.plot(wind_list1, name = "KY3", pen=pen, symbol='+', symbolsize=2)
        pen = pg.mkPen(color=(0, 0, 255), width=2)
        wind_list2 = forecast.list[1].wind_list()
        self.graphwidget.plot(wind_list2, name = "NWS", pen=pen, symbol='+', symbolsize=2)
        pen = pg.mkPen(color=(0, 255, 0), width=2)
        wind_list3 = forecast.list[2].wind_list()
        self.graphwidget.plot(wind_list3, name = "Accuweather", pen=pen, symbol='+', symbolsize=2)
        ct_list = self.central_tendency(wind_list1, wind_list2, wind_list3)
        pen = pg.mkPen(color=(0, 0, 0), width=2.5, style=QtCore.Qt.DashLine)
        self.graphwidget.plot(ct_list, name = "Central Tendency", pen=pen, symbol='+', symbolsize=2)
        real_forecast = ForecastData.Get_Realized_Data(date)
        wind_list4 = real_forecast.wind_list()
        pen = pg.mkPen(color=(255, 0, 255), width=3, style=QtCore.Qt.DashLine)
        self.graphwidget.plot(wind_list4, name="Realized Data", pen=pen, symbol='+', symbolsize=2)


    def plot_Precipitation(self, date):
        self.graphwidget.clear()
        self.graphwidget.addLegend()
        self.currentbutton = self.PrecipitationButton
        forecast = ForecastData.Get_Forecasts(date)
        self.graphwidget.setTitle("Precipitation Forecasted from " + str(forecast.get_date()))
        styleY = {'color':'r', 'font-size':'15pt'}
        stylex = {'color':'b', 'font-size':'15pt'}
        self.graphwidget.setLabel('left', 'Precipitation Chances', **styleY)
        self.graphwidget.setLabel('bottom', 'Hours From Forecast Time', **stylex)
        precip_list1 = forecast.list[0].precip_list()
        x = np.arange(12)
        bg1 = pg.BarGraphItem(x=x+0.3, height=precip_list1, name = "KY3 - Red", width=0.2, brush='r')
        self.graphwidget.addItem(bg1)
        precip_list3 = forecast.list[2].precip_list()
        bg2 = pg.BarGraphItem(x=x+0.1, height=precip_list3, name = "Accuweather - Blue", width=0.2, brush='b')
        self.graphwidget.addItem(bg2)
        ct_list = self.central_tendency_precip(precip_list1, precip_list3)
        bg3 = pg.BarGraphItem(x=x-0.1, height=ct_list, name = "Central Tendency - Green", width=0.2, brush='g')
        self.graphwidget.addItem(bg3)
        real_forecast = ForecastData.Get_Realized_Data(date)
        precip_list4 = real_forecast.precip_list()
        if self.current_date == self.start_date:
            del precip_list4[-1]
        x = np.arange(len(precip_list4))
        bg4 = pg.BarGraphItem(x=x-0.3, height=precip_list4, name = "Realized Data - Cyan",width=0.2, brush='c')
        self.graphwidget.addItem(bg4)


        # self.graphwidget.setTitle("Precipitation Forecasted from " + str(forecast.get_date()))
        # pen = pg.mkPen(color=(255, 0, 0), width=2)
        # precip_list1 = forecast.list[0].precip_list()
        # self.graphwidget.plot(precip_list1, name = "KY3", pen=pen, symbol='+', symbolsize=2)
        # #pen = pg.mkPen(color=(0, 0, 255), width=2)
        # #precip_list2 = forecast.list[1].precip_list()
        # #self.graphwidget.plot(precip_list2, name = "NWS", pen=pen, symbol='+', symbolsize=2)
        # pen = pg.mkPen(color=(0, 255, 0), width=2)
        # precip_list3 = forecast.list[2].precip_list()
        # self.graphwidget.plot(precip_list3, name = "Accuweather", pen=pen, symbol='+', symbolsize=2)
        # ct_list = self.central_tendency_precip(precip_list1, precip_list3)
        # pen = pg.mkPen(color=(0, 0, 0), width=2.5, style=QtCore.Qt.DashLine)
        # self.graphwidget.plot(ct_list, pen=pen, symbol='+', symbolsize=2)
        # real_forecast = ForecastData.Get_Realized_Data(date)
        # precip_list4 = real_forecast.precip_list()
        # if self.current_date == self.start_date:
        #     del precip_list4[-1]
        # pen = pg.mkPen(color=(255, 0, 255), width=3, style=QtCore.Qt.DashLine)
        # self.graphwidget.plot(precip_list4, name="Realized Data", pen=pen, symbol='+', symbolsize=2)



    def central_tendency(self, list_1, list_2, list_3):
        ct_list = []
        if not list_1:
            for x in range(12):
                ct_temp = (list_2[x] + list_3[x]) / 2
                ct_list.append(ct_temp)
        elif not list_2:
            for x in range(12):
                ct_temp = (list_1[x] + list_3[x]) / 2
                ct_list.append(ct_temp)
        elif not list_3:
            for x in range(12):
                ct_temp = (list_1[x] + list_2[x]) / 2
                ct_list.append(ct_temp)
        elif not list_3 and not list_2:
            for x in range(12):
                ct_temp = list_1[x]
                ct_list.append(ct_temp)
        else:
            for x in range(12):
                ct_temp = (list_1[x] + list_2[x] + list_3[x]) / 3
                ct_list.append(ct_temp)
        return ct_list

    def central_tendency_precip(self, list_1, list_2):
        ct_list = []
        for x in range(12):
            ct_temp = (list_1[x] + list_2[x]) / 2
            ct_list.append(ct_temp)
        return ct_list

    def prev_timespan(self, toggled_button):
        self.current_date = self.current_date - timedelta(hours=12)
        if toggled_button == self.TemperatureButton:
            self.plot_Temperatures(self.current_date)
        elif toggled_button == self.WindspeedButton:
            self.plot_Windspeed(self.current_date)
        else:
            self.plot_Precipitation(self.current_date)

    def next_timespan(self, toggled_button):
        self.current_date = self.current_date + timedelta(hours=12)
        if toggled_button == self.TemperatureButton:
            self.plot_Temperatures(self.current_date)
        elif toggled_button == self.WindspeedButton:
            self.plot_Windspeed(self.current_date)
        else:
            self.plot_Precipitation(self.current_date)

    def current_timespan(self, toggled_button):
        self.current_date = self.start_date
        if toggled_button == self.TemperatureButton:
            self.plot_Temperatures(self.start_date)
        elif toggled_button == self.WindspeedButton:
            self.plot_Windspeed(self.start_date)
        else:
            self.plot_Precipitation(self.start_date)



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
