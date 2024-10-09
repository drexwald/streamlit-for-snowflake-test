


Streamlit in Snowflake (SIS)
 Basic Introduction and Deployment Strategy For Multi-Environment Setup for Production

Revision History
Version
Author
Description
Date
1.0
Balbir
Information architecture on how to build and deploy Streamlit in Snowflake in Production
16-sep-2024


























Table of Contents
Streamlit In Snowflake (SIS)
Short Introduction To Streamlit
Development & Data Flow
Why Use Streamlit?
Other key feature of Streamlit
Streamlit in Snowflake
Key Points
Limitations
Deployment and Recommended Options
Snowsight
SQL
Snowflake CLI
Streamlit in Snowflake Infrastructure Setup
Information Architecture
Provision a Database and Schema
Provision roles to manage and view Streamlit App
Provision a Warehouse used by the Streamlit App
Assign privileges to create and manage Streamlit App
Assign privileges to view only Streamlit App
Assign roles to the User
Prepare Logging and Tracing Environment
Team Role and Responsibilities
DEV Environment
TEST Environment
PROD  Environment
Development and Deployment Setup
Provision a Git Resource
Local Installation in your Workstation
Project Initialization
Update main_file and add Page file
Running the App locally (Development Mode)
Deploying the App to Streamlit in Snowflake from GIT
Preparing the Pipeline Code
Checkin Code Changes to GIT Branch
Provide Access to Streamlit App Provisioned to STREAMLIT_ROLE
Reference/Training Material

Streamlit In Snowflake (SIS)
Snowflake acquired Streamlit in early 2022 with the goal of democratizing data apps. Snowflake users, especially Data Scientists, Machine Learning and Data Engineers, use SIS to quickly build Streamlit applications to interact with data in a secure environment without having to leave Snowflake.
Short Introduction To Streamlit
Streamlit is an Open Source Python library used primarily for building data applications. Streamlit allows engineers to create a data-driven web application using pure Python instead of Javascript, HTML, or CSS, as is the case with traditional web applications.

The structure of Streamlite is Client-Server. Your app's Python backend is the server, and your browser's frontend is the client. Your computer runs both the server and the client when you develop an app locally. The server and client run on different machines when someone views your app over a local or global network. 
Development & Data Flow
With Streamlit, you make changes to your data script file, save it, and Streamlit will display the changes automatically. When the source code changes or the user interacts with the web application, Streamlit reruns the entire script. Use Streamlit caching to avoid running expensive code multiple times to improve performance.

@st.cache_data
@st.cache_resource
Serializable Objects
Functions
Dataframes
API Calls
etc.
Unserializable Objects
ML models
Database Connections





Why Use Streamlit?
Simplicity: Streamlit allows you to create powerful UIs with just a few lines of Python code. Streamlit focuses on enabling developers to build functional web apps quickly and efficiently.
Interactivity: Streamlit makes it easy to add interactive widgets like sliders, text inputs, buttons, and file uploaders. These elements enable users to modify inputs dynamically and visualize the effects immediately.
Real-time updates: One of the standout features of Streamlit is its ability to rerun scripts in real-time as users interact with the app. When a user changes a widget or input, Streamlit automatically re-executes the script from top to bottom, updating the content in real-time.
No web development needed: Streamlit abstracts away the complexities of web development, allowing you to focus on building your app’s functionality rather than worrying about front-end design.
Integration with data science tools: Streamlit integrates seamlessly with Python's most popular libraries, such as Pandas, NumPy, Matplotlib, and Plotly, making it easy to visualize data or integrate machine learning models with minimal effort.
Other key feature of Streamlit
Display text
Display plots (matplotlib, plotly)
Interactivity (radio buttons, checkboxes etc..)
Multi-page apps
Database Connection
Stateful apps
Streamlit in Snowflake
Key Points
The Streamlit app adheres to Snowflake's access control framework and is schema-level objects.
The streamlit app runs with the owner's privileges, not with those of the caller.
Use the warehouse provisioned by the app owner.
It uses the database and schema that the Streamlit in Snowflake application was created in, not the database and schema that the user is currently using.
SIS applies additional restrictions to Owner's rights stored procedures.
Limitations
Using AWS PrivateLink or Azure Private Link is not supported.
The only privileges available to manage and access the Streamlit app are CREATE STREAMLIT and USAGE ON STREAMLIT.  It is not possible to separate permissions for CREATE, UPDATE, RUN, and DELETE Streamlit Apps. A role with CREATE STREAMLIT can contribute to or destroy Streamlit apps.


