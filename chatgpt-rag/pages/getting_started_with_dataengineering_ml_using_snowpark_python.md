  1. Overview
  2. Setup Environment
  3. Data Engineering
  4. Data Pipelines
  5. Machine Learning
  6. Streamlit Application
  7. Cleanup
  8. Conclusion And Resources

[ _close_](/) _menu_

# Getting Started with Data Engineering and ML using Snowpark for Python and
Snowflake Notebooks

 _access_time_ 48 mins remaining

## 1\. Overview

By completing this guide, you will be able to go from raw data to an
interactive application that can help organization optimize their advertising
budget allocation.

Here is a summary of what you will be able to learn in each step by following
this quickstart:

  * **Setup Environment** : Use stages and tables to ingest and organize raw data from S3 into Snowflake
  * **Data Engineering** : Leverage Snowpark for Python DataFrames in Snowflake Notebook to perform data transformations such as group by, aggregate, pivot, and join to prep the data for downstream applications
  * **Data Pipelines** : Use Snowflake Tasks to turn your data pipeline code into operational pipelines with integrated monitoring
  * **Machine Learning** : Process data and run training job in Snowflake Notebook using the Snowpark ML library, and register ML model and use it for inference from Snowflake Model Registry
  * **Streamlit** : Build an interactive Streamlit application using Python (no web development experience required) to help visualize the ROI of different advertising spend budgets

## What is Snowpark?

Snowpark is the set of libraries and code execution environments that run
Python and other programming languages next to your data in Snowflake.
Snowpark can be used to build data pipelines, ML models, apps, and other data
processing tasks.

![Snowpark](img/406ae6c6138972cf.png)

**Client Side Libraries** \- Snowpark libraries can be installed and
downloaded from any client-side notebook or IDE and are used for code
development and deployment. Libraries include the Snowpark API for data
pipelines and apps and the Snowpark ML API for end to end machine learning.

**Elastic Compute Runtimes** \- Snowpark provides elastic compute runtimes for
secure execution of your code in Snowflake. Runtime options include: Python,
Java, and Scala in warehouses, container runtimes for out-of-the-box
distributed processing with CPUs or GPUs using any Python framework, or custom
runtimes brought in from Snowpark Container Services to execute any language
of choice with CPU or GPU compute.

Learn more about [Snowpark](https://www.snowflake.com/snowpark/).

## What is Snowflake ML?

Snowflake ML is the integrated set of capabilities for end-to-end machine
learning in a single platform on top of your governed data. Snowflake ML can
be used for fully custom and out-of-the-box workflows. For ready-to-use ML,
analysts can use ML Functions to shorten development time or democratize ML
across your organization with SQL from Studio, our no-code user interface. For
custom ML, data scientists and ML engineers can easily and securely develop
and productionize scalable features and models without any data movement,
silos or governance tradeoffs.

To get started with Snowflake ML, developers can use the Python APIs from the
[Snowpark ML library](https://docs.snowflake.com/en/developer-guide/snowpark-
ml/index), directly from Snowflake Notebooks (public preview) or downloaded
and installed into any IDE of choice, including Jupyter or Hex.

![Snowpark](img/21f2fdac4da5b2fd.png)

This quickstart will focus on

  * Snowpark ML Modeling API, which enables the use of popular Python ML frameworks, such as scikit-learn and XGBoost, for feature engineering and model training without the need to move data out of Snowflake.
  * Snowflake Model Registry, which provides scalable and secure model management of ML models in Snowflake, regardless of origin. Using these features, you can build and operationalize a complete ML workflow, taking advantage of Snowflake's scale and security features.

**Feature Engineering and Preprocessing** \- Improve performance and
scalability with distributed execution for common scikit-learn preprocessing
functions.

**Model Training** \- Accelerate model training for scikit-learn, XGBoost and
LightGBM models without the need to manually create stored procedures or user-
defined functions (UDFs), and leverage distributed hyperparameter
optimization.

![Snowpark](img/8de45cc3c02b6206.png)

**Model Management and Batch Inference** \- Manage several types of ML models
created both within and outside Snowflake and execute batch inference.

![Snowpark](img/301e42874ba97d1f.png)

## What is Streamlit?

Streamlit enables data scientists and Python developers to combine Streamlit's
component-rich, open-source Python library with the scale, performance, and
security of the Snowflake platform.

Learn more about [Streamlit](https://www.snowflake.com/en/data-
cloud/overview/streamlit-in-snowflake/).

## What You Will Learn

  * How to analyze data and perform data engineering tasks using Snowpark DataFrames and APIs
  * How to use open-source Python libraries from curated Snowflake Anaconda channel
  * How to create Snowflake Tasks to automate data pipelines
  * How to train ML model using Snowpark ML in Snowflake
  * How to register ML model and use it for inference from Snowpark ML Model Registry
  * How to create Streamlit application that uses the ML Model for inference based on user input

## What You Will Build

  * A data engineering pipeline
  * A machine learning model
  * A Streamlit application

## Prerequisites

  * A Snowflake account with [Anaconda Packages enabled by ORGADMIN](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages.html#using-third-party-packages-from-anaconda). If you do not have a Snowflake account, you can register for a [free trial account](https://signup.snowflake.com/?utm_cta=quickstarts_).
  * A Snowflake account login with ACCOUNTADMIN role. If you have this role in your environment, you may choose to use it. If not, you will need to 1) Register for a free trial, 2) Use a different role that has the ability to create database, schema, tables, stages, tasks, user-defined functions, and stored procedures OR 3) Use an existing database and schema in which you are able to create the mentioned objects.

