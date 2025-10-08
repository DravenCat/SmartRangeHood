import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

file_path = 'device-monitor-modified.xlsx'
# file_path = 'device-monitor-library.xlsx'

def calculate_extended_regression():
    """
    计算扩展的线性回归模型:
    d = a0 + a1 * (Time of Flight) + b0 * delta_t + b1 * delta_rh + b2 * delta_p
    其中: delta_t = actual_t - 20
          delta_rh = actual_rh - 0
          delta_p = actual_p - 100
    """

    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name='Sheet1')

    # 提取数据
    real_distance = df['real_distance(mm)'].values  # 因变量 d
    time_of_flight = df['time_of_flight(ns)'].values  # 自变量1
    temperature = df['temperature(C)'].values  # 自变量2
    humidity = df['humidity(%)'].values / 100  # 转换为小数形式，自变量3
    pressure = df['pressure(kPa)'].values  # 自变量4

    # 计算delta值
    delta_t = temperature - 20  # delta_t = actual_t - 20
    delta_rh = humidity - 0     # delta_rh = actual_rh - 0
    delta_p = pressure - 100    # delta_p = actual_p - 100

    # 准备自变量矩阵 X
    # 包括: 常数项(用于a0), Time of Flight,
    # delta_t * Time of Flight, delta_rh * Time of Flight, delta_p * Time of Flight, delta_t
    X = np.column_stack([
        np.ones(len(time_of_flight)),  # 常数项，用于a0
        time_of_flight,                # 用于a1
        delta_t * time_of_flight,      # 用于b0
        delta_rh * time_of_flight,     # 用于b1
        delta_p * time_of_flight,      # 用于b2
    ])

    # 准备因变量 y (真实距离)
    y = real_distance

    # 进行线性回归（包含截距，但我们已经手动添加了常数项）
    model = LinearRegression(fit_intercept=False)  # 不使用内置截距，因为我们已添加常数项
    model.fit(X, y)

    # 获取系数
    a0, a1, b0, b1, b2 = model.coef_

    return a0, a1, b0, b1, b2, model, X, y


def main():
    try:
        a0, a1, b0, b1, b2, model, X, y = calculate_extended_regression()

        print("扩展线性回归结果:")
        print(f"a0 (常数项): {a0:.6f} mm")
        print(f"a1 (飞行时间系数): {a1:.6f} mm/ns")
        print(f"b0 (温度-飞行时间交互系数): {b0:.6f} mm/(ns·°C)")
        print(f"b1 (湿度-飞行时间交互系数): {b1:.6f} mm/ns")
        print(f"b2 (压力-飞行时间交互系数): {b2:.6f} mm/(ns·kPa)")

        print(f"\n回归模型:")
        print(f"d = {a0:.6f} + ({a1:.6f}) * (Time of Flight) + ")
        print(f"     ({b0:.6f}) * delta_t * (Time of Flight) + ")
        print(f"     ({b1:.6f}) * delta_rh * (Time of Flight) + ")
        print(f"     ({b2:.6f}) * delta_p * (Time of Flight) + ")
        print(f"其中: delta_t = t - 20, delta_rh = rh - 0, delta_p = p - 100")

        # 计算预测值和残差
        y_pred = model.predict(X)
        residuals = y - y_pred

        # 计算统计指标
        r_squared = model.score(X, y)
        mse = np.mean(residuals**2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(residuals))

        # 计算相对误差
        relative_errors = np.abs(residuals / y) * 100
        max_relative_error = np.max(relative_errors)
        mean_relative_error = np.mean(relative_errors)

        print(f"\n模型统计指标:")
        print(f"R²分数: {r_squared:.6f}")
        print(f"均方误差 (MSE): {mse:.6f} mm²")
        print(f"均方根误差 (RMSE): {rmse:.6f} mm")
        print(f"平均绝对误差 (MAE): {mae:.6f} mm")
        print(f"平均相对误差: {mean_relative_error:.2f}%")
        print(f"最大相对误差: {max_relative_error:.2f}%")

        # 输出每个数据点的预测和残差
        print(f"\n详细结果:")
        print("真实距离(mm) | 预测距离(mm) | 残差(mm) | 相对误差(%)")
        print("-" * 60)
        for i in range(len(y)):
            print(f"{y[i]:.1f}        | {y_pred[i]:.1f}        | {residuals[i]:.2f}    | {relative_errors[i]:.2f}%")


    except Exception as e:
        print(f"处理数据时出错: {e}")
        print("请确保file_path文件存在且格式正确")

if __name__ == "__main__":
    main()