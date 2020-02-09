from flask import Flask, render_template, request, redirect
from json import loads

app = Flask(__name__)


@app.route('/', methods = ["GET"])
def index_get():
    return render_template("index.html")

@app.route('/results', methods = ["GET"])
def results_get():
    return redirect("/")

@app.route('/results', methods = ["POST"])
def results_post():

    user_id = request.form.get("user_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    cost = request.form.get("end_date")
    country = request.form.get("country")

    if user_id and start_date and end_date:

        data = [[{'name' : ' One day in Austria', 'dates' : '08:00 09.02.2020 - 23:00 09.02.2020', 'cost': '6969$'},
             {'type': 'flight',
              'name': 'Самолет в Австрию',
              'time_in': '08:00',
              'time_out': '11:30'},
             {'type': 'hotel',
              'name': 'Заселение в отель Nice Plaza',
              'time_in': '12:15',
              'time_out': '13:00'},
             {'type': 'food',
              'name': 'Обед в Eat Place 1',
              'time_in': '13:15',
              'time_out': '13:50'},
             {'type': 'sightseing',
              'name': 'Музей павла семнадцатого',
              'time_in': '14:00',
              'time_out': '15:00'},
             {'type': 'sightseing',
              'name': 'Парк синий',
              'time_in': '15:30',
              'time_out': '17:00'},
             {'type': 'souvenirs',
              'name': 'Торговая площадь',
              'time_in': '17:30',
              'time_out': '18:00'},
             {'type': 'food',
              'name': 'Ужин в Eat Place 14',
              'time_in': '18:15',
              'time_out': '19:00'},
             {'type': 'hotel',
              'name': 'Выселение из отеля',
              'time_in': '19:10',
              'time_out': '19:30'},
             {'type': 'flight',
              'name': 'Аэропорт и вылет из австрии',
              'time_in': '20:15',
              'time_out': '23:00'}]]

        return render_template("results.html", data = data, start_date = start_date, end_date = end_date, cost = cost, country = country)
    return redirect("/")

@app.route('/journey', methods = ["POST"])
def journey_post():

    data = request.form.get("data")

    if data:
        data = loads(data.replace("'", '"'))
        return render_template("journey.html", data = data)
    return redirect("/")

if __name__ == "__main__":
    app.run(threaded=True, host = "0.0.0.0", port = "80")
