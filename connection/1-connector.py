import os
import snowflake.connector

conn = snowflake.connector.connect(
    account='lga76011.us-east-1',
    user='pikeche@phdata.io',
    authenticator = 'externalbrowser',
    # password=os.environ['SNOWSQL_PWD'],
    database='SANDBOX',
    schema='PIKECHE',
    role='DATAENGINEERING_ALL',
    warehouse='SANDBOX_WH'
)

# (1) fetching row by row
cur = conn.cursor()
cur.execute('select * from SANDBOX.STREAMLIT.employees')
for row in cur: print(row)

# (2) getting the whole set
df = cur.fetch_pandas_all()
print(df)
