#   .streamlit/secrets.toml

[connections_snowflake]
    account = "******"
    user = "********"
    authenticator = "externalbrowser"
    # password=os.environ["SNOWSQL_PWD"]
    database = "SANDBOX"
    schema = "****"
    role = "********"
    warehouse = "SANDBOX_WH"
    client_session_keep_alive = true

# using streamlit secrets tunnel -- st.connections("snowflake)
[connections.snowflake]
    account = "lga76011.us-east-1"
    user = "pikeche@phdata.io"
    authenticator = "externalbrowser"
    # password=os.environ["SNOWSQL_PWD"]
    database = "SANDBOX"
    schema = "PIKECHE"
    role = "DATAENGINEERING_ALL"
    warehouse = "SANDBOX_WH"
    client_session_keep_alive = true