For more limitation refer to Limitations and unsupported features | Snowflake Documentation 
Deployment and Recommended Options
In Snowflake, we have three options for deploying and managing Streamlit, which we will discuss briefly here. Additionally, we will outline the recommended approach for productionizing Streamlit Apps.

All these three options defined here require Streamlit in Snowflake Infrastructure Setup steps completed.
Snowsight
You can create a single-page Streamlite app using Snowsight. Streamlit in Snowflake in Snowsight provides a Python editor to write, edit and run code for a Streamlit app.

This approach is not recommended for managing and deploying productionized Streamlite apps. There is no versioning of code, developers are unable to use a local IDE for development and testing, and there is no continuous integration and deployment (CI/CD) workflow to propagate the changes from lower to higher environments in a controlled manner. Additionally, enabling configuration changes like external network access and multi-page requires SQL execution with a challenge to identify the right ROOT Location in the Stage object.

Reference: Create and deploy Streamlit apps using Snowsight | Snowflake Documentation 
SQL
Create a Streamlit app in Snowflake Using SQL. This approach is not recommended for managing and deploying productionized Streamlite apps. 

Pros: You have more control over parameters like ROOT_LOCATION, MAIN_FILE, etc.

Cons: There is no out-of-the box solution available for continuous integration and deployment (CI/CD) workflow based on Git.
Snowflake CLI
	Snowflake CLI (Command-Line Interface) is a tool provided by Snowflake to interact with and manage your Snowflake data warehouse directly from the command line. Snowflake CLI is recommended for managing and deploying productionized Streamlite apps in Streamlit in Snowflake.

The Snowflake CLI provides a template for setting up a Streamlit app project with all the necessary configuration files. Due to its CLI-based nature, Streamlit App can be integrated into any workflow or script via Snowflake CLI commands making CI/CD workflow a very favorable solution for productionizing the Streamlit in Snowflake apps.

Note: The Snowflake CLI streamlit deploy command only supports updating or creating new files in the stage location. Dropped files must be dealt with separately using the Snowflake CLI stage command in your code or GIT Pipeline. 
Streamlit in Snowflake Infrastructure Setup
To get started with using Streamlit in Snowflake we have to make sure infrastructure prerequisites are met. The following diagram illustrates what we hope to accomplish at a high level.

Assumption: Snowflake user is already provisioned.

BitBucket Repository: https://bitbucket.org/phdata/streamlit_template/src/dev/ 
Information Architecture

Provision a Database and Schema
Tip: The Streamlit App should generally be provisioned within the Data Product database where we have Business Ready data.
use role sysadmin;

set db_name='streamlit_db';
set schema_name = 'streamlit_schema';

create database identifier($db_name);
create schema identifier($schema_name);
Provision roles to manage and view Streamlit App
Two roles are provisioned here, one for owening, managing and editing the Streamit App and another for viewing only.

Tip: The Creator role can be related to FR_ENGINEER role in our IA recommendation. The Viewer role can be related to FR_READER role in our IA recommendation. For Streamlit, we recommend having a Project Role associated with the Service Account that has all necessary permissions to manage the app and access source data.

use role securityadmin;

set editor_rl_name='streamlit_creator'; //Managing and Editing Streamlit App
set viewer_rl_name='streamlit_role'; //View and Run Streamlit App

create role identifier($editor_rl_name);
create role identifier($viewer_rl_name);
Provision a Warehouse used by the Streamlit App
set streamlit_wh_name='steamlit_sbx_wh';
use role sysadmin;
create warehouse if not exists identifier($streamlit_wh_name);
Assign privileges to create and manage Streamlit App
It is worth noting that you would be granting CREATE STREAMLIT and CREATE STAGE grants if you have USAGE privileges on the database and schema containing the Streamlit application.

