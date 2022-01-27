from flask import Flask,render_template,request,session,redirect
import flask
from flask_session import Session
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly
import pandas as pd
import json
import matplotlib.pyplot as plt
import json
from datetime import datetime
from pycaret.anomaly import *
import plotly.graph_objects as go
import pyautogui

app=Flask(__name__,template_folder="templates")
@app.route("/")
def index():    
    df=pd.read_csv("output5.csv")
    df["Timestamp"]=df["Timestamp"].str.split(" ")
    date=[]
    from datetime import datetime
    for i in range(len(df["Timestamp"])):
        date.append(datetime.strptime(df["Timestamp"][i][0]+df["Timestamp"][i][1],"%m/%d/%Y%H:%M:%S"))
    
    df["Time"]=date
    df=df.drop("Timestamp",axis=1)
    df1=df.tail(1000)
    fig=px.line(df1,x="Time",y="Avg_Memory_Utilization",title="Time series")
    data=df.set_index("Time")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    data['day'] = [i.day for i in data.index]
    data['day_name'] = [i.day_name() for i in data.index]
    data['day_of_year'] = [i.dayofyear for i in data.index]
    data['week_of_year'] = [i.weekofyear for i in data.index]
    data['hour'] = [i.hour for i in data.index]
    data['is_weekday'] = [i.isoweekday() for i in data.index]
    s = setup(data, session_id = 123,silent=True)
    
    iforest = create_model('iforest', fraction = 0.1)
    iforest_results = assign_model(iforest)
    iforest1=iforest_results.tail(1000)
    
    fig = px.line(iforest1, x=iforest1.index, y="Avg_Memory_Utilization", title='Avg_Memory_Utilization - UNSUPERVISED ANOMALY DETECTION', template = 'plotly_dark')
# create list of outlier_dates
    outlier_dates = iforest1[iforest1['Anomaly'] == 1].index
# obtain y value of anomalies to plot
    y_values = [iforest1.loc[i]['Avg_Memory_Utilization'] for i in outlier_dates]
    fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                name = 'Anomaly', 
                marker=dict(color='red',size=10)))
    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig=px.line(df1,x="Time",y="Avg_GPU_Usage",title="Time series")
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig = px.line(iforest1, x=iforest1.index, y="Avg_GPU_Usage",
     title='Avg_GPU_Usage - UNSUPERVISED ANOMALY DETECTION', template = 'plotly_dark')
# # create list of outlier_dates
    outlier_dates = iforest1[iforest1['Anomaly'] == 1].index
#     # obtain y value of anomalies to plot
    y_values = [iforest1.loc[i]['Avg_GPU_Usage'] for i in outlier_dates]
    fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                    name = 'Anomaly', 
                    marker=dict(color='red',size=10))) 
    graphJSON3=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig=px.line(df1,x="Time",y="Avg_Disk_ActiveTime",title="Time series")
    graphJSON4 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig = px.line(iforest1, x=iforest1.index, y="Avg_Disk_ActiveTime",
     title='Avg_Disk_ActiveTime - UNSUPERVISED ANOMALY DETECTION', template = 'plotly_dark')
# # create list of outlier_dates
    outlier_dates = iforest1[iforest1['Anomaly'] == 1].index
#     # obtain y value of anomalies to plot
    y_values = [iforest1.loc[i]['Avg_Disk_ActiveTime'] for i in outlier_dates]
    fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                    name = 'Anomaly', 
                    marker=dict(color='red',size=10))) 
    graphJSON5=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig=px.line(df1,x="Time",y="Avg_Network_Usage",title="Time series")
    graphJSON6 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig = px.line(iforest1, x=iforest1.index, y="Avg_Network_Usage",
     title='Avg_Network_Usage - UNSUPERVISED ANOMALY DETECTION', template = 'plotly_dark')
# # create list of outlier_dates
    outlier_dates = iforest1[iforest1['Anomaly'] == 1].index
#     # obtain y value of anomalies to plot
    y_values = [iforest1.loc[i]['Avg_Network_Usage'] for i in outlier_dates]
    fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                    name = 'Anomaly', 
                    marker=dict(color='red',size=10))) 
    graphJSON7=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig=px.line(df1,x="Time",y="Avg_CPU_Utilization",title="Time series")
    graphJSON8 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig = px.line(iforest1, x=iforest1.index, y="Avg_CPU_Utilization",
     title='Avg_CPU_Utilization - UNSUPERVISED ANOMALY DETECTION', template = 'plotly_dark')
# # create list of outlier_dates
    outlier_dates = iforest1[iforest1['Anomaly'] == 1].index
#     # obtain y value of anomalies to plot
    y_values = [iforest1.loc[i]['Avg_CPU_Utilization'] for i in outlier_dates]
    fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                    name = 'Anomaly', 
                    marker=dict(color='red',size=10))) 
    graphJSON9=json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)      
    
    return render_template("index.html",graphJSON=graphJSON,graphJSON1=graphJSON1,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,graphJSON6=graphJSON6,graphJSON7=graphJSON7,graphJSON8=graphJSON8,graphJSON9=graphJSON9)
    

if __name__ == "__main__" :
    app.debug=True
    app.run(host="127.0.0.1",port=5000)

