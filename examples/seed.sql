-- Synthetic only. Amounts are integer cents; snapshot fixed at 2026-10-31.
CREATE TABLE customers(tenant_id TEXT NOT NULL, customer_id TEXT NOT NULL, name TEXT NOT NULL, email TEXT, PRIMARY KEY(tenant_id,customer_id));
CREATE TABLE orders(tenant_id TEXT NOT NULL, order_id TEXT NOT NULL, customer_id TEXT NOT NULL, amount_cents INTEGER NOT NULL CHECK(amount_cents>=0), status TEXT NOT NULL CHECK(status IN ('paid','pending','cancelled')), order_date TEXT NOT NULL, PRIMARY KEY(tenant_id,order_id), FOREIGN KEY(tenant_id,customer_id) REFERENCES customers(tenant_id,customer_id));
INSERT INTO customers VALUES ('a','1','客户甲','shared@example.test'),('a','2','客户乙','shared@example.test'),('b','1','客户丙',NULL);
INSERT INTO orders VALUES ('a','o1','1',10000,'paid','2026-10-01'),('a','o2','2',20000,'paid','2026-10-02'),('a','o3','1',90000,'cancelled','2026-10-03'),('a','o4','2',5000,'pending','2026-10-04'),('b','o1','1',7000,'paid','2026-10-05');
