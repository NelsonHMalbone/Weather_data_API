from flask import Flask, render_template
import pandas as pd


# __name__ is a special var
app = Flask(__name__)

# load data from sheet for table
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
# only to show certain columns
stations = stations[['STAID', 'STANAME                                 ']]

# allows user to go straight to home website
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {'station': station,
            'date': date,
            'temperature': temperature}


# function for another one station for all dates
@app.route("/api/v1/<station>")
def all_data(station):
    filename_1 = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename_1, skiprows=20, parse_dates=["    DATE"])
    # giving user all the data
    result = df.to_dict(orient="records")
    return result

# function for another one for just the year
# will have to add a sub dirctly as of right now "/api/v1/<station>/<date>" this will clash but if
# add "/api/v1/<year>/<station>/<date>" it wont affect anything
@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename_1 = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename_1, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient='records')
    return result

# will only run this app when this script is activated directly
if __name__ == "__main__":
    app.run(debug=True)
