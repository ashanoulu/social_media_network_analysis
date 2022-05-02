import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    counts = pd.read_csv('G:\\test\\count.csv')
    counts.hist()
    plt.show()


if __name__ == "__main__":
    main()