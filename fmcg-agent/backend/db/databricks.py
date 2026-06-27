from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Get or create a Databricks connection."""
    try:
        conn = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Databricks: {str(e)}")


def run_query(sql_query: str) -> list[dict]:
    """
    Execute a SQL query against Databricks.

    Args:
        sql_query: The SQL query to execute

    Returns:
        List of dictionaries representing rows

    Raises:
        RuntimeError: If query fails
    """
    if not sql_query.strip():
        raise ValueError("SQL query cannot be empty")

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)

                try:
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                except Exception:
                    columns = []

                # Fetch up to 1000 rows to avoid memory issues
                rows = cursor.fetchall()[:1000]

                if columns:
                    return [dict(zip(columns, row)) for row in rows]
                return []

    except Exception as e:
        raise RuntimeError(f"Query execution failed: {str(e)}")


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

Join Keys:
- fact_orders.product_code = dim_products.product_code = dim_gross_price.product_code
- fact_orders.customer_code = dim_customers.customer_code
- fact_orders.date = dim_date.month_start_date
- dim_gross_price.year = CAST(YEAR(fact_orders.date) AS STRING)
"""