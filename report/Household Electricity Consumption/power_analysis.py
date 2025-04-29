import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def merge_datetime_columns(file_path: str, date_col: str = 'Date', time_col: str = 'Time', 
                         new_col_name: str = 'DateTime', date_format: str = '%d/%m/%y', 
                         time_format: str = '%H:%M:%S', separator: str = ';', 
                         na_values: list = ['?']) -> pd.DataFrame:
    """
    读取CSV文件，合并日期和时间列为单一的DateTime列。
    
    参数:
        file_path (str): CSV文件路径
        date_col (str): 日期列名，默认为'Date'
        time_col (str): 时间列名，默认为'Time'
        new_col_name (str): 合并后的新列名，默认为'DateTime'
        date_format (str): 日期格式字符串，默认为'%d/%m/%y'
        time_format (str): 时间格式字符串，默认为'%H:%M:%S'
        separator (str): CSV分隔符，默认为';'
        na_values (list): 需要识别为缺失值的值列表，默认为['?']
    
    返回:
        pd.DataFrame: 包含合并后DateTime列的数据框
    """
    try:
        # 读取CSV文件，确保日期和时间列作为字符串读入
        df = pd.read_csv(
            file_path,
            sep=separator,
            na_values=na_values,
            dtype={date_col: str, time_col: str}
        )
        
        # 创建临时列合并日期和时间字符串
        temp_datetime_str_col = '_temp_datetime_str_'
        df[temp_datetime_str_col] = df[date_col] + ' ' + df[time_col]
        
        # 尝试将合并的字符串转换为datetime对象
        df[new_col_name] = pd.to_datetime(df[temp_datetime_str_col], errors='coerce')
        
        # 处理无法解析的日期时间
        mask_nat = df[new_col_name].isna()
        if mask_nat.any():
            # 使用指定的格式尝试解析
            full_format = f'{date_format} {time_format}'
            df.loc[mask_nat, new_col_name] = pd.to_datetime(
                df.loc[mask_nat, temp_datetime_str_col], 
                format=full_format, 
                errors='coerce'
            )
            
            # 定义其他可能的日期时间格式
            alternative_formats = [
                '%d/%m/%Y %H:%M:%S',
                '%m/%d/%y %H:%M:%S',
                '%m/%d/%Y %H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%d-%m-%y %H:%M:%S',
                '%d-%m-%Y %H:%M:%S'
            ]
            
            # 尝试使用替代格式解析剩余的NaT值
            for fmt in alternative_formats:
                mask_still_nat = df[new_col_name].isna()
                if not mask_still_nat.any():
                    break
                df.loc[mask_still_nat, new_col_name] = pd.to_datetime(
                    df.loc[mask_still_nat, temp_datetime_str_col], 
                    format=fmt, 
                    errors='coerce'
                )

        # 删除临时列
        df.drop(columns=[temp_datetime_str_col], inplace=True)
        return df

    except Exception as e:
        print(f"处理文件时发生错误：{e}")
        raise

def load_power_data(file_path):
    """
    加载家庭用电数据并处理日期时间格式。
    
    参数:
        file_path (str): CSV文件路径
    
    返回:
        pandas.DataFrame: 处理后的数据框，使用datetime作为索引
    """
    try:
        # 使用merge_datetime_columns函数加载和处理数据
        df = merge_datetime_columns(
            file_path,
            date_col='Date',
            time_col='Time',
            new_col_name='Datetime',
            separator=',',
            na_values=['?']
        )
        print(f"数据初步加载自: {file_path}")
        
        # 将Datetime列设置为索引
        df.set_index('Datetime', inplace=True)
        
        # 删除原始的日期和时间列
        if 'Date' in df.columns and 'Time' in df.columns:
            df.drop(columns=['Date', 'Time'], inplace=True)
        
        print("Datetime 索引创建成功。")
        return df
        
    except FileNotFoundError:
        print(f"错误: 文件未找到 {file_path}")
        return None
    except Exception as e:
        print(f"加载或处理数据时发生错误: {e}")
        if 'df' in locals():
            print("发生错误时的数据列:", df.columns.tolist())
        return None


