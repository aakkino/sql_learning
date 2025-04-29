import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os
from collections import Counter
import numpy as np

# --- Configuration ---
DATA_FILE = 'scripts/recipes_data.csv'
REPORT_FILE = 'scripts/recipe_analysis_report.md'
IMAGE_DIR = 'scripts/report_images'
TOP_N_CUISINE = 15
TOP_N_INGREDIENTS = 20

# --- Helper Functions ---
def safe_literal_eval(s):
    """Safely evaluate a string containing a Python literal (list)."""
    try:
        # Handle potential numpy nan strings within the list string representation
        s = s.replace("nan", "None")
        evaluated = ast.literal_eval(s)
        if isinstance(evaluated, list):
            # Replace None back to np.nan if needed, or handle specific strings like 'nan'
            # For dietary_restrictions, specifically handle the ['nan'] case later
            return evaluated
        else:
            return [] # Return empty list if not a list
    except (ValueError, SyntaxError, TypeError):
        return [] # Return empty list on error

def ensure_dir(directory):
    """Ensure the directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# --- Main Analysis Logic ---
def analyze_recipes():
    """Loads data, performs analysis, generates plots, and creates a report."""
    print(f"开始分析 {DATA_FILE}...")

    # 1. Load Data
    try:
        df = pd.read_csv(DATA_FILE)
        print(f"成功加载数据，维度: {df.shape}")
    except FileNotFoundError:
        print(f"错误: 数据文件 {DATA_FILE} 未找到。")
        return
    except Exception as e:
        print(f"加载数据时出错: {e}")
        return

    # 2. Clean Data
    print("开始数据清理...")
    numeric_cols = ['cooking_time_minutes', 'prep_time_minutes', 'servings', 'calories_per_serving']
    initial_nan_counts = df[numeric_cols].isna().sum()
    print("数值列初始 NaN 统计:")
    print(initial_nan_counts)

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    cleaned_nan_counts = df[numeric_cols].isna().sum()
    print("数值列转换后 NaN 统计:")
    print(cleaned_nan_counts)

    # Parse list-like strings
    df['ingredients_list'] = df['ingredients'].apply(safe_literal_eval)
    df['dietary_restrictions_list'] = df['dietary_restrictions'].apply(safe_literal_eval)

    # Specific handling for ['nan'] in dietary_restrictions
    df['dietary_restrictions_list'] = df['dietary_restrictions_list'].apply(lambda x: [] if x == ['nan'] or x == [None] else x)

    # Clean cuisine names
    df['cuisine'] = df['cuisine'].str.lower().str.strip()
    print("数据清理完成。")

    # 3. Feature Engineering
    print("计算派生列...")
    df['total_time_minutes'] = df['cooking_time_minutes'] + df['prep_time_minutes']
    print("派生列计算完成。")


    # 4. Analysis and Visualization
    print("开始数据分析与可视化...")
    ensure_dir(IMAGE_DIR) # Create image directory if it doesn't exist

    # --- Descriptive Statistics ---
    print("计算描述性统计...")
    desc_stats = df[numeric_cols + ['total_time_minutes']].describe()
    print(desc_stats)

    # --- Cuisine Analysis ---
    print("菜系分析...")
    cuisine_counts = df['cuisine'].value_counts()
    top_cuisines = cuisine_counts.nlargest(TOP_N_CUISINE)

    plt.figure(figsize=(12, 7))
    sns.barplot(x=top_cuisines.values, y=top_cuisines.index, palette="viridis")
    plt.title(f'Top {TOP_N_CUISINE} 菜系食谱数量')
    plt.xlabel('食谱数量')
    plt.ylabel('菜系')
    plt.tight_layout()
    cuisine_counts_path = os.path.join(IMAGE_DIR, 'cuisine_counts.png')
    plt.savefig(cuisine_counts_path)
    plt.close()
    print(f"菜系数量图已保存至: {cuisine_counts_path}")

    cuisine_avg_time = df.groupby('cuisine')['total_time_minutes'].mean().nlargest(TOP_N_CUISINE)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=cuisine_avg_time.values, y=cuisine_avg_time.index, palette="viridis")
    plt.title(f'Top {TOP_N_CUISINE} 菜系平均总耗时 (分钟)')
    plt.xlabel('平均总耗时 (分钟)')
    plt.ylabel('菜系')
    plt.tight_layout()
    cuisine_avg_time_path = os.path.join(IMAGE_DIR, 'cuisine_avg_time.png')
    plt.savefig(cuisine_avg_time_path)
    plt.close()
    print(f"菜系平均时间图已保存至: {cuisine_avg_time_path}")

    cuisine_avg_calories = df.groupby('cuisine')['calories_per_serving'].mean().nlargest(TOP_N_CUISINE)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=cuisine_avg_calories.values, y=cuisine_avg_calories.index, palette="viridis")
    plt.title(f'Top {TOP_N_CUISINE} 菜系平均每份卡路里')
    plt.xlabel('平均每份卡路里')
    plt.ylabel('菜系')
    plt.tight_layout()
    cuisine_avg_calories_path = os.path.join(IMAGE_DIR, 'cuisine_avg_calories.png')
    plt.savefig(cuisine_avg_calories_path)
    plt.close()
    print(f"菜系平均卡路里图已保存至: {cuisine_avg_calories_path}")


    # --- Time/Calorie Analysis ---
    print("时间与卡路里分析...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_time_minutes'].dropna(), kde=True, bins=30)
    plt.title('食谱总耗时分布')
    plt.xlabel('总耗时 (分钟)')
    plt.ylabel('频数')
    plt.tight_layout()
    total_time_dist_path = os.path.join(IMAGE_DIR, 'total_time_distribution.png')
    plt.savefig(total_time_dist_path)
    plt.close()
    print(f"总耗时分布图已保存至: {total_time_dist_path}")

    plt.figure(figsize=(10, 6))
    sns.histplot(df['calories_per_serving'].dropna(), kde=True, bins=30)
    plt.title('每份卡路里分布')
    plt.xlabel('每份卡路里')
    plt.ylabel('频数')
    plt.tight_layout()
    calories_dist_path = os.path.join(IMAGE_DIR, 'calories_distribution.png')
    plt.savefig(calories_dist_path)
    plt.close()
    print(f"卡路里分布图已保存至: {calories_dist_path}")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df.dropna(subset=['total_time_minutes', 'calories_per_serving']),
                    x='total_time_minutes', y='calories_per_serving', alpha=0.6)
    plt.title('总耗时 vs 每份卡路里')
    plt.xlabel('总耗时 (分钟)')
    plt.ylabel('每份卡路里')
    plt.tight_layout()
    time_vs_calories_path = os.path.join(IMAGE_DIR, 'time_vs_calories_scatter.png')
    plt.savefig(time_vs_calories_path)
    plt.close()
    print(f"时间vs卡路里散点图已保存至: {time_vs_calories_path}")

    # --- Ingredient Analysis ---
    print("食材分析...")
    all_ingredients = [ingredient.lower().strip() for sublist in df['ingredients_list'] for ingredient in sublist if isinstance(ingredient, str)]
    ingredient_counts = Counter(all_ingredients)
    top_ingredients = ingredient_counts.most_common(TOP_N_INGREDIENTS)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=[count for _, count in top_ingredients], y=[ing for ing, _ in top_ingredients], palette="mako")
    plt.title(f'Top {TOP_N_INGREDIENTS} 最常见食材')
    plt.xlabel('出现次数')
    plt.ylabel('食材')
    plt.tight_layout()
    top_ingredients_path = os.path.join(IMAGE_DIR, 'top_ingredients.png')
    plt.savefig(top_ingredients_path)
    plt.close()
    print(f"Top食材图已保存至: {top_ingredients_path}")

    # --- Dietary Restriction Analysis ---
    print("饮食限制分析...")
    all_restrictions = [restriction.lower().strip() for sublist in df['dietary_restrictions_list'] for restriction in sublist if isinstance(restriction, str)]
    restriction_counts = Counter(all_restrictions)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(restriction_counts.values()), y=list(restriction_counts.keys()), palette="rocket")
    plt.title('食谱饮食限制统计')
    plt.xlabel('食谱数量')
    plt.ylabel('饮食限制')
    plt.tight_layout()
    dietary_restrictions_path = os.path.join(IMAGE_DIR, 'dietary_restrictions_counts.png')
    plt.savefig(dietary_restrictions_path)
    plt.close()
    print(f"饮食限制图已保存至: {dietary_restrictions_path}")

    print("分析与可视化完成。")

    # 5. Generate Report
    print(f"生成报告文件: {REPORT_FILE}...")
    report_content = f"""# 食谱数据分析报告

