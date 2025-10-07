import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# device_monitor_file_path = 'device-monitor-modified.xlsx'
device_monitor_file_path = 'device-monitor-library.xlsx'

def calculate_regression_coefficients():
    """
    根据excel数据计算声速关于温度、湿度和压力的线性回归系数
    模型: c = c0 + a_t * delta_t + a_rh * delta_rh + a_p * delta_p
    其中: c0 = 343.5
          delta_t = actual_t - 20
          delta_rh = actual_rh - 0  
          delta_p = actual_p - 100
    """

    # 读取Excel文件
    df = pd.read_excel(device_monitor_file_path, sheet_name='Sheet1')

    # 提取需要的列数据
    # 注意：real_speed_of_sound列需要计算，因为Excel中显示的是公式
    # 我们将从原始数据重新计算real_speed_of_sound
    real_distance = df['real_distance(mm)'].values
    time_of_flight = df['time_of_flight(ns)'].values

    # 计算实际声速 (mm/s)，然后转换为m/s
    # real_speed_of_sound_mm_per_s = (real_distance / time_of_flight) * 1e9 * 2
    real_speed_of_sound_m_per_s = (real_distance / time_of_flight) * 1e9 * 2 / 1000  # 转换为m/s

    # 提取环境参数
    temperature = df['temperature(C)'].values
    humidity = df['humidity(%)'].values / 100  # 转换为小数形式
    pressure = df['pressure(kPa)'].values

    # 计算delta值
    delta_t = temperature - 20  # delta_t = actual_t - 20
    delta_rh = humidity - 0     # delta_rh = actual_rh - 0
    delta_p = pressure - 100    # delta_p = actual_p - 100

    # 准备自变量 (delta_t, delta_rh, delta_p)
    X = np.column_stack([delta_t, delta_rh, delta_p])

    # 准备因变量 (c - c0)
    c0 = 343.5  # m/s
    y = real_speed_of_sound_m_per_s - c0

    # 进行线性回归（无截距，因为模型已经包含c0）
    model = LinearRegression(fit_intercept=False)
    model.fit(X, y)

    # 获取系数
    a_t, a_rh, a_p = model.coef_

    return a_t, a_rh, a_p, model

def main():
    try:
        a_t, a_rh, a_p, model = calculate_regression_coefficients()

        print("线性回归结果:")
        print(f"a_t (温度系数): {a_t:.6f} m/s/°C")
        print(f"a_rh (湿度系数): {a_rh:.6f} m/s")
        print(f"a_p (压力系数): {a_p:.6f} m/s/kPa")
        print(f"\n回归模型: c = 343.5 + ({a_t:.6f}) * delta_t + ({a_rh:.6f}) * delta_rh + ({a_p:.6f}) * delta_p")
        print(f"其中: delta_t = t - 20, delta_rh = rh - 0, delta_p = p - 100")

        # 计算R²分数
        real_distance = pd.read_excel(device_monitor_file_path, sheet_name='Sheet1')['real_distance(mm)'].values
        time_of_flight = pd.read_excel(device_monitor_file_path, sheet_name='Sheet1')['time_of_flight(ns)'].values
        real_speed_of_sound_m_per_s = (real_distance / time_of_flight) * 1e9 * 2 / 1000

        temperature = pd.read_excel(device_monitor_file_path, sheet_name='Sheet1')['temperature(C)'].values
        humidity = pd.read_excel(device_monitor_file_path, sheet_name='Sheet1')['humidity(%)'].values / 100
        pressure = pd.read_excel(device_monitor_file_path, sheet_name='Sheet1')['pressure(kPa)'].values

        delta_t = temperature - 20
        delta_rh = humidity - 0
        delta_p = pressure - 100
        X = np.column_stack([delta_t, delta_rh, delta_p])

        c0 = 343.5
        y_pred = c0 + model.predict(X)

        r_squared = model.score(X, real_speed_of_sound_m_per_s - c0)
        print(f"\n模型R²分数: {r_squared:.6f}")

    except Exception as e:
        print(f"处理数据时出错: {e}")
        print("请确保device_monitor_file_path文件存在且格式正确")

if __name__ == "__main__":
    main()