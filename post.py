import Adafruit_BMP.BMP085 as BMP085
from light_sensor import TSL2561
from dallas_sensors import get_dallas_temps
import requests
from requests.auth import HTTPBasicAuth
import smtplib
import textwrap
import os

data = {}


def post(sn, d):
    payload = {"sensor_name": sn, "data": d}

    try:
        requests.post('http://crox.io/sensor/sensorsapi/',
                         auth=HTTPBasicAuth('aquaman', 'aquaponics'), data=payload)
    except Exception, e:
        TEXT = "An error has occured when sending the data to the server. The Exception was this: {0}".format(e)
        sendMail('Aquaman@Aquaponics.com', 'a.field738@gmail.com', 'Error has occured', TEXT)
        raise e

def sendMail(FROM,TO,SUBJECT,TEXT):
    """this is some test documentation in the function"""
    message = textwrap.dedent("""\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (FROM, TO, SUBJECT, TEXT))
    # Send the mail
    # import ipdb; ipdb.set_trace()
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('os.environ["email"]', 'os.environ["password"]')
    server.sendmail(FROM, TO, message)
    server.quit()


def post_sensor_data():
    dallasTemps = get_dallas_temps()

    # Dallas Sensors
    sump_temp = dallasTemps['sump_tank']
    data.update({'ST': sump_temp})

    fish_temp = dallasTemps['fish_tank']
    data.update({'FT': fish_temp})

    grow_temp = dallasTemps['grow_bed']
    data.update({'GT': grow_temp})

    # Air Sensor
    air_Sensor = BMP085.BMP085()
    
    air_temp = air_Sensor.read_temperature()
    data.update({'AT': air_temp})

    air_press = air_Sensor.read_pressure()
    data.update({'AP': air_press})

    # Light Sensor
	try:
		light_sensor = TSL2561()
		light_lux = light_sensor.readLux()
    		data.update({'LS': light_lux})
	except Exception, e:
		pass

    # import ipdb; ipdb.set_trace()
    for x in data:
        post(x, data[x])
	print x
	print data[x]


if __name__ == '__main__':
    post_sensor_data()
