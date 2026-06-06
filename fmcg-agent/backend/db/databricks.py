from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )

def run_query(sql_query: str) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

SCHEMA_CONTEXT = """
Tables in fmcg.gold:

1. fact_orders
   - date (date): first of month
   - product_code (string): SHA-256 hash
   - customer_code (string)
   - sold_quantity (double)

2. dim_customers
   - customer_code (string)
   - customer (string): "CustomerName-City"
   - market (string)
   - platform (string)
   - channel (string)

3. dim_products
   - product_code (string)
   - division (string)
   - category (string)
   - product (string)
   - variant (string)

4. dim_gross_price
   - product_code (string)
   - price_inr (double)
   - year (string)

5. dim_date
   - month_start_date (date)
   - date_key (int)
   - year (int)
   - month_name (string)
   - month_short_name (string)
   - quarter (string)
   - year_quarter (string)
"""