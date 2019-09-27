#!/usr/bin/env python

import sys
import traceback 

# pyqt5 libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtNetwork import QUdpSocket, QHostAddress

# core libraries
import numpy as np
import time
import os
from os.path import basename


# I2C bus=1, Address=0x40
sht = SHT20(1, 0x40)


from time import gmtime, strftime, localtime




##########################
#      Global vars       #
##########################




class PD(QMainWindow):

    def quitProgram(self):
        PD.close()
        
    def __init__(self, parent=None):
        super(PD, self).__init__()
        self.initUI()

    def initUI(self):
        self.showFullScreen()

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setFixedSize(480, 800)
   
        self.setStyleSheet("background-color:black;  color: white;")
        
 
        self.timeLabel = QLabel("", self)
        self.timeLabel.setGeometry(40, 80, 480, 150)
        self.timeLabel.setAlignment(Qt.AlignLeft)
        labelFont = QFont("Calibri", 60, QFont.Bold) 
        self.timeLabel.setFont(labelFont)
        
        self.dateLabel = QLabel("", self)
        self.dateLabel.setGeometry(40, 180, 480, 100)
        self.dateLabel.setAlignment(Qt.AlignLeft)
        labelFont = QFont("Calibri", 24) 
        self.dateLabel.setFont(labelFont)
 
        self.tempIcon = QLabel(self)
        pixmap = QPixmap('T_icon.png')
        pixmap = pixmap.scaledToWidth(125)
        pixmap = pixmap.scaledToHeight(125)
        self.tempIcon.setPixmap(pixmap)
        self.tempIcon.setGeometry(40, 270, 125, 125)
        self.tempLabel = QLabel("25.6°C", self)
        self.tempLabel.setGeometry(180, 290, 480, 150)
        self.tempLabel.setAlignment(Qt.AlignLeft)
        labelFont = QFont("Calibri", 50, QFont.Bold) 
        self.tempLabel.setStyleSheet("color: red")
        self.tempLabel.setFont(labelFont)
        
        
        self.humIcon = QLabel(self)
        pixmap2 = QPixmap('H_icon.png')
        pixmap2 = pixmap2.scaledToWidth(125)
        pixmap2 = pixmap2.scaledToHeight(125)
        self.humIcon.setPixmap(pixmap2)
        self.humIcon.setGeometry(40, 405, 125, 125)
        self.humLabel = QLabel("78.6%", self)
        self.humLabel.setGeometry(180, 425, 480, 150)
        self.humLabel.setAlignment(Qt.AlignLeft)
        labelFont = QFont("Calibri", 50, QFont.Bold) 
        self.humLabel.setStyleSheet("color: #2194f3")
        self.humLabel.setFont(labelFont)
        
        
        self.heatIcon = QLabel(self)
        pixmap3 = QPixmap('HI_icon.png')
        pixmap3 = pixmap3.scaledToWidth(125)
        pixmap3 = pixmap3.scaledToHeight(125)
        self.heatIcon.setPixmap(pixmap3)
        self.heatIcon.setGeometry(40, 535, 125, 125)
        self.heatLabel = QLabel("78.6", self)
        self.heatLabel.setGeometry(180, 555, 480, 150)
        self.heatLabel.setAlignment(Qt.AlignLeft)
        labelFont = QFont("Calibri", 50, QFont.Bold) 
        self.heatLabel.setStyleSheet("color: #00b04f")
        self.heatLabel.setFont(labelFont)
        
        
        
        
        
        
        self.quitBtn = QPushButton('Quit', self)
        self.quitBtn.clicked.connect(self.quitProgram)
        self.quitBtn.resize(self.quitBtn.sizeHint())
        self.quitBtn.setStyleSheet("background-color: gray")
        self.quitBtn.setGeometry(360, 700, 50, 50)
        
        self.timeLabel.show()
        self.dateLabel.show()
        self.tempIcon.show()
        self.humIcon.show()
        self.heatIcon.show()
        self.tempLabel.show()
        self.humLabel.show()
        self.heatLabel.show()
        self.quitBtn.show()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeTime)
        self.timer.start(1000)
        
        
    def changeTime(self):
        self.timer.setInterval(1000)
        
        
        # Get time
        time_now = strftime("%I:%M", localtime())
        time_all_now = strftime("%I:%M:%S", localtime())
        hour_now = strftime("%H", localtime())
        hour_now = int(hour_now)
        if hour_now < 12:
            time_now = time_now + " AM"
        else:
            time_now = time_now + " PM"

        # Get date
        date_now = strftime("%b. %d, %Y %A", localtime())


        
        try:
            # Get T and H
            TC = sht.temperature().C
            H = sht.humidity().RH
            #TC = 25.0
            #H = 85.0
            
            # Tc to Tf
            T = (TC * 9.0/5.0) + 32.0
            
            # Get HIf
            c1 = 42.379
            c2 = 2.04901523
            c3 = 10.14333127
            c4 = 0.22475541
            c5 = 6.83783 * (10 ** -3)
            c6 = 5.481717 * (10 ** -2)
            c7 = 1.22874 * (10 ** -3)
            c8 = 8.5282 * (10 ** -4)
            c9 = 1.99 * (10 ** -6)
            HIF = -c1+(c2*T)+(c3*H)-(c4*T*H)-(c5*T*T)-(c6*H*H)+(c7*T*T*H)+(c8*T*H*H)-(c9*T*T*H*H)
            
            # Get HIc
            HIC = (HIF - 32.0) * 5.0/9.0 
            

            




            # Set time
            self.timeLabel.setText(time_now)
            
            # Set date
            self.dateLabel.setText(date_now)
            
            
            # Set T
            self.tempLabel.setText(str(round(TC,1)) + "°C")
            
            # Set H
            self.humLabel.setText(str(round(H,1)) + "%")

            # Set HI
            self.heatLabel.setText(str(round(HIC,1)) + "°C")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        

   




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    PD = PD()
    PD.show()

    sys.exit(app.exec_())




