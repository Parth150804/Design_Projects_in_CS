import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save, stock_df

def get_data(sym, x):
    df = stock_df(symbol = sym, from_date = date(2024-x, 1, 1), to_date = date(2024, 1, 1), series = "EQ")
    return df

def write_to_csv(data, filename):
    data.to_csv(filename, index=False)

def write_to_txt(data, filename):
    data.to_csv(filename, index=False, sep='\t')

def write_to_binary(data, filename):
    data.to_pickle(filename)

def write_to_parquet(data, filename):
    data.to_parquet(filename)

def benchmark_write_time_and_size(data, write_function, filename):
    start_time = time.time()
    write_function(data, filename)
    end_time = time.time()

    file_size = os.path.getsize(filename)

    return end_time - start_time, file_size/1000000

def plot_comparison(results, labels):
    time_taken, file_size = zip(*results)

    bar_width = 0.35 

    X_axis = np.arange(len(labels))

    plt.figure(figsize=(10, 6))

    plt.bar(X_axis - bar_width/2, time_taken, width=bar_width, color='blue', alpha=0.7, label='Time Taken')

    plt.bar(X_axis + bar_width/2, file_size, width=bar_width, color='orange', alpha=0.7, label='File Size')
    plt.xticks(X_axis, labels)
    plt.xlabel('File Formats')
    plt.ylabel('Time Taken(in sec) and File Size(in MB)')
    plt.title('Comparison of File Formats')
    plt.legend()
    plt.show()

def main():
    symbol = input()
    years = int(input())      

    data = get_data(symbol, years)

    results = [
        benchmark_write_time_and_size(data, write_to_csv, '${SYMBOL}.csv'),
        benchmark_write_time_and_size(data, write_to_txt, '${SYMBOL}.txt'),
        benchmark_write_time_and_size(data, write_to_binary, '${SYMBOL}.pkl'),
        benchmark_write_time_and_size(data, write_to_parquet, '${SYMBOL}.gzip'),
    ]

    file_formats = ['CSV', 'TXT', 'Binary', 'Parquet']

    plot_comparison(results, file_formats)

if __name__ == "__main__":
    main()

