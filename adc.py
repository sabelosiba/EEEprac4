import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time
import threading
import datetime

count = 0
rate = 0.0
ldr = None
temp_read = None
s_time =0

def setup_GPIO():
    global temp_read
    global ldr
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    temp_read = AnalogIn(mcp, MCP.P1)
    ldr = AnalogIn(mcp, MCP.P3)
    #print("Raw ADC Value: ", chan.value)

    #print("ADC Voltage: " + str(chan.voltage) + "V")

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(22, GPIO.FALLING, callback=press_button, bouncetime=100)

def press_button(channel):
    print("button pressed")
    global rate
    global count
    count += 1

    if count==1:
        rate = 10.0
    if count==2:
        rate = 5.0
    if count==3 :
        rate = 1.0
        count = 0
    #print("The rate of sampling is : " + rate + "seconds")
    #output_line =  ("Runtime","Temp Reading", "Temp", "Light Reading")
    #print("{0: <20} {1: <20} {2: <20}".format(*output_line))

def threading_():
    thread = threading.Timer(rate, threading_)
    thread.daemon = True
    thread.start()

    rate_time =int( time.time() - s_time )

    runtime = str(rate_time) + "s"
    temp_Read = temp_read.value
    temp = str( round( (temp_read.voltage - 0.5)/0.01, 2 ) ) + " C"
    light_Read = ldr.value

    print("{0:<20} {1:<20} {2:<20} {3:<20}".format(runtime , temp_Read , temp , li$

if __name__ == "__main__":
    try:
        setup_GPIO()
        s_time = time.time()
        print("The rate of sampling is : " + str(rate) + "seconds")
        output_line =  ("Runtime","Temp Reading", "Temp", "Light Reading")
        print("{0: <20} {1: <20} {2: <20} {3: <20}".format(*output_line))
        threading_()
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting gracefully")
        GPIO.cleanup()
    except Exception as e:
        print(e)
        GPIO.cleanup()
    finally:
        GPIO.cleanup()


