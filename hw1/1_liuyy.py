import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from matplotlib.colors import Normalize

def calc_raw(x): # 计算一行的最大值、最小值、平均值和标准差
    max_value = x[0]
    min_value = x[0]
    mean_value = 0.0
    n = 0
    M2 = 0.0
    for value in x:
        if value > max_value:
            max_value = value
        elif value < min_value:
            min_value = value
        n += 1
        delta = value - mean_value
        mean_value += delta / n
        delta2 = value - mean_value
        M2 += delta * delta2
    std_value = (M2 / n) ** 0.5
    return max_value, min_value, mean_value, std_value    

def calc_array(data): # 计算每一行的最大值、最小值、平均值和标准差
    row_max, row_min, row_mean, row_std = [], [], [], []
    for row in data:
        max_value, min_value, mean_value, std_value = calc_raw(row)
        row_max.append(max_value)
        row_min.append(min_value)
        row_mean.append(mean_value)
        row_std.append(std_value)
    return np.array(row_max), np.array(row_min), np.array(row_mean), np.array(row_std)

def main():
    # read the FITS file and display the image
    with fits.open('sdo_image.fits') as hdul:
        image = hdul[0].data
    plt.imshow(image, origin="lower", cmap='gray', norm=Normalize(0.04, 0.98))
    # plt.savefig('output1.png', dpi=100)
    plt.show()

    # calculate the max, min, mean and std of every row
    raw_max, raw_min, raw_mean, raw_std = calc_array(image)
    print("row max(s): ", raw_max)
    print("row min(s): ", raw_min)
    print("row mean(s): ", raw_mean)
    print("row std(s): ", raw_std)

    # plot the results
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(raw_max, label='max', color='red')
    ax.plot(raw_min, label='min', color='blue')
    ax.plot(raw_mean, label='mean', color='green')
    ax.plot(raw_std, label='std', color='orange')
    ax.legend()
    # plt.savefig('output3.png', dpi=100)
    plt.show()

if __name__ == "__main__":
    main()