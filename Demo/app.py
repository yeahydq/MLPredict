from flask import Flask, render_template
import pandas as pd
from flask import Flask, render_template

df = pd.read_csv('./data/economic-indicators.csv',parse_dates=[['Year', 'Month']])
length = len(df)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', length=length,
                           dataframe=df.to_html())

@app.route('/data')
def data():
    return render_template('data.html')


if __name__ == '__main__':
    app.run(debug=True, port=5957)
