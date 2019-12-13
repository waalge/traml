"""
Utils for pulling data, processing streams, and splitting streams into events.
"""
import os
import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt

import obspy 
import obspy.signal.trigger as trigger
from obspy.clients.fdsn import Client


def name_stream(st):
    """
    Standardize naming 
    """
    return  '{0}_{1}_{2}_{3}'.format(
            st[0].stats.network,
            st[0].stats.station,
            st[0].stats.channel,
            st[0].stats.starttime.strftime('%Y-%m-%d_%H_%M_%S'))

def stream_to_events(
        st, 
        sta=15, 
        trigger_on=0.9, 
        trigger_off=0.2, 
        pre_pad=10, 
        post_pad=10,
        ):
    """
    Use the z_detect feature to distinguish events. 

    Input stream should be pre-normalizde with resource function I cant run. 

    Return list of events
    """
    fmin = 10
    fmax = 30
    st.filter('bandpass',freqmin=fmin,freqmax=fmax,corners=4)
    cft = trigger.z_detect(st[0].data, int(sta * 100)) # st[0].stats.sampling_rate))
    on_off = np.array(trigger.trigger_onset(cft, trigger_on, trigger_off)) # cast as np.array?

    #trigger.plot_trigger(st[0], cft, trigger_on, trigger_off, show=True)
    print("ON OFF TRIGGER", on_off.shape) 
    starttime = st[0].stats.starttime 
    # signals = [st.slice(starttime=starttime+ start - pre_pad, endtime= starttime + end + post_pad) for start, end in on_off]

    centered = []
    for ii in range(0,len(on_off)):
        start_eve = st[0].times()[on_off[ii][0]]
        end_eve = st[0].times()[on_off[ii][1]]

        st_eve = st.slice(starttime = starttime + start_eve - pre_pad,
                endtime = starttime + end_eve + post_pad)
        # Mid point of signal estimation 
        abs_cumsum = np.cumsum(abs(st_eve[0].data))
        idx = np.where(abs_cumsum>np.max(abs_cumsum)/2)

        ## centering the signal
        midtime = st_eve[0].stats.starttime + st_eve[0].times()[idx[0][0]]

        st_cent = st.slice(starttime = midtime - 20,
                endtime = midtime + 20)
        ## data selection
        try: 
            if np.std(st_cent[0].data) < 1.75*1e-7:
                centered.append(st_cent)
        except Exception as E:
            print(ii,E) 
    return centered 

def get_stream(starttime, endtime):
    """
    Get stream from start and end time (strings) 
    """
    starttime = obspy.UTCDateTime(starttime)
    endtime = obspy.UTCDateTime(endtime)
    client = Client(base_url='https://fdsnws.raspberryshakedata.com/')
    st = client.get_waveforms('AM', 'R10DB', '00', 'EHZ', starttime, endtime, attach_response=True)
    pre_filt = (0.005, 0.006, 30.0, 35.0)
    st = st.remove_response(output='DISP', pre_filt=pre_filt)
    return st

def write_events(events): 
    """
    Write stream to file by name. 
    """
    [st.write('./_events/{0}.sac'.format(name_stream(st)), format='SAC') for st in events]
    return 1

def read_events(directory):
    """
    Get events data
    """
    return [obspy.read(os.path.join(directory,fn)) for fn in os.listdir(directory)]
    pass 

def spectrums(events):
    """
    Turn waves to spectograms
    """
    return [sig.spectrum for sig in events]

def PCA():
    """
    Do PCA 
    """
    pass

def get_timetable(file_name): 
    """
    Interval of
    """
    df = pd.from_csv(file_name)
    pass

def label_events(events, df):
    """
    Input:
        list of streams corresponding to events.
        df of transport labels and interval start and end time expected to pass close to the sensor
        e.g     source: "u6", start:timestamp, end: timestamp. 
    """
    df = df[["source", "start", "end"]].drop_duplicates()
    sources = df["source"].drop_duplicates()
    column_names = ["name", "starttime"] + ["oh_"+source for source in sources]
    data = {"name" : [name_stream(st) for st in events],  
        "starttime" : [pd.to_datetime(str(st[0].stats.starttime)) for st in events], }
    df.interval = [pd.Interval(pd.Timestamp(start), pd.Timestamp(end)) for start, end in zip(df.start, df.end)]
    coincide = [list(set([source for source, interval in zip(df.source, df.interval) if starttime in interval])) for starttime in data["starttime"]] 
    for source in sources: 
        name = "oh_" + str(source)
        data[name] = np.array([source in co for co in coincide], dtype=float)
    df_events = pd.DataFrame(data = data) 
    return df_events
