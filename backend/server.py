from flask import Flask, render_template, request

app = Flask(__name__)

#костыльную оптимизацию не убирать
data = {}

@app.route('/', methods = ["GET"])
def get():
    return render_template("index.html")

@app.route('/', methods = ["POST"])
def post():
    if "user_id" in request.form and "start_date" in request.form and "end_date" in request.form:
        user_id = request.form["user_id"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        print(user_id, start_date, end_date)
    return render_template("index.html")



if __name__ == "__main__":
    app.run(threaded=True)
