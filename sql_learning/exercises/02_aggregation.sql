-- 聚合函数与分组练习
-- 文件: scripts/02_aggregation.sql

-- 练习 1: 计算 orders 表中的总订单数
-- 预期输出: 一个数字，表示订单总行数



-- 练习 2: 计算 orders 表中的总销售额 (所有订单金额 amount 的总和)
-- 预期输出: 一个数字，表示所有 amount 的和



-- 练习 3: 计算 orders 表中平均订单金额
-- 预期输出: 一个数字，表示 amount 的平均值



-- 练习 4: 查询每个客户 (customer_id) 的订单数量
-- 提示: 使用 GROUP BY customer_id 和 COUNT(*)
-- 预期输出: 两列 (customer_id, 订单数量)，每个客户一行



-- 练习 5: 查询每个客户 (customer_id) 的总订单金额
-- 提示: 使用 GROUP BY customer_id 和 SUM(amount)
-- 预期输出: 两列 (customer_id, 总金额)，每个客户一行



-- 练习 6: 查询哪个城市 (city) 的客户数量最多
-- 提示: 先按 city 分组计算客户数，再排序取第一个
-- 预期输出: 一个城市名称



-- 练习 7: 查询总订单金额大于 200 的客户ID (customer_id)
-- 提示: 使用 GROUP BY 和 HAVING
-- 预期输出: customer_id 列，只包含总金额 > 200 的客户



-- 练习 8: 查询每个订单日期 (order_date) 的订单数量和总金额
-- 提示: 使用 GROUP BY order_date
-- 预期输出: 三列 (order_date, 订单数量, 总金额)，每个日期一行 