import time
import serial
import serial.tools.list_ports

# global variables for module
startMarker = 60
endMarker = 62
startTime = 0


def valToArduino(emoStateTuple):
    sendStr = "%s,%s,%s, %s, %s,%s,%s, %s, %s,%s,%s, %s" % emoStateTuple
    print "SENDSTR %s" % (sendStr)
    sendToArduino(sendStr)

# ========================

def setupSerial():

    global ser, startTime

    # NOTE the user must ensure that the serial port and baudrate are correct
    print "==================================================================="
    # Find live ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print p
        for index in range(0, 20):
            str1 = "COM%d" % (index)
            if str1 in p[1]:
                serPort = str1
            index += 1

    baudRate = 9600
    ser = serial.Serial(serPort, baudRate)
    print "Serial port " + serPort + " opened  Baudrate " + str(baudRate)
    time.sleep(2);

# ========================

def closeSerial():

    global ser
    if 'ser' in globals():
        ser.close()
        print "Serial Port Closed"
    else:
        print "Serial Port Not Opened"

# ========================

def sendToArduino(sendStr):

    global startMarker, endMarker, ser

    ser.write(chr(startMarker))
    ser.write(sendStr)
    ser.write(chr(endMarker))

# ===========================

def sendToArduinoLeap(sendStr):

    ser.write(sendStr)
    waitForArduino()
    print sendStr

# ===========================

def recvFromArduino(timeOut):  # timeout in seconds eg 1.5

    global startMarker, endMarker, ser

    dataBuf = ""
    x = "z"  # any value that is not an end- or startMarker
    byteCount = -1
    # to allow for the fact that the last increment will be one too many
    startTime = time.time()
    # ~ print "Start %s" %(startTime)

    # wait for the start marker
    while ord(x) != startMarker:
        if time.time() - startTime >= timeOut:
            return('<<')
        x = ser.read()

    # save data until the end marker is found
    while ord(x) != endMarker:
        if time.time() - startTime >= timeOut:
            return('>>')
        if ord(x) != startMarker:
            dataBuf = dataBuf + x
        x = ser.read()

    return(dataBuf)

# ============================


def waitForArduino():

    # wait until the Arduino sends'Arduino Ready'-allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are
    # discarded

    print "Waiting for Arduino to reset"

    msg = ""
    while msg.find("Arduino is ready") == -1:

        msg = recvFromArduino(10)

        print msg
        print