## 引言
本报告基于 `recipes_data.csv` 数据集，旨在探索食谱的各项特征，包括菜系分布、烹饪时间、卡路里含量、常用食材以及饮食限制等。

## 数据概览
*   数据集维度: {df.shape[0]} 行, {df.shape[1]} 列 (包含中间处理列)
*   原始列名: {list(df.columns)}

### 缺失值统计 (清理后)
```
{cleaned_nan_counts.to_string()}
```

## 描述性统计
以下是主要数值特征的描述性统计信息：
```
{desc_stats.to_string()}
```

## 菜系分析
分析了不同菜系的食谱数量、平均总耗时和平均卡路里。

![Top {TOP_N_CUISINE} 菜系食谱数量]({os.path.relpath(cuisine_counts_path, os.path.dirname(REPORT_FILE))})
*图 1: 食谱数量最多的前 {TOP_N_CUISINE} 个菜系。*

![Top {TOP_N_CUISINE} 菜系平均总耗时]({os.path.relpath(cuisine_avg_time_path, os.path.dirname(REPORT_FILE))})
*图 2: 平均总耗时最长的前 {TOP_N_CUISINE} 个菜系。*

![Top {TOP_N_CUISINE} 菜系平均每份卡路里]({os.path.relpath(cuisine_avg_calories_path, os.path.dirname(REPORT_FILE))})
*图 3: 平均每份卡路里最高的前 {TOP_N_CUISINE} 个菜系。*

