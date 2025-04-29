-- 删除已存在的表 (如果存在)，以便脚本可以重复运行
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;

-- 创建 customers 表
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY, -- 客户ID，主键
    name TEXT NOT NULL,             -- 客户姓名，不能为空
    city TEXT                       -- 所在城市
);

-- 创建 orders 表
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,     -- 订单ID，主键
    customer_id INTEGER,            -- 客户ID，关联 customers 表
    order_date DATE,                -- 订单日期
    amount REAL,                    -- 订单金额
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) -- 外键约束
);

-- 设置 SQLite 以读取 CSV 文件
.mode csv

-- 导入 customers.csv 数据 (确保你的终端在此项目的根目录下运行此脚本)
-- 或者在 DB Browser for SQLite 中使用 文件 -> 导入 -> 从CSV导入表 功能
.import data/customers.csv customers

-- 导入 orders.csv 数据
.import data/orders.csv orders

-- (可选) 显示导入后的表的行数，进行快速验证
SELECT 'customers 表行数:', COUNT(*) FROM customers;
SELECT 'orders 表行数:', COUNT(*) FROM orders; 