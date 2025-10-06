import re
import csv
from datetime import datetime

def parse_log_file(log_file_path, output_csv_path):
    """
    解析日志文件，提取时间戳、US Raw、Time of Flight、Temp、Hum、Pres数据
    并保存为CSV文件
    """
    # 存储提取的数据
    extracted_data = []

    # 从文件名提取日期信息（假设格式为 device-monitor-YYMMDD-HHMMSS.log）
    filename_date = log_file_path.split('-')[-2]  # 提取251006
    filename_time = log_file_path.split('-')[-1].split('.')[0]  # 提取154357

    # 解析文件名中的日期和时间
    file_date = datetime.strptime(filename_date, "%y%m%d").date()  # YYMMDD格式

    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # 检查是否是分隔线行
            if '-----------------------------------------------------------' in line:
                # 这是分隔线，跳过创建新记录
                continue

            if 'Alt' in line or 'Xg' in line or 'Yg' in line or 'Zg' in line or 'Mic' in line:
                continue

            if 'EMF' in line or 'Light' in line or 'AIN' in line:
                continue

            # 匹配时间戳行 (格式: HH:MM:SS.sss)
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) >', line)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)

                # 将时间戳转换为完整的datetime对象
                time_obj = datetime.strptime(timestamp_str, "%H:%M:%S.%f").time()
                full_datetime = datetime.combine(file_date, time_obj)

                # 初始化当前时间戳的数据字典
                current_data = {
                    'datetime': full_datetime,
                    'us_raw': None,
                    'time_of_flight': None,
                    'temp': None,
                    'hum': None,
                    'pres': None
                }
                extracted_data.append(current_data)

            # 如果当前有活跃的时间戳，尝试匹配数据
                if full_datetime and extracted_data:
                    current_record = extracted_data[-1]

                # 匹配US Raw数据 - 更精确的匹配
                    us_raw_match = re.search(r'US Raw:\s+([\d.]+)\s+mm', line)
                    if us_raw_match:
                        current_record['us_raw'] = float(us_raw_match.group(1))

                # 匹配Time of Flight数据
                    tof_match = re.search(r'Time of Flight:\s+([\d.]+)\s+ns', line)
                    if tof_match:
                        current_record['time_of_flight'] = float(tof_match.group(1))

                # 匹配温度数据
                    temp_match = re.search(r'Temp:\s+([\d.]+)\s+°C', line)
                    if temp_match:
                        current_record['temp'] = float(temp_match.group(1))

                # 匹配湿度数据
                    hum_match = re.search(r'Hum:\s+([\d.]+)\s+%', line)
                    if hum_match:
                        current_record['hum'] = float(hum_match.group(1))

                # 匹配压力数据
                    pres_match = re.search(r'Pres:\s+([\d.]+)\s+kPa', line)
                    if pres_match:
                        current_record['pres'] = float(pres_match.group(1))

    # 写入CSV文件
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['datetime', 'us_raw', 'time_of_flight', 'temp', 'hum', 'pres']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in extracted_data:
            writer.writerow(data)

    print(f"成功提取 {len(extracted_data)} 条数据到 {output_csv_path}")

# 使用示例
if __name__ == "__main__":
    log_file_path = "../logs/device-monitor-251006-154357.log"  # 输入日志文件路径
    output_csv_path = "../logs/extracted_data.csv"  # 输出CSV文件路径

    parse_log_file(log_file_path, output_csv_path)