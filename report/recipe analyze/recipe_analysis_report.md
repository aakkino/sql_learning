# 食谱数据分析报告

## 引言
本报告基于 `recipes_data.csv` 数据集，旨在探索食谱的各项特征，包括菜系分布、烹饪时间、卡路里含量、常用食材以及饮食限制等。

## 数据概览
*   数据集维度: 161 行, 11 列 (包含中间处理列)
*   原始列名: ['recipe_name', 'cuisine', 'ingredients', 'cooking_time_minutes', 'prep_time_minutes', 'servings', 'calories_per_serving', 'dietary_restrictions', 'ingredients_list', 'dietary_restrictions_list', 'total_time_minutes']

### 缺失值统计 (清理后)
```
cooking_time_minutes    0
prep_time_minutes       0
servings                4
calories_per_serving    5
```

## 描述性统计
以下是主要数值特征的描述性统计信息：
```
       cooking_time_minutes  prep_time_minutes    servings  calories_per_serving  total_time_minutes
count            161.000000         161.000000  157.000000            156.000000          161.000000
mean              62.614907          22.608696    5.312102            390.076923           85.223602
std               76.166517          10.957973    3.275499            153.747700           79.979449
min                5.000000           2.000000    1.000000             40.000000            7.000000
25%               30.000000          15.000000    4.000000            299.750000           45.000000
50%               45.000000          20.000000    4.000000            381.500000           65.000000
75%               68.000000          30.000000    6.000000            500.000000           95.000000
max              720.000000          60.000000   24.000000            784.000000          750.000000
```

## 菜系分析
分析了不同菜系的食谱数量、平均总耗时和平均卡路里。

![Top 15 菜系食谱数量](report_images\cuisine_counts.png)
*图 1: 食谱数量最多的前 15 个菜系。*

![Top 15 菜系平均总耗时](report_images\cuisine_avg_time.png)
*图 2: 平均总耗时最长的前 15 个菜系。*

![Top 15 菜系平均每份卡路里](report_images\cuisine_avg_calories.png)
*图 3: 平均每份卡路里最高的前 15 个菜系。*

## 时间与卡路里分析
分析了食谱的总耗时和卡路里分布，以及两者之间的关系。

![食谱总耗时分布](report_images\total_time_distribution.png)
*图 4: 食谱总耗时（准备时间 + 烹饪时间）的分布情况。*

![每份卡路里分布](report_images\calories_distribution.png)
*图 5: 每份食谱卡路里的分布情况。*

![总耗时 vs 每份卡路里](report_images\time_vs_calories_scatter.png)
*图 6: 食谱总耗时与每份卡路里之间的关系散点图。*

## 食材分析
统计了数据集中最常出现的食材。

![Top 20 最常见食材](report_images\top_ingredients.png)
*图 7: 数据集中出现频率最高的前 20 种食材。*

## 饮食限制分析
统计了符合各种饮食限制的食谱数量。

![食谱饮食限制统计](report_images\dietary_restrictions_counts.png)
*图 8: 数据集中各种饮食限制的食谱数量统计。*

## 结论
本报告对食谱数据进行了多方面的分析和可视化。主要发现包括 [此处可根据图表结果添加简要总结，例如：意大利、墨西哥菜系数量较多；某些菜系平均耗时或卡路里显著偏高；洋葱、大蒜是最常用食材；素食食谱占有一定比例等]。这些分析有助于理解该数据集中的食谱特征。
