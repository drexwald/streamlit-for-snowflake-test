import os
from snowflake.snowpark import Session

def getSession():
    return Session.builder.configs({
        "account": 'lga76011.us-east-1',
        "user": 'pikeche@phdata.io',
        "authenticator": 'externalbrowser',
        "database": 'SANDBOX',
        "schema": 'STREAMLIT',
        "warehouse": 'SANDBOX_WH',
        "role": 'DATAENGINEERING_ALL'   
    }).create()
