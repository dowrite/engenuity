#!/usr/bin/env python3

""" Adds new columns to the log file to label it with the ATT&CK 'Tactic' and 'Technique'  
    that generated the log entry.
"""

import os
import argparse
from xmlrpc.client import Boolean
import pandas as pd

def label_log(log: str, atk: str):
    
    # Convert time string to datetime
    log['_time'] = pd.to_datetime(log['_time'])
    atk['_time'] = pd.to_datetime(atk['_time'])
    
    # Ensure logs are sorted by time in Descending order
    log = log.sort_values('_time', ascending=False)
    atk = atk.sort_values('_time', ascending=False)

    # Trim log events that are outside the time of interest:
    #   1) Events more than 10s before the first execution time
    #   2) Events after the last execution time
    log.drop(log[log._time < (atk._time.iloc[-1] - pd.Timedelta(seconds=10))].index, inplace=True)
    log.drop(log[log._time > atk._time.iloc[1]].index, inplace=True)
        
    # print("After trimming irrelevant timestamps...")
    # log.info()
    # print(log['_time'])
    # atk.info()

    # Assign label to matching time events in atc_log
    log = log.merge(atk, on='_time', how='left')

    # Since atk_log execution timestamps are written after completion of the technique, we can assume 
    # log events that happened immediately before the execution timestamp is a result of the technique
    # being executed.
    log['Tactic'].fillna(method='ffill', inplace=True)
    log['Technique'].fillna(method='ffill', inplace=True)

    # print("Final log dataframe...")
    # print(log['_time'])
    return log

def import_log(log_path: str, preview: Boolean=False):
    # Load log_file and delete empty columns
    if not preview: 
        log_df = pd.read_csv(log_path) 
    else: 
        log_df = pd.read_csv(log_path, nrows=250)
    log_df.replace("", float("NaN"), inplace=True)
    log_df.dropna(how='all', axis=1, inplace=True)

    # print("Imported...")
    # print(log_df['_time'])
    return log_df

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--preview", '-p', 
        default=False, action='store_true',
        help="Just import the first 250 lines of log. Note:this might 0 useable events if the first \
            250 lines are not within the relevant timeline."
    )
    parser.add_argument(
        "splunk_log", 
        help='A csv file exported from splunk, or a directory of splunk logs with *.csv extension.'
    )
    parser.add_argument(
        "atk_log", 
        help='ATT&CK execution log file, as generated by the `get_attack_data` search in splunk'        
    )
    
    ns = parser.parse_args()
    
    # Load atk_log, taking only columns of interested
    atk_df = pd.read_csv(ns.atk_log, usecols=['_time','Tactic', 'Technique'])

    # Directory given - label all unlabeled *.csv files
    if os.path.isdir(ns.splunk_log):  
        print("\nLabeling all *.csv files in directory.")  
        files = [f for f in os.scandir(ns.splunk_log) if f.is_file()]
        logs = [f for f in files if f.name.endswith(".csv") and not f.name.startswith("LABELED_")]
        for log in logs:            
            log_df = import_log(log, ns.preview)
            log_df = label_log(log_df, atk_df)
            
            # print(atk[['_time','Technique']])
            
            # Save log to file
            [log_dir, log_name] = os.path.split(os.path.abspath(log))
            new_filename = os.path.join(log_dir, "LABELED_" + log_name)
            log_df.to_csv(new_filename)
            print("Wrote to file: " + new_filename)
    # File given
    elif os.path.isfile(ns.splunk_log):  
        log_df = import_log(ns.splunk_log, ns.preview)
        log_df = label_log(log_df, atk_df)
            
        # Save log to file
        [log_dir, log_name] = os.path.split(os.path.abspath(ns.splunk_log))
        new_filename = os.path.join(log_dir, "LABELED_" + log_name)
        log_df.to_csv(new_filename)
        # print(log_df[['_time','Technique']])
        print("Wrote to file: " + new_filename)

    else:  
        print("splunk_log must be a file or directory!" )
        return

if __name__ == "__main__":
    main()
