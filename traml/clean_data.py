"""
We want to label events by source. 

We have data on the supposed times a source should appear as an event. 

Here we aim to merge the various files of transport data, 
and ultimately try to provide labels and a confidence value to each event. 
"""

import os
import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt

import obspy 
import obspy.signal.trigger as trigger
from obspy.clients.fdsn import Client

import traml.utils as utils

if __name__ == "__main__": 
    df = pd.read_csv("../traML_recognition/WienerLinien/time_schedule_explorer.csv")

    df["source"] = df.line.rename("source")
    df["start"] = pd.to_datetime(df.timeReal) + pd.Timedelta("- 120 seconds")
    df["end"] = pd.to_datetime(df.timeReal) + pd.Timedelta("+ 60 seconds")
    df = df[["source", "start", "end"]]

    df1 = pd.read_csv("./timetables/S40_times_FJB.csv")
    df1["source"] = ["s40"] * len(df1)
    df1["start"] = pd.to_datetime(df1.to_FJB_FJB) 
    df1["end"] = pd.to_datetime(df1.to_FJB_FJB) 
    df2 = pd.read_csv("./timetables/S40_times_STP.csv")
    df2["source"] = ["s40"] * len(df2)
    df2["start"] = pd.to_datetime(df2.to_STP_FJB) 
    df2["end"] = pd.to_datetime(df2.to_STP_FJB) 
    df1 = df1[["source", "start", "end"]]
    df2 = df2[["source", "start", "end"]]
    s40 = pd.concat([df1, df2, df])

    events = utils.read_events("./data/events/")
    l = utils.label_events(events,s40)

    print(l) 
