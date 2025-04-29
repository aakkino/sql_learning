# 安装所需依赖（如果尚未安装）:
# pip install kagglehub[pandas-datasets]
import os
import kagglehub
from kagglehub import KaggleDatasetAdapter

# 设置要加载的文件路径
# 注意：如果要加载整个数据集，可以将此设置为空字符串
# 如果要加载特定文件，请指定相对路径，例如："data.csv"
# 必须指定文件扩展名，否则会导致ValueError
file_path = "unique_dates_csv.csv"  # 修正文件名，添加.csv扩展名

# 加载数据集的最新版本
# 参数说明：
# - KaggleDatasetAdapter.PANDAS：指定使用Pandas适配器加载数据
# - "shivamsoni017/load-curve-graphs"：数据集的引用路径（所有者/数据集名称）
# - file_path：要加载的特定文件路径
# 注意：load_dataset 函数已被弃用 (DeprecationWarning)，建议查阅 kagglehub 文档以了解最新的推荐加载方法。
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "shivamsoni017/load-curve-graphs",
  file_path,
  pandas_kwargs={'encoding': 'latin1'} # 指定编码
  # 可以提供其他参数，如sql_query或pandas_kwargs
  # 更多信息请参考官方文档：
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

# 打印前5条记录，用于预览数据集内容
print("First 5 records:", df.head())

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 设置保存文件的路径（与当前脚本在同一目录下）
output_file_path = os.path.join(current_dir, "unique_dates_output.csv")

# 保存数据集到CSV文件
df.to_csv(output_file_path, index=False, encoding='utf-8')

print(f"数据集已保存到: {output_file_path}")
# kaggle datasets download shivamsoni017/load-curve-graphs --unzip
# kaggle datasets download thedevastator/240000-household-electricity-consumption-records --unzip 