use role securityadmin;

set editor_rl_name='streamlit_creator';
set db_name='streamlit_db';
set schema_name = 'streamlit_schema';
set namespace = 'streamlit_db.streamlit_schema';
set streamlit_wh_name='steamlit_sbx_wh';

GRANT USAGE ON SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
GRANT USAGE ON DATABASE identifier($db_name) TO ROLE identifier($editor_rl_name);
GRANT CREATE STREAMLIT ON SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
GRANT CREATE STAGE ON SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
GRANT READ,WRITE ON FUTURE STAGES IN SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
GRANT USAGE ON WAREHOUSE identifier($streamlit_wh_name) TO ROLE identifier($editor_rl_name);
GRANT CREATE TABLE ON SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
GRANT INSERT,DELETE,SELECT,DELETE ON FUTURE TABLES IN SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
Assign privileges to view only Streamlit App
When you share a Streamlit App from Snowsight to another role, the USAGE privilege is automatically granted to the new role. However, if a Streamlit app is created in a schema with MANAGED ACCESS, the USAGE privilege must be manually granted to the new role using privilege “USAGE ON STREAMLIT”.

use role securityadmin;

set viewer_rl_name='streamlit_role';
set db_name='streamlit_db';
set schema_name = 'streamlit_schema';
set namespace = 'streamlit_db.streamlit_schema';
set streamlit_wh_name='steamlit_sbx_wh';
set streamlit_app_name ='streamlit_db.streamlit_schema.streamlit_app';

GRANT USAGE ON SCHEMA identifier($namespace) TO ROLE identifier($viewer_rl_name);
GRANT USAGE ON DATABASE identifier($db_name) TO ROLE identifier($viewer_rl_name);
//GRANT USAGE ON STREAMLIT identifier($streamlit_app_name) TO ROLE identifier($viewer_rl_name);
GRANT USAGE ON WAREHOUSE identifier($streamlit_wh_name) TO ROLE identifier($viewer_rl_name);
GRANT CREATE STAGE ON SCHEMA identifier($namespace) TO ROLE identifier($viewer_rl_name);
GRANT SELECT ON FUTURE TABLES IN SCHEMA identifier($namespace) TO ROLE identifier($editor_rl_name);
Assign roles to the User
Members of the development team should be assigned the 'streamlit_creator' role, and end users should be assigned the 'streamlit_role' role.

With the role streamlit_creator, we can create a sample table that will be used to populate some data from the streamlit app.

CREATE TABLE streamlit_db.streamlit_schema.SAMPLE_PEOPLE(
NAME VARCHAR(100),
EMAIL VARCHAR(100),
ID NUMBER
);
Prepare Logging and Tracing Environment

USE ROLE SYSADMIN;
CREATE DATABASE IF NOT EXISTS SNF_ACCOUNT_EVENTS;
CREATE SCHEMA IF NOT EXISTS SNF_ACCOUNT_EVENTS.LOGGING_AND_TRACING;

-- Create an event table if it doesn't already exist
CREATE EVENT TABLE SNF_ACCOUNT_EVENTS.LOGGING_AND_TRACING.EVENTS;

-- Associate the event table with the account
ALTER ACCOUNT SET EVENT_TABLE = SNF_ACCOUNT_EVENTS.LOGGING_AND_TRACING.EVENTS;

-- Set log level for the database containing your app
ALTER DATABASE streamlit_db SET LOG_LEVEL = INFO;

-- Set trace level for the database containing your app
ALTER DATABASE streamlit_db SET TRACE_LEVEL = ON_EVENT;
Team Role and Responsibilities

To get started with development of Streamlit App, it's important to understand ownership and management of Streamlit App in different environments, such as Dev, Test, and Production.

EPO 
DE
ML/DS
Using Provision Tool to provision and manage infrastructure	
Dashboard migration from one platform to Streamlit in Snowflake
Creating a dashboard to represent Cortex Studio data.
Developing conversational apps 
Creating complex data applications that require sophisticated interactive data applications that involve building and managing models as well as creating interactive data dashboards based on the models' output.

