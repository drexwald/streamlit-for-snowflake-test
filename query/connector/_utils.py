import os
import snowflake.connector

def getConnection():
    return snowflake.connector.connect(
        account='lga76011.us-east-1',
        user='pikeche@phdata.io',
        authenticator = 'externalbrowser',
        # password=os.environ['SNOWSQL_PWD'],
        database='SANDBOX',
        schema='STREAMLIT',
        role='DATAENGINEERING_ALL',
        warehouse='SANDBOX_WH'
    )
