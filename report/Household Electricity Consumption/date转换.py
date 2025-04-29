import pandas as pd
import numpy as np # numpy 通常随 pandas 一起安装，NaT/NaN 处理可能用到

# 1. 导入 pandas (已完成)
# 2. 定义文件路径
file_path = ''
# 3. 定义日期列名
date_column_name = 'Date'

print(f"开始处理文件: {file_path}")
print(f"目标列: {date_column_name}")
try:
    # 4. 读取 CSV 文件
    #    注意：根据实际文件分隔符调整 sep 参数 (',' 或 ';')
    #    low_memory=False 建议用于可能包含混合类型的大文件
    df = pd.read_csv(file_path, sep=',', low_memory=False)
    print(f"文件读取成功，共 {len(df)} 行。")

    if date_column_name not in df.columns:
        print(f"错误: 列 '{date_column_name}' 不在文件中。可用列: {df.columns.tolist()}")
    else:
        # 5. 备份原始日期数据
        original_dates = df[date_column_name].copy()
        print(f"原始 '{date_column_name}' 列的前5行:\n{original_dates.head()}")

        # 6. 尝试按 'dd/mm/yyyy' 格式转换，无效值转为 NaT
        converted_dates = pd.to_datetime(df[date_column_name], format='%d/%m/%Y', errors='coerce')

        # 7. 将成功转换的日期格式化为 'dd/mm/yy'，NaT 会变成 NaN
        formatted_dates = converted_dates.dt.strftime('%d/%m/%y')

        # 8. 将格式化后的日期（包含 NaN）与原始日期合并，用原始值填充 NaN
        #    这样，只有成功按 'dd/mm/yyyy' 格式转换的日期才会被更新为 'dd/mm/yy'
        df[date_column_name] = formatted_dates.fillna(original_dates)

        # 9. 打印转换后列的前5行
        print(f"\n转换后 '{date_column_name}' 列的前5行:\n{df[date_column_name].head()}")

        # 10. 检查转换后是否还存在 NaN 值 (理论上不应存在，除非原始数据就有 NaN)
        final_nan_count = df[date_column_name].isnull().sum()
        print(f"\n转换操作完成。")
        print(f"最终 '{date_column_name}' 列中的 NaN 值数量: {final_nan_count}")

        # (可选) 如果需要保存修改后的文件:
        output_file_path = file_path.replace('.csv', '_processed.csv')
        df.to_csv(output_file_path, index=False)
        print(f"已将修改后的数据保存到: {output_file_path}")

except FileNotFoundError:
    print(f"错误: 文件未找到于路径 {file_path}")
except Exception as e:
    print(f"处理过程中发生错误: {e}")


# 11. 去除含有空数据的行
print("\n开始清理含有空数据的行...")
original_row_count = len(df)
print(f"清理前数据行数: {original_row_count}")

# 检查每列的空值数量
null_counts = df.isnull().sum()
print("\n各列空值数量:")
for column, count in null_counts.items():
    print(f"- {column}: {count}")

# 删除包含任何空值的行
df_cleaned = df.dropna()
cleaned_row_count = len(df_cleaned)
removed_rows = original_row_count - cleaned_row_count
print(f"\n已删除 {removed_rows} 行含有空值的数据 ({removed_rows/original_row_count:.2%})")
print(f"清理后数据行数: {cleaned_row_count}")

# 保存清理后的数据
cleaned_output_path = file_path.replace('.csv', '_cleaned.csv')
df_cleaned.to_csv(cleaned_output_path, index=False)
print(f"已将清理后的数据保存到: {cleaned_output_path}")
