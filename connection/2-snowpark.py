import os
from snowflake.snowpark import Session

pars = {
    "account": 'lga76011.us-east-1',
    "user": 'pikeche@phdata.io',
    "authenticator": 'externalbrowser',
    "database": 'SANDBOX',
    "schema": 'PIKECHE',
    "warehouse": 'SANDBOX_WH',
    "role": 'DATAENGINEERING_ALL'    
}
session = Session.builder.configs(pars).create()

# basic usage
df = session.sql('select * from employees')
rows = df.collect()
for row in rows:
    print(row)

# alternative w/ pandas DataFrame
dfp = df.to_pandas()
print(dfp)