## 时间与卡路里分析
分析了食谱的总耗时和卡路里分布，以及两者之间的关系。

![食谱总耗时分布]({os.path.relpath(total_time_dist_path, os.path.dirname(REPORT_FILE))})
*图 4: 食谱总耗时（准备时间 + 烹饪时间）的分布情况。*

![每份卡路里分布]({os.path.relpath(calories_dist_path, os.path.dirname(REPORT_FILE))})
*图 5: 每份食谱卡路里的分布情况。*

![总耗时 vs 每份卡路里]({os.path.relpath(time_vs_calories_path, os.path.dirname(REPORT_FILE))})
*图 6: 食谱总耗时与每份卡路里之间的关系散点图。*

## 食材分析
统计了数据集中最常出现的食材。

![Top {TOP_N_INGREDIENTS} 最常见食材]({os.path.relpath(top_ingredients_path, os.path.dirname(REPORT_FILE))})
*图 7: 数据集中出现频率最高的前 {TOP_N_INGREDIENTS} 种食材。*

## 饮食限制分析
统计了符合各种饮食限制的食谱数量。

![食谱饮食限制统计]({os.path.relpath(dietary_restrictions_path, os.path.dirname(REPORT_FILE))})
*图 8: 数据集中各种饮食限制的食谱数量统计。*

## 结论
本报告对食谱数据进行了多方面的分析和可视化。主要发现包括 [此处可根据图表结果添加简要总结，例如：意大利、墨西哥菜系数量较多；某些菜系平均耗时或卡路里显著偏高；洋葱、大蒜是最常用食材；素食食谱占有一定比例等]。这些分析有助于理解该数据集中的食谱特征。
"""

    try:
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"报告已成功生成: {REPORT_FILE}")
    except Exception as e:
        print(f"写入报告文件时出错: {e}")

# --- Script Execution ---
if __name__ == "__main__":
    # 设置 Matplotlib 使用支持中文的字体
    # 这里假设系统安装了 SimHei 字体，如果未安装或不同系统，需要替换为可用字体
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
    except Exception as e:
        print(f"设置中文字体失败，可能缺少 SimHei 字体或环境不支持: {e}")
        print("图表中的中文可能无法正常显示。")

    analyze_recipes() 