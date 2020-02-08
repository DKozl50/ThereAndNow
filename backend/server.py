from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods = ["GET"])
def index_get():
    return render_template("index.html")

@app.route('/results', methods = ["GET"])
def results_get():
    return redirect("/")

@app.route('/results', methods = ["POST"])
def results_post():

    user_id = request.form["user_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    if user_id and start_date and end_date:
        print(user_id, start_date, end_date)

        return render_template("results.html", start_date = start_date, end_date = end_date, results )
    return redirect("/")



if __name__ == "__main__":
    app.run(threaded=True)
