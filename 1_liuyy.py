import matplotlib.pyplot as plt
from astropy.io import fits

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
    return row_max, row_min, row_mean, row_std

def main():
    raw_max, raw_min, raw_mean, raw_std = calc_array(image)
    print("max of every row: ", raw_max)
    print("min of every row: ", raw_min)
    print("mean of every row: ", raw_mean)
    print("std of every row: ", raw_std)

if __name__ == "__main__":
    main()