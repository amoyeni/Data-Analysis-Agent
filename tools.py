import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
from langchain.tools import Tool

data = pd.read_csv("/Users/adammoore/Documents/GitHub/Data-Analysis-Agent/data/coffeeSales.csv", parse_dates=["date"])

def query_data(expression:str):
    #return dataframe rows that match pandas query string
    try:
        df = data.query(expression).copy()
        return df.to_dict(orient="records")[:50]
    except Exception as e:
        return f"Query error: {e}"

#Summarise
def quick_stats(column:str, metric:str):
    if metric=="sum": val = data[column].sum()
    elif metric=="avg": val = data[column].mean()
    else:
        return "Metric must me sum or avg"
    return {metric:val}


#plot graph
def plot_timeseries(column: str):
    plt.figure()
    data.groupby("date")[column].sum().plot()
    path = f"charts/{column}_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
    os.makedirs("charts", exist_ok=True)
    plt.title(column + "over time")
    plt.savefig(path)
    plt.close()
    return path

#Save log
def save_log(text:str):
    os.makedirs("logs", exist_ok=True)
    fname = f"logs/{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    open(fname,"w").write(text)
    return fname

tools = [
    Tool("query_data", query_data, "run pandas query on data"),
    Tool("quick_stats", quick_stats, "Get Sum or average of a column"),
    Tool("plot_timeseries", plot_timeseries, "Create chart"),
    Tool("save_log", save_log, "save chat transcripts")]




    