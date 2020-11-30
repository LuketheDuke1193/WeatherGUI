import sys
from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from datetime import datetime
import ForecastData

from MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.graphwidget.setBackground('w')
        self.graphwidget.setTitle("Temperatures Forecasted")
        self.plot_Temperatures(datetime.now())

    def plot(self, hour, temperature):
        pen = pg.mkPen(color=(255,0,0), width=2)
        self.graphwidget.plot(hour, temperature, pen=pen, symbol='+', symbolsize=2)

    def plot_Temperatures(self, date):
        forecast = ForecastData.Get_Temp_Forecasts(date)
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        temp_list1 = forecast.list[0].temp_list()
        self.graphwidget.plot(temp_list1, pen=pen, symbol='+', symbolsize=2)
        pen = pg.mkPen(color=(0, 0, 255), width=2)
        temp_list2 = forecast.list[1].temp_list()
        self.graphwidget.plot(temp_list2, pen=pen, symbol='+', symbolsize=2)
        pen = pg.mkPen(color=(0, 255, 0), width=2)
        temp_list3 = forecast.list[2].temp_list()
        self.graphwidget.plot(temp_list3, pen=pen, symbol='+', symbolsize=2)
        ct_list = self.central_tendency(temp_list1, temp_list2, temp_list3)
        pen = pg.mkPen(color=(0, 0, 0), width=2.5, style=QtCore.Qt.DashLine)
        self.graphwidget.plot(ct_list, pen=pen, symbol='+', symbolsize=2)

    def central_tendency(self, list_1, list_2, list_3):
        ct_list = []
        for x in range(12):
            ct_temp = (list_1[x] + list_2[x] + list_3[x]) / 3
            ct_list.append(ct_temp)
        return ct_list


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
