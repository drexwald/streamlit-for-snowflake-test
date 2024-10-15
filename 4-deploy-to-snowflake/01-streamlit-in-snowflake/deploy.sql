-- to be deployed as a Streamlit App with: snowsql -c demo_conn -f deploy.sql
use schema sandbox.pikeche;

create or replace stage streamlit_stage;

put file:///Users/pikeche/Documents/snowflake/udemy/streamlit-for-snowflake-test/4-deploy-to-snowflake/01-streamlit-in-snowflake/app.py @streamlit_stage
    overwrite=true auto_compress=false;

create or replace streamlit first_streamlit_app
    root_location = '@sandbox.pikeche.streamlit_stage'
    main_file = '/app.py'
    query_warehouse = 'SANDBOX_WH';
show streamlits;