IMPORTANT: Before proceeding, make sure you have a Snowflake account with
Anaconda packages enabled by ORGADMIN as described
[here](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-
packages#getting-started).

## 2\. Setup Environment

## Create Tables and Load Data

Log into [Snowsight](https://docs.snowflake.com/en/user-guide/ui-
snowsight.html#) using your credentials to create tables and load data from
Amazon S3.

IMPORTANT:

  * If you use different names for objects created in this section, be sure to update scripts and code in the following sections accordingly.
  * For each SQL script block below, select all the statements in the block and execute them top to bottom.

In a new SQL worksheet, run the following SQL commands to create the
[warehouse](https://docs.snowflake.com/en/sql-reference/sql/create-
warehouse.html), [database](https://docs.snowflake.com/en/sql-
reference/sql/create-database.html) and
[schema](https://docs.snowflake.com/en/sql-reference/sql/create-schema.html).

    
    
    USE ROLE ACCOUNTADMIN;
    
    CREATE WAREHOUSE IF NOT EXISTS DASH_S WAREHOUSE_SIZE=SMALL;
    CREATE DATABASE IF NOT EXISTS DASH_DB;
    CREATE SCHEMA IF NOT EXISTS DASH_SCHEMA;
    
    USE DASH_DB.DASH_SCHEMA;
    USE WAREHOUSE DASH_S;

In the same SQL worksheet, run the following SQL commands to create table
**CAMPAIGN_SPEND** from data hosted on publicly accessible S3 bucket.

    
    
    CREATE or REPLACE file format csvformat
      skip_header = 1
      type = 'CSV';
    
    CREATE or REPLACE stage campaign_data_stage
      file_format = csvformat
      url = 's3://sfquickstarts/ad-spend-roi-snowpark-python-scikit-learn-streamlit/campaign_spend/';
    
    CREATE or REPLACE TABLE CAMPAIGN_SPEND (
      CAMPAIGN VARCHAR(60), 
      CHANNEL VARCHAR(60),
      DATE DATE,
      TOTAL_CLICKS NUMBER(38,0),
      TOTAL_COST NUMBER(38,0),
      ADS_SERVED NUMBER(38,0)
    );
    
    COPY into CAMPAIGN_SPEND
      from @campaign_data_stage;

In the same SQL worksheet, run the following SQL commands to create table
**MONTHLY_REVENUE** from data hosted on publicly accessible S3 bucket.

    
    
    CREATE or REPLACE stage monthly_revenue_data_stage
      file_format = csvformat
      url = 's3://sfquickstarts/ad-spend-roi-snowpark-python-scikit-learn-streamlit/monthly_revenue/';
    
    CREATE or REPLACE TABLE MONTHLY_REVENUE (
      YEAR NUMBER(38,0),
      MONTH NUMBER(38,0),
      REVENUE FLOAT
    );
    
    COPY into MONTHLY_REVENUE
      from @monthly_revenue_data_stage;

In the same SQL worksheet, run the following SQL commands to create table
**BUDGET_ALLOCATIONS_AND_ROI** that holds the last six months of budget
allocations and ROI.

    
    
    CREATE or REPLACE TABLE BUDGET_ALLOCATIONS_AND_ROI (
      MONTH varchar(30),
      SEARCHENGINE integer,
      SOCIALMEDIA integer,
      VIDEO integer,
      EMAIL integer,
      ROI float
    )
    COMMENT = '{"origin":"sf_sit-is", "name":"aiml_notebooks_ad_spend_roi", "version":{"major":1, "minor":0}, "attributes":{"is_quickstart":1, "source":"streamlit"}}';
    
    INSERT INTO BUDGET_ALLOCATIONS_AND_ROI (MONTH, SEARCHENGINE, SOCIALMEDIA, VIDEO, EMAIL, ROI)
    VALUES
    ('January',35,50,35,85,8.22),
    ('February',75,50,35,85,13.90),
    ('March',15,50,35,15,7.34),
    ('April',25,80,40,90,13.23),
    ('May',95,95,10,95,6.246),
    ('June',35,50,35,85,8.22);

Optionally, you can also open [setup.sql](https://github.com/Snowflake-
Labs/sfguide-getting-started-dataengineering-ml-snowpark-
python/blob/main/setup.sql) in Snowsight and run all SQL statements to create
the objects and load data from AWS S3.

IMPORTANT: If you use different names for objects created in this section, be
sure to update scripts and code in the following sections accordingly.

## 3\. Data Engineering

The Notebook linked below covers the following data engineering tasks.

  1. Load data from Snowflake tables into Snowpark DataFrames
  2. Perform Exploratory Data Analysis on Snowpark DataFrames
  3. Pivot and Join data from multiple tables using Snowpark DataFrames
  4. Automate data pipelines using Snowflake Tasks

## Data Engineering Notebook

To get started, follow these steps:

  1. Click on [Snowpark_For_Python_DE.ipynb](https://github.com/Snowflake-Labs/sfguide-getting-started-dataengineering-ml-snowpark-python/blob/main/Snowpark_For_Python_DE.ipynb) to download the Notebook from GitHub. **_(NOTE: Do NOT right-click to download.)_**
  2. In your Snowflake account:

  * On the left hand navigation menu, click on **Projects** » **Notebooks**
  * On the top right, click on **Notebook** down arrow and select **Import .ipynb file** from the dropdown menu
  * Select the file you downloaded in step 1 above

  3. In the Create Notebook popup

  * For **Notebook location** , select DASH_DB and DASH_SCHEMA
  * For **SQL warehouse** , select DASH_S
  * Click on **Create** button

If all goes well, you should see the following Notebook:

![Snowflake DE NB](img/4c829868e8c27c19.png)

  4. On the top right, click on **Packages** and make sure you install `snowflake` package by typing it in the search box and clicking on the first one.

![Snowflake DE NB](img/748748281e6438a.png)

  5. On the top right, click on **Start**. **_(NOTE: The first time it will take a couple of mins to install the packages.)_**
  6. Once the packages are installed and the state changes from **Start** » **Starting** » **Active** , you can either click on **Run all** to execute all cells, or you can run individual cells in the order from top to bottom by clicking on the play icon on the top right corner of each cell.

## 4\. Data Pipelines

You can also operationalize the data transformations in the form of automated
data pipelines running in Snowflake.

In particular, in the [Data Engineering
Notebook](https://github.com/Snowflake-Labs/sfguide-getting-started-
dataengineering-ml-snowpark-python/blob/main/Snowpark_For_Python_DE.ipynb),
there's a section that demonstrates how to optionally build and run the data
transformations as [Snowflake Tasks](https://docs.snowflake.com/en/user-
guide/tasks-intro).

For reference purposes, here are the code snippets.

## **Campaign Spend**

This task automates loading campain spend data and performing various
transformations.

    
    
    def campaign_spend_data_pipeline(session: Session) -> str:
      # DATA TRANSFORMATIONS
      # Perform the following actions to transform the data
    
      # Load the campaign spend data
      snow_df_spend_t = session.table('campaign_spend')
    
      # Transform the data so we can see total cost per year/month per channel using group_by() and agg() Snowpark DataFrame functions
      snow_df_spend_per_channel_t = snow_df_spend_t.group_by(year('DATE'), month('DATE'),'CHANNEL').agg(sum('TOTAL_COST').as_('TOTAL_COST')).\
          with_column_renamed('"YEAR(DATE)"',"YEAR").with_column_renamed('"MONTH(DATE)"',"MONTH").sort('YEAR','MONTH')
    
      # Transform the data so that each row will represent total cost across all channels per year/month using pivot() and sum() Snowpark DataFrame functions
      snow_df_spend_per_month_t = snow_df_spend_per_channel_t.pivot('CHANNEL',['search_engine','social_media','video','email']).sum('TOTAL_COST').sort('YEAR','MONTH')
      snow_df_spend_per_month_t = snow_df_spend_per_month_t.select(
          col("YEAR"),
          col("MONTH"),
          col("'search_engine'").as_("SEARCH_ENGINE"),
          col("'social_media'").as_("SOCIAL_MEDIA"),
          col("'video'").as_("VIDEO"),
          col("'email'").as_("EMAIL")
      )
    
      # Save transformed data
      snow_df_spend_per_month_t.write.mode('overwrite').save_as_table('SPEND_PER_MONTH')
    
    # Register data pipeline function as a task
    root = Root(session)
    my_task = Task(name='campaign_spend_data_pipeline_task'
                   , definition=StoredProcedureCall(
                       campaign_spend_data_pipeline, stage_location='@dash_sprocs'
                   )
                   , warehouse='DASH_S'
                   , schedule=timedelta(minutes=3))
    
    tasks = root.databases[session.get_current_database()].schemas[session.get_current_schema()].tasks
    task_res = tasks.create(my_task,mode=CreateMode.or_replace)

## **Monthly Revenue**

This task automates loading monthly revenue data, performing various
transformations, and joining it with transformed campaign spend data.

    
    
    def monthly_revenue_data_pipeline(session: Session) -> str:
      # Load revenue table and transform the data into revenue per year/month using group_by and agg() functions
      snow_df_spend_per_month_t = session.table('spend_per_month')
      snow_df_revenue_t = session.table('monthly_revenue')
      snow_df_revenue_per_month_t = snow_df_revenue_t.group_by('YEAR','MONTH').agg(sum('REVENUE')).sort('YEAR','MONTH').with_column_renamed('SUM(REVENUE)','REVENUE')
    
      # Join revenue data with the transformed campaign spend data so that our input features (i.e. cost per channel) and target variable (i.e. revenue) can be loaded into a single table for model training
      snow_df_spend_and_revenue_per_month_t = snow_df_spend_per_month_t.join(snow_df_revenue_per_month_t, ["YEAR","MONTH"])
    
      # SAVE in a new table for the next task
      snow_df_spend_and_revenue_per_month_t.write.mode('overwrite').save_as_table('SPEND_AND_REVENUE_PER_MONTH')

## **Tasks DAG**

    
    
    # Delete the previous task
    task_res.delete()
    
    with DAG("de_pipeline_dag", schedule=timedelta(minutes=3)) as dag:
        # Create a task that runs our first pipleine
        dag_spend_task = DAGTask(name='campaign_spend_data_pipeline_task'
                            , definition=StoredProcedureCall(
                                        campaign_spend_data_pipeline, stage_location='@dash_sprocs'
                                    )
                            ,warehouse='DASH_S'
                            )
        # Create a task that runs our second pipleine
        dag_revenue_task = DAGTask(name='monthly_revenue_data_pipeline'
                              , definition=StoredProcedureCall(
                                    monthly_revenue_data_pipeline, stage_location='@dash_sprocs'
                                )
                            ,warehouse='DASH_S'
                            )
    
    # Shift right and left operators can specify task relationships
    dag_spend_task >> dag_revenue_task  # dag_spend_task is a predecessor of dag_revenue_task
    
    schema = root.databases[session.get_current_database()].schemas[session.get_current_schema()]
    dag_op = DAGOperation(schema)
    
    dag_op.deploy(dag)
    
    # A DAG is not suspended by default so we will suspend the root task that will suspend the full DAG
    root_task = tasks["DE_PIPELINE_DAG"]
    root_task.suspend()

### Run DAG

We can manually run DAGs even if they're suspended.

    
    
    # dag_op.run(dag)

### Resume Task

Here's how you can resume Tasks.

    
    
    # root_task = tasks["DE_PIPELINE_DAG"]
    # root_task.resume()

### Suspend Task

If you resumed the above tasks, suspend them to avoid unecessary resource
utilization by uncommenting and executing the following commands.

    
    
    # root_task = tasks["DE_PIPELINE_DAG"]
    # root_task.suspend()

## Tasks Observability

These tasks and their [DAGs](https://docs.snowflake.com/en/user-guide/tasks-
intro#label-task-dag) can be viewed in
[Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight-
tasks#viewing-individual-task-graphs) as shown below.

![Tasks-Observability](img/4d1d1310582c38c9.png)

## Error Notificatons For Tasks

You can also enable push notifications to a cloud messaging service when
errors occur while tasks are being executed. For more information, please
refer to the [documentation](https://docs.snowflake.com/en/user-guide/tasks-
errors).

## 5\. Machine Learning

PREREQUISITE: Successful completion of steps outlined under [Data
Engineering](https://github.com/Snowflake-Labs/sfguide-getting-started-
dataengineering-ml-snowpark-python/blob/main/Snowpark_For_Python_DE.ipynb).

The Notebook linked below covers the following machine learning tasks.

  1. Load features and target from Snowflake table into Snowpark DataFrame
  2. Prepare features for model training
  3. Train ML model using Snowpark ML in Snowflake
  4. Register ML model and use it for inference from Snowflake Model Registry

## Machine Learning Notebook

  1. Click on [Snowpark_For_Python_ML.ipynb](https://github.com/Snowflake-Labs/sfguide-getting-started-dataengineering-ml-snowpark-python/blob/main/Snowpark_For_Python_ML.ipynb) to download the Notebook from GitHub. **_(NOTE: Do NOT right-click to download.)_**
  2. In your Snowflake account:

  * On the left hand navigation menu, click on **Projects** » **Notebooks**
  * On the top right, click on **Notebook** down arrow and select **Import .ipynb file** from the dropdown menu
  * Select the file you downloaded in step 1 above

  3. In the Create Notebook popup

  * For **Notebook location** , select DASH_DB and DASH_SCHEMA
  * For **SQL warehouse** , select DASH_S
  * Click on **Create** button

If all goes well, you should see the following:

![Snowflake DE NB](img/82f1b3e4b0eb3b41.png)

  4. On the top right, click on **Packages** and make sure you install `snowflake-ml-python` package by typing it in the search box and selecting the first one.
  5. On the top right, click on **Start**. **_(NOTE: The first time it will take a couple of mins to install the packages.)_**
  6. Once the packages are installed and the state changes from **Start** » **Starting** » **Active** , you can either click on **Run all** to execute all cells, or you can run individual cells in the order from top to bottom by clicking on the play icon on the top right corner of every cell.

## 6\. Streamlit Application

Follow these steps to build Streamlit application in Snowsight.

**Step 1.** Click on **Streamlit** on the left navigation menu

**Step 2.** Click on **\+ Streamlit App** on the top right

**Step 3.** Enter **App title**

**Step 4.** Select **App location** (DASH_DB and DASH_SCHEMA) and **App
warehouse** (DASH_S)

**Step 5.** Click on **Create**

  * At this point, you will be provided code for an example Streamlit application

**Step 6.** Replace sample application code displayed in the code editor on
the left with the code provided in
[Snowpark_Streamlit_Revenue_Prediction_SiS.py](https://github.com/Snowflake-
Labs/sfguide-ad-spend-roi-snowpark-python-streamlit-scikit-
learn/blob/main/Snowpark_Streamlit_Revenue_Prediction_SiS.py)

**Step 7.** Click on **Run** on the top right

If all goes well, you should see the application in Snowsight as shown below.

![Streamlit-in-Snowflake](img/5091bfc3df14f2a5.png)

**Step 8.** Save data to Snowflake

In the application, adjust the advertising budget sliders to see the predicted
ROI for those allocations. You can also click on **Save to Snowflake** button
to save the current allocations and predicted ROI into
BUDGET_ALLOCATIONS_AND_ROI Snowflake table.

## 7\. Cleanup

If you started/resumed the tasks as part of the **Data Engineering** or **Data
Pipelines** sections, then it is important that you run the following commands
to suspend those tasks in order to avoid unecessary resource utilization.

_Note: Suspending the root task will suspend the full DAG._

    
    
    root_task = tasks["DE_PIPELINE_DAG"]
    root_task.suspend()

## 8\. Conclusion And Resources

Congratulations! You've successfully performed data engineering tasks and
trained a Linear Regression model to predict future ROI (Return On Investment)
of variable advertising spend budgets across multiple channels including
Search, Video, Social Media, and Email using Snowpark for Python and scikit-
learn. And then you created a Streamlit application that uses that model to
generate predictions on new budget allocations based on user input.

We would love your feedback on this QuickStart Guide! Please submit your
feedback using this [Feedback Form](https://forms.gle/XKd8rXPUNs2G1yM28).

## What You Learned

  * How to analyze data and perform data engineering tasks using Snowpark DataFrames and APIs
  * How to use open-source Python libraries from curated Snowflake Anaconda channel
  * How to create Snowflake Tasks to automate data pipelines
  * How to train ML model using Snowpark ML in Snowflake
  * How to register ML model and use it for inference from Snowflake Model Registry
  * How to create Streamlit application that uses the ML Model for inference based on user input

## Related Resources

  * [Source Code on GitHub](https://github.com/Snowflake-Labs/sfguide-getting-started-dataengineering-ml-snowpark-python)
  * [Snowpark for Python Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html)
  * [Snowpark for Python API Reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/index.html)
  * [Snowpark ML Modeling](https://docs.snowflake.com/developer-guide/snowpark-ml/modeling)
  * [Snowpark ML Model Registry](https://docs.snowflake.com/developer-guide/snowpark-ml/model-registry/overview)

Back

Next[Done](/ "Codelab complete")

![](https://www.facebook.com/tr?id=1336281856462827&ev=PageView&noscript=1)
![](https://www.facebook.com/tr?id=7343521989095756&ev=PageView&noscript=1)

![](https://bat.bing.com/action/0?ti=25015801&tm=gtm002&Ver=2&mid=6ad20b49-1f2f-42cc-8d20-48bc26c6e2cd&sid=64f07e10866b11efb403d95ef4ab0cc2&vid=64f06e50866b11efb07eb3dc17df63a6&vids=1&msclkid=N&pi=0&lg=en-
US&sw=1800&sh=1169&sc=30&nwd=1&tl=Getting%20Started%20with%20Data%20Engineering%20and%20ML%20using%20Snowpark%20for%20Python%20and%20Snowflake%20Notebooks&p=https%3A%2F%2Fquickstarts.snowflake.com%2Fguide%2Fgetting_started_with_dataengineering_ml_using_snowpark_python%2F%230&r=&lt=539&evt=pageLoad&sv=1&cdb=AQAQ&rn=941008)![](https://bat.bing.com/action/0?ti=25015801&tm=gtm002&Ver=2&mid=6ad20b49-1f2f-42cc-8d20-48bc26c6e2cd&sid=64f07e10866b11efb403d95ef4ab0cc2&vid=64f06e50866b11efb07eb3dc17df63a6&vids=0&msclkid=N&ec=quickstarts&gc=USD&tpp=1&ea=quickstarts&en=Y&p=https%3A%2F%2Fquickstarts.snowflake.com%2Fguide%2Fgetting_started_with_dataengineering_ml_using_snowpark_python%2F%230&sw=1800&sh=1169&sc=30&nwd=1&evt=custom&cdb=AQAQ&rn=92852)

![](https://acq-3pas.admatrix.jp/if/5/01/1a12ead04d19771bfe22fd90210dc8cc.fs?cb=3528127&rf=https%3A%2F%2Fquickstarts.snowflake.com%2Fguide%2Fgetting_started_with_dataengineering_ml_using_snowpark_python%2F%230&prf=&i=ySsypG7P)

![](//acq-3pas.admatrix.jp/if/6/01/1a12ead04d19771bfe22fd90210dc8cc.fs)

## Snowflake's Use of Cookies

We use cookies to enhance your experience and to analyze site traffic as
described in our Cookie Statement. By accepting, you consent to our use of
cookies.[Cookie Statement.](https://www.snowflake.com/privacy-policy/cookie-
statement/)

Cookies Settings Reject All Accept All Cookies

![Company
Logo](https://cdn.cookielaw.org/logos/cb85e692-4053-4d0a-8dda-d24b5daa8b06/ff6c124b-1473-4861-9ca3-9eaf6debb37d/SNO-
SnowflakeLogo_blue.png)

## Privacy Preference Center

Your Opt Out Preference Signal is Honored

  * ### Your Privacy

  * ### Strictly Necessary Cookies

  * ### Performance Cookies

  * ### Functional Cookies

  * ### Targeting Cookies

#### Your Privacy

When you visit any website, it may store or retrieve information on your
browser, mostly in the form of cookies. This information might be about you,
your preferences or your device and is mostly used to make the site work as
you expect it to. The information does not usually directly identify you, but
it can give you a more personalized web experience. Because we respect your
right to privacy, you can choose not to allow some types of cookies. Click on
the different category headings to find out more and change our default
settings. However, blocking some types of cookies may impact your experience
of the site and the services we are able to offer.  
[More information](https://cookiepedia.co.uk/giving-consent-to-cookies)

#### Strictly Necessary Cookies

Always Active

These cookies are necessary for the website to function and cannot be switched
off. They are usually only set in response to actions made by you which amount
to a request for services, such as setting your privacy preferences, logging
in or filling in forms. You can set your browser to block or alert you about
these cookies, but some parts of the site will not then work. These cookies do
not store any personally identifiable information.

Cookies Details‎

#### Performance Cookies

Performance Cookies

These cookies allow us to count visits and traffic sources so we can measure
and improve the performance of our site. They help us to know which pages are
the most and least popular and see how visitors move around the site.    All
information these cookies collect is aggregated and therefore anonymous. If
you do not allow these cookies we will not know when you have visited our
site, and will not be able to monitor its performance.

Cookies Details‎

#### Functional Cookies

Functional Cookies

These cookies enable the website to provide enhanced functionality and
personalisation. They may be set by us or by third party providers whose
services we have added to our pages.    If you do not allow these cookies then
some or all of these services may not function properly.

Cookies Details‎

#### Targeting Cookies

Targeting Cookies

These cookies may be set through our site by our advertising partners. They
may be used by those companies to build a profile of your interests and show
you relevant adverts on other sites. They do not store directly identifiable
personal information, but are based on uniquely identifying your browser and
internet device. If you do not allow these cookies, you will experience less
targeted advertising.

Cookies Details‎

Back Button

### Cookie List

Filter Button

Consent Leg.Interest

checkbox label label

checkbox label label

checkbox label label

Clear

checkbox label label

Apply Cancel

Confirm My Choices

Allow All

[![Powered by
Onetrust](https://cdn.cookielaw.org/logos/static/powered_by_logo.svg)](https://www.onetrust.com/products/cookie-
consent/)