DEV Environment
All deployments to the Streamlit App should be done via CICD using a Project Service Account, which should be owned by the operations team. A developer should only have read access to an app.

Developers must be part of the Viewer Role with sufficient privileges to view and run Streamlit Apps.
TEST Environment
All deployments to the Streamlit App should be done via CICD using a Project Service Account, which should be owned by the operations team. 

A developer should only have read access to an app.
PROD  Environment
All deployments to the Streamlit App should be done via CICD using a Project Service Account, which should be owned by the operations team. 

A developer should only have read access to an app if they have sufficient approvals to view the data.
Development and Deployment Setup

To get started you can use any choice of your editor which has support for Python and Git Plugin.
Provision a Git Resource
It is very simple to set up a BitBucket repository and clone it to your local computer, and there are many articles available on the web about how to do it, but here are the steps you should follow.

Create a new repository in BitBucket 
Create three branches dev, test, and prod
Set appropriate branch permissions on dev, test and prod. Minimum would be no one should be able to delete these branches.
Clone the repository in your local workstation.
Go to the root location of your repository.
Create a new branch feature/initial_Setup from dev branch.
Local Installation in your Workstation
Install Streamlit be sure to check the version of Streamlit in Snowflake supported (Getting started with Streamlit in Snowflake) 

Using a Python Virtual Environment (12. Virtual Environments and Packages - Python 3.12.6 documentation) is always recommended, so create a Virtual Environment and follow these steps.

During the preparation of this document, I was using Python 3.10.14.

> python --version
Python 3.10.14

> pip install streamlit

> streamlit version
Streamlit, version 1.35.0

> snow --version
Snowflake CLI version: 2.8.1

Project Initialization
With just a few lines of code, you can create your first app with Streamlit. Here are the steps you need to follow:

Initialize a sample Streamlit project using Snowflake CLI init command from terminal.

#Initialize a sample project
snow init streamlit  --template example_streamlit

Update config.toml with Snowflake Connection details (Specifying your Snowflake credentials ). In config.toml, all groups except development should use a service account.

The BitBucket Pipeline script explains how to use Password for the connection.

The database and schema parameters point to the location where Streamlit in Snowflake will be provisioned.
	
default_connection_name = "development"


[cli.logs]
save_logs = true
path = "./logs"
level = "info"


[connections.development]
account = "<SNF_ACCOUNT_ID>"
user = "<USERID>"
role = "streamlit_creator"
authenticator = "externalbrowser"
warehouse = "streamlit_sbx_wh"


[connections.sandbox]
account = "<SNF_ACCOUNT_ID>"
user = "<USERID>"
role = "streamlit_creator"
database = "streamlit_db"
schema = "streamlit_schema"
warehouse = "streamlit_sbx_wh"


[connections.test]
account = "<SNF_ACCOUNT_ID>"
user = "<USERID>"
role = "streamlit_creator"
database = "streamlit_db"
schema = "streamlit_schema"
warehouse = "streamlit_sbx_wh"


[connections.prod]
account = "<SNF_ACCOUNT_ID>"
user = "<USERID>"
role = "streamlit_creator"
database = "streamlit_db"
schema = "streamlit_schema"
warehouse = "streamlit_sbx_wh"

Test the Snowflake Connection
#Test Snowflake Connection
cd streamlit
snow --config-file=./config.toml connection test --connection="development"

Update environment.yml file with package requirement for Streamlit App

name: sf_env
channels:
  - snowflake
dependencies:
  - streamlit=1.35.0

Create a project definition file to support CICD for multi-environment, create one project definition file for each enviornment. 

Because I am using the same Snowflake Account, Database, and Schema, I am separating project definition files by environment. You can adjust this project definition according to your requirement.

Note: If you plan to use a pre-signed URL with an internal stage, the stage must first be created with ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE') and defined here. Internal Stages are not encrypted by Snowflake CLI Streamlit Deploy.
 
Dev (snowflake_dev.yml)

definition_version: 1
streamlit:
 name: streamlit_app_dev
 stage: streamlit_app_dev_stage
 query_warehouse: streamlit_sbx_wh
 main_file: streamlit_app.py
 env_file: environment.yml
 pages_dir: pages/

