-- 子查询 (Subquery) 和 公用表表达式 (CTE) 练习
-- 文件: scripts/04_subqueries_cte.sql

-- 练习 1: 查询订单金额大于平均订单金额的所有订单信息
-- 提示: 使用子查询计算平均订单金额
-- 预期输出: orders 表中 amount 大于平均值的行



-- 练习 2: 查询下过订单的客户的姓名和城市
-- 提示: 使用子查询 (SELECT DISTINCT customer_id FROM orders) 或 IN 操作符
-- 预期输出: 至少有一个订单的客户的 name 和 city



-- 练习 3: 查询没有下过订单的客户信息
-- 提示: 使用子查询 (SELECT DISTINCT customer_id FROM orders) 或 NOT IN 操作符，或者使用 LEFT JOIN + WHERE IS NULL
-- 预期输出: 在 orders 表中没有记录的客户信息



-- 练习 4: 使用 CTE 查询每个客户的总订单金额，并只显示总金额大于 150 的客户及其总金额
-- 提示: 创建一个 CTE 计算每个客户的总金额，然后在主查询中过滤
/*
WITH CustomerTotal AS (
    SELECT customer_id, SUM(amount) as total_amount
    FROM orders
    GROUP BY customer_id
)
SELECT ... FROM CustomerTotal WHERE ...
*/
-- 预期输出: 两列 (customer_id, total_amount)，只包含 total_amount > 150 的行



-- 练习 5: 查询订单金额最高的订单对应的客户姓名
-- 提示: 可以使用子查询找到最高金额，或者使用 CTE/窗口函数 (如果学过)
-- 预期输出: 一个客户姓名



-- 练习 6: 使用 CTE 查询来自北京 (Beijing) 的客户，然后查询这些客户的订单总数
-- 提示: 第一个 CTE 选出北京客户的 ID，第二个 CTE/主查询连接 orders 表计算订单数
/*
WITH BeijingCustomers AS (
    SELECT customer_id FROM customers WHERE city = '北京'
)
SELECT COUNT(*) FROM orders WHERE customer_id IN (SELECT customer_id FROM BeijingCustomers);
*/
-- 预期输出: 一个数字，表示北京客户的总订单数 