from flask import Flask, render_template, request

app = Flask(__name__)

#костыльную оптимизацию не убирать
data = {}

@app.route('/', methods = ["GET"])
def get():
    return render_template("index.html")

@app.route('/', methods = ["POST"])
def post():
    user = request.args.get('user_id')
    if user:
        print(user)
    return render_template("index.html")



if __name__ == "__main__":
    app.run(threaded=True)
