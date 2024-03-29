from datetime import datetime
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib
matplotlib.use('Agg')
# import psycopg2

from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)

# Possible way to connect to a postgres database

# conn = psycopg2.connect(host=""
#                         , user="postgres", password="", dbname="", port=)

## Generate DQ Report by loading data and calling ProfileReport
def generate_report(min):
    # Example Sample data 
    # df = pd.DataFrame(np.random.rand(100, 6), columns=["a", "b", "c", "d", "e", "f"])

    # Data saved as pickle file and loaded in as pandas dataframe
    df = pd.read_pickle('data.pick').convert_dtypes(convert_integer=False)

    # Instantiate the report class
    profile_max = ProfileReport(df,
                        config_file="config.json",
                        # dark_mode=True,
                        title="Data Quality Dashboard DEMO", 
                        infer_dtypes= False,
                        lazy=True,
                        # typeset=typesets,
                        # explorative=True,
                        # config_file="report_req.yml",
                        )

    # Save the Report as HTML and JSON in static/report
    profile_max.to_file("static/report/report_max.html")
    profile_max.to_file("static/report/report_max.json")
    

@app.route("/")
def home(): 
    # Possible code to use to fetch data from postgres db
    # with connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute("Select * from model limit 10")
    #         ex = cursor.fetchone()

    # Possible index template to return here 
    # return render_template("index.html")

    # Directly load the loading file, arguments can be passed here to html
    return render_template('loading.html', min = False) 

@app.route("/report", methods=["POST"])
def target():
	# You could do any information passing here if you want (i.e Post or Get request)
	min = request.form["min"]
	# This is where the loading screen will be.
	# ( You don't have to pass data if you want, but if you do, make sure you have a matching variable in the html i.e {{my_data}} )
	return render_template('loading.html', min = min)    

# This is where the time-consuming generate report process, sql queries, etc. can take place
@app.route("/processing")
def processing():
	    # In this case, the data was passed as a get request as you can see at the bottom of the loading.html file
    if request.args.to_dict(flat=False)['data'][0] == 'False':
        # Possible code to fetch data passed as get request
		# data = str(request.args.to_dict(flat=False)['data'][0])
        generate_report(min=False)
        return redirect(url_for("get_max_html_report"))
    else:
        # Since no index.html is used to give the user an option, this section will never be executed
        generate_report(min=True)
        return redirect(url_for("get_min_html_report"))
    
	# You can return a success/fail page here or whatever logic you want

    
# Possible implementeation of a record getter 
# @app.route("/api/records")
# def get_records():
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute("Select * from model limit 10")
#             ex = cursor.fetchone()
#     return {"example": ex}


# @app.route("/report/min/html")
# def get_min_html_report():
#     return app.send_static_file("report/report_min.html")

# Return the static html report file, possible for different report types (min or max) 
@app.route("/report/max/html")
def get_max_html_report():
    return app.send_static_file("report/report_max.html")

# @app.route("/report/min/json")
# def get_min_json_report():
#     return app.send_static_file("report/report_min.json")

# Return the static json report file, possible for different report types (min or max) 
@app.route("/report/max/json")
def get_max_json_report():
    return app.send_static_file("report/report_max.json")
