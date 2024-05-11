from flask import Flask, render_template

# __name__ is a special var
app = Flask(__name__)


# allows user to go straight to home website
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    temperature = 23
    return {'station': station,
            'date': date,
            'temperature': temperature}


# will only run this app when this script is activated directly
if __name__ == "__main__":
    app.run(debug=True)
