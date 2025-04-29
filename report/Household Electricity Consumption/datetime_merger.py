import pandas as pd

def merge_datetime_columns(file_path: str, date_col: str = 'Date', time_col: str = 'Time', new_col_name: str = 'DateTime', date_format: str = '%d/%m/%y', time_format: str = '%H:%M:%S', separator: str = ',', na_values: list = ['?'], drop_original: bool = True) -> pd.DataFrame:
    """
    读取CSV文件，合并指定的日期和时间列，并返回包含新DateTime列的DataFrame。

    参数:
        file_path (str): CSV文件的路径。
        date_col (str): 包含日期的列名。默认为 'Date'。
        time_col (str): 包含时间的列名。默认为 'Time'。
        new_col_name (str): 合并后新列的名称。默认为 'DateTime'。
        date_format (str): 日期列的格式字符串。默认为 '%d/%m/%y'。
        time_format (str): 时间列的格式字符串。默认为 '%H:%M:%S'。
        separator (str): CSV文件的分隔符。默认为 ','。
        na_values (list): 需要识别为缺失值的值列表。默认为 ['?']。
        drop_original (bool): 是否删除原始的日期和时间列。默认为 True。

    返回:
        pd.DataFrame: 包含合并后的DateTime列的Pandas DataFrame。
                     如果读取或解析过程中发生错误，将引发相应的异常。
                     无法解析的日期时间组合将被转换为 NaT (Not a Time)。
    """
    try:
        # Checklist item 3: Read CSV with specific dtype for date/time columns
        df = pd.read_csv(
            file_path,
            sep=separator,
            na_values=na_values,
            dtype={date_col: str, time_col: str} # 确保作为字符串读取
        )

        # Checklist item 4: Concatenate date and time strings
        # 使用 .loc 避免 SettingWithCopyWarning，并确保在原始 DataFrame 上操作
        temp_datetime_str_col = '_temp_datetime_str_' # 临时列名，避免与现有列冲突
        df[temp_datetime_str_col] = df[date_col] + ' ' + df[time_col]

        # Checklist item 5: Convert concatenated string to datetime objects
        # 尝试多种日期格式以处理不同格式的日期
        df[new_col_name] = pd.to_datetime(df[temp_datetime_str_col], errors='coerce')
        
        # 检查是否有无法解析的日期时间
        mask_nat = df[new_col_name].isna()
        if mask_nat.any():
            # 尝试使用指定的格式解析那些未成功解析的日期时间
            full_format = f'{date_format} {time_format}'
            df.loc[mask_nat, new_col_name] = pd.to_datetime(
                df.loc[mask_nat, temp_datetime_str_col], 
                format=full_format, 
                errors='coerce'
            )
            
            # 尝试其他可能的日期格式
            alternative_formats = [
                '%d/%m/%Y %H:%M:%S',  # 带4位年份
                '%m/%d/%y %H:%M:%S',  # 美式日期格式
                '%m/%d/%Y %H:%M:%S',  # 美式日期格式带4位年份
                '%Y-%m-%d %H:%M:%S',  # ISO格式
                '%d-%m-%y %H:%M:%S',  # 破折号分隔
                '%d-%m-%Y %H:%M:%S'   # 破折号分隔带4位年份
            ]
            
            for fmt in alternative_formats:
                # 只对仍然是NaT的行尝试新格式
                mask_still_nat = df[new_col_name].isna()
                if not mask_still_nat.any():
                    break
                    
                df.loc[mask_still_nat, new_col_name] = pd.to_datetime(
                    df.loc[mask_still_nat, temp_datetime_str_col], 
                    format=fmt, 
                    errors='coerce'
                )

        # Checklist item 6: Drop the temporary concatenated string column
        df.drop(columns=[temp_datetime_str_col], inplace=True)
        
        # 删除原始的日期和时间列
        if drop_original:
            df.drop(columns=[date_col, time_col], inplace=True)

        # Checklist item 7: Return the processed DataFrame
        return df

    except FileNotFoundError:
        print(f"错误：文件未找到于路径 '{file_path}'")
        raise
    except KeyError as e:
        print(f"错误：列名 '{e}' 在文件中未找到。请检查 'date_col' 和 'time_col' 参数。")
        raise
    except Exception as e:
        print(f"处理文件时发生未知错误：{e}")
        raise

# 可以在这里添加一个简单的示例用法，方便测试
if __name__ == '__main__':
    # 假设 household_power_consumption.csv 在 'report/Household Electricity Consumption/' 目录下
    # 请根据您的实际文件路径修改下面的路径
    example_file_path = r'E:\desktop_directory\SQL学习\report\Household Electricity Consumption\household_power_consumption_cleaned.csv' # 使用原始字符串以避免转义问题

    try:
        print(f"正在处理文件: {example_file_path}")
        # 因为文件很大，只读取前几行进行演示和测试
        # 注意：实际使用时不应加 nrows，或者根据内存调整
        processed_df = merge_datetime_columns(example_file_path)

        print("\n处理完成。DataFrame 的前5行:")
        print(processed_df.head())

        print("\n新 DateTime 列的信息:")
        print(processed_df[processed_df.columns[-1]].info()) # 打印最后一列（即新列）的信息

        print("\n检查是否存在 NaT (无法解析的日期时间):")
        print(f"NaT 数量: {processed_df[processed_df.columns[-1]].isnull().sum()}")

    except FileNotFoundError:
        print(f"示例用法错误：请确保文件 '{example_file_path}' 存在于指定位置。")
    except Exception as e:
        print(f"示例用法执行时发生错误: {e}") 
    #保存处理后的数据
    processed_df.to_csv('processed_household_power_consumption_merged.csv', index=True)
