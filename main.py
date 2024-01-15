import sys
import os
import datetime
import mysqlclient as mysql

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
from PyQt5 import QtBluetooth

# ESP32 Bluetooth Address
DEVICE_ADDRESS = "24:62:AB:D7:D1:56"

# Blootooth Device Class for connecting to
class BluetoothDevice(QObject):
    def __init__(self, parent = None):
        super(BluetoothDevice, self).__init__(parent)
        self.makeConnections()

        self.lastSyncTime = datetime.datetime.now()

    def makeConnections(self):
        self.sock = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)
        self.serviceScan = QtBluetooth.QBluetoothServiceDiscoveryAgent(self)

        self.sock.connected.connect(self.connectedToBluetooth)
        self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.error.connect(self.socketError)

        self.serviceScan.serviceDiscovered.connect(self.foundService)
        self.serviceScan.setRemoteAddress(QtBluetooth.QBluetoothAddress(DEVICE_ADDRESS))
        self.serviceScan.start()

    def socketError(self,error):
        print(self.sock.errorString())

    def connectedToBluetooth(self):
        self.sock.write('A'.encode())

    def disconnectedFromBluetooth(self):
        self.print('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        mydb = connector.connect(
                host="localhost",
                user="root",
                password="fesha4641",
                database="finalyear"
            )

        while self.sock.canReadLine():
            line = self.sock.readLine().decode('utf-8')
            
            print(line)

            if (self.lastSyncTime - datetime.datetime.now()) >= 10000:
                splitted = line.split(":")
                self.lastSyncTime = datetime.datetime.now()

                if len(splitted) > 4:
                    acpower = splitted[0]
                    dcpower = splitted[1]
                    load1power = splitted[2]
                    load2power = splitted[3]
                    load3power = splitted[4]

                    # Write to MySQL DB
                    try:
                        mycursor = mydb.cursor()

                        dt = datetime.datetime.now().split(".")[0]

                        sql = "INSERT INTO netmeter (time, solarpower, gridpower, load1, load2, load3) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (dt, dcpower, acpower, load1power, load2power, load3power)
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")

                    except Exception as e:
                        print("Error: ", e)
    
    def foundService(self, service):
        self.sock.connectToService(service)


if __name__ == "__main__":
    if sys.platform == 'darwin':
        os.environ['QT_EVENT_DISPATCHER_CORE_FOUNDATION'] = '1'

    app = QApplication(sys.argv)
    ex = BluetoothDevice()
    sys.exit(app.exec_())