def preprocess_data(df):
    """
    对用电数据进行预处理，包括处理缺失值和数据类型转换。
    
    参数:
        df (pandas.DataFrame): 原始数据框
    
    返回:
        pandas.DataFrame: 预处理后的数据框
    """
    print("\n开始数据预处理...")
    
    # 检查初始缺失值
    print("初始缺失值数量:")
    print(df.isnull().sum())

    # 使用前向填充处理缺失值
    print("使用前向填充 (ffill) 处理缺失值...")
    df_filled = df.ffill()

    # 检查填充后的缺失值
    print("\n填充后缺失值数量:")
    print(df_filled.isnull().sum())

    # 确保所有列的数据类型正确
    for col in df_filled.columns:
        if df_filled[col].dtype == 'object':  # 对象类型列转换为数值
            try:
                df_filled[col] = pd.to_numeric(df_filled[col])
            except ValueError:
                print(f"警告: 列 '{col}' 无法转换为数值类型。")
        # 将数值列统一转换为float类型
        elif pd.api.types.is_numeric_dtype(df_filled[col]):
            df_filled[col] = df_filled[col].astype(float)

    print("\n数据类型:")
    print(df_filled.dtypes)
    print("数据预处理完成。")
    return df_filled

def explore_and_visualize(df, save_dir):
    """
    进行探索性数据分析并创建可视化图表。
    
    参数:
        df (pandas.DataFrame): 预处理后的数据框
        save_dir (str): 保存图表的目录
    """
    print("\n开始探索性分析与可视化...")

    # 1. 绘制每日总有功功率时序图
    print("绘制每日总有功功率...")
    plt.figure(figsize=(15, 6))
    df['Global_active_power'].resample('D').sum().plot(
        title='Daily Global Active Power (Resampled Daily Sum)'
    )
    plt.ylabel('Global Active Power (kilowatt)')
    plt.xlabel('Date')
    plt.grid(True)
    plt.tight_layout()
    save_path_1 = os.path.join(save_dir, 'daily_global_active_power.png')
    plt.savefig(save_path_1)
    print(f"图表已保存至: {save_path_1}")
    plt.show()

    # 2. 绘制分项用电量时序图
    print("绘制每日分项计量...")
    plt.figure(figsize=(15, 6))
    df['Sub_metering_1'].resample('D').sum().plot(label='Kitchen', alpha=0.8)
    df['Sub_metering_2'].resample('D').sum().plot(label='Laundry Room', alpha=0.8)
    df['Sub_metering_3'].resample('D').sum().plot(label='Water Heater & AC', alpha=0.8)
    plt.title('Daily Sub-metering (Resampled Daily Sum)')
    plt.ylabel('Energy (watt-hour)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    save_path_2 = os.path.join(save_dir, 'daily_sub_metering.png')
    plt.savefig(save_path_2)
    print(f"图表已保存至: {save_path_2}")
    plt.show()

    # 3. 绘制总有功功率分布直方图
    print("绘制Global Active Power Distribution...")
    plt.figure(figsize=(10, 6))
    df['Global_active_power'].hist(bins=100, alpha=0.7)
    plt.title('Global Active Power Distribution')
    plt.xlabel('Global Active Power (kilowatt)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    save_path_3 = os.path.join(save_dir, 'global_active_power_distribution.png')
    plt.savefig(save_path_3)
    print(f"图表已保存至: {save_path_3}")
    plt.show()

    # 4. 绘制每月平均总有功功率柱状图
    print("绘制Monthly Average Global Active Power...")
    plt.figure(figsize=(12, 6))
    df['Global_active_power'].resample('M').mean().plot(
        kind='bar',
        title='Monthly Average Global Active Power'
    )
    plt.ylabel('Average Global Active Power (kilowatt)')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    save_path_4 = os.path.join(save_dir, 'monthly_avg_global_active_power.png')
    plt.savefig(save_path_4)
    print(f"图表已保存至: {save_path_4}")
    plt.show()

    print("探索性分析与可视化完成。")


if __name__ == "__main__":
    # 设置文件路径
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'household_power_consumption.csv')
    
    try:
        # 加载数据
        power_df = load_power_data(file_path)

        if power_df is not None:
            # 预处理数据
            processed_df = preprocess_data(power_df)
            # 进行探索性分析和可视化
            explore_and_visualize(processed_df, script_dir)
        else:
            print("数据加载失败，无法继续分析。")
    except Exception as e:
        print(f"执行主程序时发生意外错误: {e}")
