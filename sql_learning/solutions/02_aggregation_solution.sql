-- solutions/02_aggregation_solution.sql
-- 聚合函数与分组练习答案

-- 练习 1: 计算 orders 表中的总订单数
SELECT COUNT(*) AS total_orders FROM orders;

-- 练习 2: 计算 orders 表中的总销售额 (所有订单金额 amount 的总和)
SELECT SUM(amount) AS total_sales FROM orders;

-- 练习 3: 计算 orders 表中平均订单金额
SELECT AVG(amount) AS average_order_amount FROM orders;

-- 练习 4: 查询每个客户 (customer_id) 的订单数量
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id;

-- 练习 5: 查询每个客户 (customer_id) 的总订单金额
SELECT customer_id, SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id;

-- 练习 6: 查询哪个城市 (city) 的客户数量最多
SELECT city
FROM customers
GROUP BY city
ORDER BY COUNT(customer_id) DESC
LIMIT 1;

-- 练习 7: 查询总订单金额大于 200 的客户ID (customer_id)
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 200;

-- 练习 8: 查询每个订单日期 (order_date) 的订单数量和总金额
SELECT order_date, COUNT(*) AS daily_order_count, SUM(amount) AS daily_total_sales
FROM orders
GROUP BY order_date; 