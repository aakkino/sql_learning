-- solutions/01_basic_select_solution.sql
-- 基础 SELECT 练习答案

-- 练习 1: 查询 customers 表中的所有数据
SELECT * FROM customers;

-- 练习 2: 查询 orders 表中 order_id 为 103 的订单信息
SELECT * FROM orders WHERE order_id = 103;

-- 练习 3: 查询 customers 表中城市为 '北京' 的客户姓名 (name) 和客户ID (customer_id)
SELECT name, customer_id FROM customers WHERE city = '北京';

-- 练习 4: 查询 orders 表中订单金额 (amount) 大于 100 的所有订单信息
SELECT * FROM orders WHERE amount > 100;

-- 练习 5: 查询 orders 表中订单日期 (order_date) 为 '2023-10-28' 的订单ID (order_id) 和订单金额 (amount)
SELECT order_id, amount FROM orders WHERE order_date = '2023-10-28';

-- 练习 6: 查询 customers 表中的所有客户姓名，并按姓名升序排序
SELECT name FROM customers ORDER BY name ASC;

-- 练习 7: 查询 orders 表中订单金额最高的前 3 个订单的所有信息
SELECT * FROM orders ORDER BY amount DESC LIMIT 3; 