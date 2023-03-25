from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return "Hello World"

@app.route('/stockAnalysis', methods=["GET", "POST"])
def stockAnalysis():
    if request.method == "POST":
        print(request.form["stock"])
        print(request.form["startDate"])
        print(request.form["endDate"])

        # Put stock analysis method here
        # put
        return "STOCKS are inputed";
    else:
        return render_template("InputStocks.html");


if __name__ == '__main__':
    app.run()