Test(snowflake_test.yml)

definition_version: 1
streamlit:
 name: streamlit_app_test
 stage: streamlit_app_test_stage
 query_warehouse: streamlit_test_wh
 main_file: streamlit_app.py
 env_file: environment.yml
 pages_dir: pages/

Prod(snowflake_prod.yml)

definition_version: 1
streamlit:
 name: streamlit_app_prod
 stage: streamlit_app_prod_stage
 query_warehouse: streamlit_prod_wh
 main_file: streamlit_app.py
 env_file: environment.yml
 pages_dir: pages/
Update main_file and add Page file
main_file = streamlit_app.py

Since we would like to run this code from our local workstation as well as from Streamlit in Snowflake in local mode code doesn’t have access to the active default snowpark connection. For that reason, we rely on the function getSnowflakeSession() to take a local development path if there is no default active connection available.

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSessionException
import streamlit as st
import pandas as pd
import logging

logger = logging.getLogger("simple_logger")

@st.cache_resource
def getSnowflakeSession():
    session = None
    try:
        logger.info("Getting active default session for Stremlit App.")
        session = get_active_session()
    except SnowparkSessionException :
        logger.warning("Not able to get active default session for Stremlit App.")
        logger.info("Building a active  session for Stremlit App, only supported for local development mode.")
        session = Session.builder.config("connection_name", "development").create()

    return session

# Set page config
st.set_page_config(layout="centered")

# Get current session
session = getSnowflakeSession()

# Give your app a title
st.title("Input Sample Data")

def populate_data():
    id = st.session_state.id
    name = st.session_state.name
    email = st.session_state.email

    if "@" not in email:
        st.write(":red[Not a valid email ID]")
        return False
    try:
        session.sql("INSERT INTO STREAMLIT_DB.STREAMLIT_SCHEMA.SAMPLE_PEOPLE VALUES (?, ?,?)",params=[name,email,id]).collect()
        container.write(f":green[Record inserted!]")
        container.write(f"Record List")
        rows = session.sql("SELECT * FROM STREAMLIT_DB.STREAMLIT_SCHEMA.SAMPLE_PEOPLE").collect()
        container.write(rows)
    except Exception as ex :
        container.write(f":red[{ex}]")
    st.session_state.insert_status = True

with st.form(key="sample"):
    id = st.number_input(label="ID",key="id",min_value=1,value=1)
    name = st.text_input(label="NAME",key="name")
    email = st.text_input(label="EMAIL",key="email")

    form_submit = st.form_submit_button("Submit Form",on_click=populate_data)

container = st.container()




When you run your Streamlit app code, you can capture log messages and trace events, then analyze the results with SQL. All logs should be found in table “SNF_ACCOUNT_EVENTS.LOGGING_AND_TRACING”

Page

Create a file pages/HelloWorldPage.py to demonstrate multi page support.

import streamlit as st
st.title("Example page")
Running the App locally (Development Mode)
Navigate to the directory where the Python script is saved and run it:
export SNOWFLAKE_HOME=$PWD
streamlit run streamlit_app.py

With your Snowflake account, you will be asked to authenticate externally via your browser and a session detail will be displayed.
Deploying the App to Streamlit in Snowflake from GIT
Pipeline prerequisites must be met before we can start with GIT checkin and checkout.
Preparing the Pipeline Code
Enable Pipelines in your repository from Repository settings -> pipeline -> settings 
Create three Deployments Dev,Test, and Prod
Under each deployment, create a secret variable called SNOWFLAKE_PASSWORD with the value set to Snowflake User Account password.
Pipeline Code for Multi-Environment deployment. 
https://bitbucket.org/phdata/streamlit_template/src/main/bitbucket-pipelines.yml 
image: python:3.10.14

