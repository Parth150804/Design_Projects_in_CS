from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    plot_option = request.form['plot_option']
    if plot_option == 'single':
        return plot_single_stock()
    else:
        return plot_multiple_stocks()

@app.route('/plot_single', methods=['POST'])
def plot_single_stock():
    stock_symbol = request.form['stock_symbol']
    time_scale = request.form['time_scale']

    if time_scale == 'daily':
        data = main.get_data(stock_symbol, 1)
        main.write_to_csv(data, '${SYMBOL}.csv')
        df = pd.read_csv('${SYMBOL}.csv')
        stock_data = df[df['SYMBOL'] == stock_symbol]
        if stock_data.empty:
            return 'Invalid stock symbol'
        x = stock_data['DATE']
        y = stock_data['LTP']

    elif time_scale == 'weekly':
        data = main.get_data(stock_symbol, 2)
        main.write_to_csv(data, '${SYMBOL}.csv')
        df = pd.read_csv('${SYMBOL}.csv')
        stock_data = df[df['SYMBOL'] == stock_symbol]
        if stock_data.empty:
            return 'Invalid stock symbol'
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.drop(columns=['SERIES', 'SYMBOL'], inplace=True)
        weekly_data = df.resample('W', on='DATE').mean()

        x = weekly_data.index
        y = weekly_data['LTP']

    elif time_scale == 'monthly':
        data = main.get_data(stock_symbol, 5)
        main.write_to_csv(data, '${SYMBOL}.csv')
        df = pd.read_csv('${SYMBOL}.csv')
        stock_data = df[df['SYMBOL'] == stock_symbol]
        if stock_data.empty:
            return 'Invalid stock symbol'
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.drop(columns=['SERIES', 'SYMBOL'], inplace=True)
        monthly_data = df.resample('M', on='DATE').mean()

        x = monthly_data.index
        y = monthly_data['LTP']

    else:
        data = main.get_data(stock_symbol, 10)
        main.write_to_csv(data, '${SYMBOL}.csv')
        df = pd.read_csv('${SYMBOL}.csv')
        stock_data = df[df['SYMBOL'] == stock_symbol]
        if stock_data.empty:
            return 'Invalid stock symbol'
        df['DATE'] = pd.to_datetime(df['DATE'])
        df.drop(columns=['SERIES', 'SYMBOL'], inplace=True)
        yearly_data = df.resample('Y', on='DATE').mean()

        x = yearly_data.index
        y = yearly_data['LTP']

    trace = go.Scatter(x=x, y=y, mode='lines+markers', name=stock_symbol)
    layout = go.Layout(title=f'Stock Price of {stock_symbol} ({time_scale.capitalize()})')
    fig = go.Figure(data=[trace], layout=layout)

    gJSON = fig.to_json()

    return render_template('plot_single.html', graphJSON=gJSON)

@app.route('/plot_multiple', methods=['POST'])
def plot_multiple_stocks():
    stock_symbols = []
    for i in range(1, 5):
        stock_symbols.append(request.form['stock_symbol_' + str(i)])

    time_scale = request.form['time_scale']

    data = []
    x = []
    y = []
    if time_scale == 'daily':
        for i in range(4):
            data.append(main.get_data(stock_symbols[i], 1))
            main.write_to_csv(data[i], '${SYMBOL}.csv')
            df = pd.read_csv('${SYMBOL}.csv')
            stock_data = df[df['SYMBOL'] == stock_symbols[i]]
            if stock_data.empty:
                return 'Invalid stock symbol'
            x.append(stock_data['DATE'])
            y.append(stock_data['LTP'])

    elif time_scale == 'weekly':
        for i in range(4):
            data.append(main.get_data(stock_symbols[i], 2))
            main.write_to_csv(data[i], '${SYMBOL}.csv')
            df = pd.read_csv('${SYMBOL}.csv')
            stock_data = df[df['SYMBOL'] == stock_symbols[i]]
            if stock_data.empty:
                return 'Invalid stock symbol'
            df['DATE'] = pd.to_datetime(df['DATE'])
            df.drop(columns=['SERIES', 'SYMBOL'], inplace=True)
            weekly_data = df.resample('W', on='DATE').mean()
            x.append(weekly_data.index)  
            y.append(weekly_data['LTP'])

    elif time_scale == 'monthly':
        for i in range(4):
            data.append(main.get_data(stock_symbols[i], 5))
            main.write_to_csv(data[i], '${SYMBOL}.csv')
            df = pd.read_csv('${SYMBOL}.csv')
            stock_data = df[df['SYMBOL'] == stock_symbols[i]]
            if stock_data.empty:
                return 'Invalid stock symbol'
            df['DATE'] = pd.to_datetime(df['DATE'])
            df.drop(columns=['SERIES', 'SYMBOL'], inplace=True)
            monthly_data = df.resample('M', on='DATE').mean()
            x.append(monthly_data.index)
            y.append(monthly_data['LTP'])

    else:
        for i in range(4):
            data.append(main.get_data(stock_symbols[i], 10))
            main.write_to_csv(data[i], '${SYMBOL}.csv')
            df = pd.read_csv('${SYMBOL}.csv')
            stock_data = df[df['SYMBOL'] == stock_symbols[i]]
            if stock_data.empty:
                return 'Invalid stock symbol'
            df['DATE'] = pd.to_datetime(df['DATE'])
            df.drop(columns=['SERIES', 'SYMBOL'], inplace=True)
            yearly_data = df.resample('Y', on='DATE').mean()

            x.append(yearly_data.index)
            y.append(yearly_data['LTP'])

    traces = []

    for i in range(4):  
        trace = go.Scatter(
            x=x[i],  
            y=y[i],  
            mode='lines+markers',
            name=stock_symbols[i]  
        )
        traces.append(trace)

    layout = go.Layout(
        title='Stock Prices of Multiple Stocks'
    )

    fig = go.Figure(data=traces, layout=layout)

    gJSON = fig.to_json()

    return render_template('plot_multiple.html', graphJSON=gJSON)


if __name__ == '__main__':
    app.run(debug=True)
