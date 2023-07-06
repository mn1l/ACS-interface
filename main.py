from website import create_app
import serial
import re
import click
from flask.cli import with_appcontext
from website.models import Data
from website import db

app = create_app()

@app.cli.command("read_sensor_values")
def read_sensor_values():
    ser = serial.Serial('COM7',115200)
    RE_MEASUREMENTS = re.compile(r"(\d+\.\d+)C, (\d+\.\d+)%, (\d+\.\d+)hPa\r\n")

    while True:
        line = ser.readline().decode("utf-8")
        result = RE_MEASUREMENTS.match(line)
        temp = float(result.group(1))
        humi = float(result.group(2))
        pres = float(result.group(3))

        data = Data(
            luchttemp=temp, 
            opptemp=0.0, 
            luchtvochtigheid=humi, 
            luchtdruk=pres,
        )
        db.session.add(data)
        db.session.commit()

# Read ESP serial: flask --app main read_sensor_values
# Server: flask --app main run

# app.cli.add_command(read_sensor_values)

# if __name__ == '__main__':
#     app.run(debug=True)