pipelines:

  pull-requests:
    '{feature/*}': #PR branch -> Dev
      - step:
          name: "Dry Run for dev"
          deployment: dev
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_dev.yml snowflake.yml
            - snow --config-file=/tmp/config.toml connection test --connection="sandbox"

    '{hotfix_prod/*}': #Hotfix PR branch -> prod
      #- step: *security-scan
      - step:
          name: "Dry Run for Prod"
          deployment: prod
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_prod.yml snowflake.yml
            - snow --config-file=/tmp/config.toml connection test --connection="prod"

    dev: #PR Dev -> Test
      - step:
          name: "Dry Run for test"
          deployment: test
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_test.yml snowflake.yml
            - snow --config-file=/tmp/config.toml connection test --connection="test"

    test: #PR tst -> main
      - step:
          name: "Dry Run for prod"
          deployment: prod
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_prod.yml snowflake.yml
            - snow --config-file=/tmp/config.toml connection test --connection="prod"

  branches:
    dev:
      - step:
          name: "Provision Run for dev"
          deployment: dev
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_dev.yml snowflake.yml
	     - stage_name=$(cat snowflake.yml | shyaml get-value streamlit.stage)
     - stage_foler_name=$(cat snowflake.yml | shyaml get-value  streamlit.name)
     - chmod 0777 ../bin/cleanup_streamlit_stage_folder.sh
     - ../bin/cleanup_streamlit_stage_folder.sh $stage_name $stage_foler_name prod
		
            - snow --config-file=/tmp/config.toml streamlit deploy --replace --connection="sandbox"

    test:
      - step:
          name: "Provision Run for tst"
          deployment: test
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_test.yml snowflake.yml
	     - stage_name=$(cat snowflake.yml | shyaml get-value streamlit.stage)
     - stage_foler_name=$(cat snowflake.yml | shyaml get-value  streamlit.name)
     - chmod 0777 ../bin/cleanup_streamlit_stage_folder.sh
     - ../bin/cleanup_streamlit_stage_folder.sh $stage_name $stage_foler_name prod	
            - snow --config-file=/tmp/config.toml streamlit deploy --replace --connection="test"

    main:
      - step:
          name: "Provision Run for prod"
          oidc: true
          deployment: prod
          script:
            - pip install -r requirements.txt
            - cd ./streamlit
            - cp ./config.toml /tmp/config.toml
            - chmod 0600 /tmp/config.toml
            - cp ./snowflake_prod.yml snowflake.yml
	     - stage_name=$(cat snowflake.yml | shyaml get-value streamlit.stage)
     - stage_foler_name=$(cat snowflake.yml | shyaml get-value  streamlit.name)
     - chmod 0777 ../bin/cleanup_streamlit_stage_folder.sh
     - ../bin/cleanup_streamlit_stage_folder.sh $stage_name $stage_foler_name prod	
            - snow --config-file=/tmp/config.toml streamlit deploy --replace --connection="prod"


Checkin Code Changes to GIT Branch
The changes to branch feature/initial_Setup should be committed and pushed
From feature/initial_Setup, create a PR pointing to dev.
Verify the Dry Run of the Dev pipeline. 
Merge the changes to the dev branch.
Verify the provision pipeline run which should provision dev streamlit app.

Create a PR from dev branch to test branch
Verify the Dry Run of the Test pipeline. 
Merge the changes to the test branch.
Verify the provision pipeline run which should provision test streamlit app.

Create a PR from test branch to main branch
Verify the Dry Run of the Prod pipeline. 
Merge the changes to the main branch.
Verify the provision pipeline run which should provision prod streamlit app.
Provide Access to Streamlit App Provisioned to STREAMLIT_ROLE
	To provide access to Streamlit App provisioned to end users and developers to test their apps in Streamlit in Snowflake, we have to share the App provisioned either using the GRANT command or by going to the App and sharing it with the role. Please refer to the section Assign privileges to view only Streamlit App

GRANT USAGE ON STREAMLIT identifier($streamlit_app_name) TO ROLE identifier($viewer_rl_name)
Reference/Training Material
About Streamlit in Snowflake
Getting Started With Snowpark for Python and Streamlit
Get started with Streamlit 
https://phdata.udemy.com/course/machine-learning-model-deployment-with-streamlit   
https://phdata.udemy.com/course/streamlit-for-snowflake/  (Recommended)
