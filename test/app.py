from flask import Flask, request, jsonify, render_template,session, redirect
import databases as db
import databases as db
from datetime import date, datetime, timedelta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ACS'
@app.route("/")
def temperature_read():
    data = db.krijg_temperatuur()
    lengte = len(data)
    return render_template("temperatuur.html", thempratuur=data[::-1], lengte = lengte)

@app.route("/dash")
def dash():
    datum = date.today().strftime("%d/%m/%Y")
    datum = datum.replace('/', '-')
    return redirect(f"/dash/{datum}/A2.24")


@app.route("/dash/<datum_url>/<kamer>")
def dash2(datum_url, kamer):
    datum = datum_url.replace('-', '/')
    session['datum'] = datum
    session['kamer'] = kamer
    datum = datetime.strptime(datum, "%d/%m/%Y")

    morgen = datum + timedelta(days=1)
    gisteren = datum - timedelta(days=1)

    m = morgen.strftime("%d/%m/%Y").replace('/', '-')
    g = gisteren.strftime("%d/%m/%Y").replace('/', '-')

    kamerS = db.krijg_kamers()
    return render_template("dashboard.html", gisteren = g, morgen = m, kamer = kamer, kamerS = kamerS, datum_url = datum_url)


@app.route("/temperature", methods=["POST"])
def temperature():
    """An endpoint accepting a temperature reading"""
    data = request.json  # temperature reading
    datum = date.today().strftime("%d/%m/%Y")
    tijd = datetime.now().strftime("%H:%M:%S")

    print(data)
    print(datum)
    print(tijd)
    

    # if temperature exceeds a certain treshold (e.g. 20 °C),
    # reply with a warning so the client can set the red LED
    if data > 20:
        response = "lamp_aan"

    # else just reply all is well and maybe signal that
    # the red LED should be switched off
    else:
        response = "lamp_uit"
    sensor_data = db.SensorData(sensorid = 1, luchttemperatuur = data, datum = datum, tijd = tijd, stralingstemperatuur = random.randint(18,22))
    sensor_data.save()
    
    return jsonify(response)

@app.route('/krijg-temperatuur-json')
def krijg_temperatuur_json():
    temperatures = db.krijg_temperatuur_grafiek(session['datum'], session["kamer"])
    result = []
    for temp in temperatures:
        # parse the year string into a datetime object
        dt = datetime.strptime(temp[0], '%H:%M:%S')
        # create a dictionary with the datetime object and temperature values
        d = {'y': dt.strftime('%H:%M'), 'a': temp[1], 'b': temp[2]}
        result.append(d)
    session.clear()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)