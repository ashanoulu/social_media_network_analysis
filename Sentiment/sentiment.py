import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import *
import ternary
import numpy

data = read_csv(".\..\posts3.csv")

tweets = data['text'].tolist()

data_rows = []
file_header = ['a', 'b', 'c']

analyzer = SentimentIntensityAnalyzer()

progress = 0

for sentence in tweets:
    data_row: list = []

    vs = analyzer.polarity_scores(sentence)

    data_row.append(vs['neg'])
    data_row.append(vs['neu'])
    data_row.append(vs['pos'])
    # data_row.append(vs['compound'])

    data_rows.append(data_row)
    data_row = []
    progress += 1
    print(progress)
    with open('sentiments.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_header)
        writer.writerows(data_rows)

arr = numpy.array(data_rows)
# new_arr = arr*100
# test_arr = [(0.05, 0.9, 0.05)]

scale: int = 1
fontsize = 8
offset = 0.07

figure, tax = ternary.figure(scale=scale)
tax.set_title("Sentiment", fontsize=20)
tax.boundary(linewidth=0.5)
tax.gridlines(multiple=0.05, color="black")
tax.left_axis_label("Positive", fontsize=fontsize, offset=offset)
tax.right_axis_label("Neutral", fontsize=fontsize, offset=offset)
tax.bottom_axis_label("Negative", fontsize=fontsize, offset=-0.1)

tax.scatter(arr, marker='.', color='green', label="points")
tax.ticks(axis='lbr', linewidth=0.8, multiple=1)

tax.show()

tax.savefig('filename.pdf')
