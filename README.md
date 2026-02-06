# Reddits ETL tool

A Python 3.11 application for reddits ingestion and other ETL processes. Ingestion is loading appropriate data from files directly into appropriate database tables. Other ETL processes are relying on loading the data from table, processing them and persisting processed data into other tables.

## Installation
Before downloading the repo you have to install [Anaconda](https://anaconda.org/). After installation clone the repo. Go into the downloaded repo directory.

    cd ETLReddit

Then establish new Anaconda Python 3.11 environment, like _etl_reddit_311_ with required packages:

    conda create -n etl_reddit_311 python=3.11 --file "requirements.txt"

Activate the Anaconda environment via: `conda activate etl_reddit_311`. The application is now ready to be used.

## Setting up the Supabase Postgres database
To set the Supabase Postgres database server run the folllowing steps:
1. Create `supabase_config.json` file in main project directory like.
2. Create new database project. **Important!** Remember your **username** and **password** for further steps!
3. Select **Project Overview** and then click **Connect** icon at the top toolbar.
![supabase connection settings](/assets/images/supabase_connection_settings.png)
4. The illustration above shows you the database connection string you should use to connect `[postgresql://postgres.<YOUR-USERNAME>:<YOUR-PASSWORD>@aws-1-eu-west-1.pooler.supabase.com:5432/postgres]`
5. Put inside the following content like in the illustration below:
![supabase config json file content](/assets/images/supabase_config_json.png)

where "your database username" and "your password" should refer you own Supabase credentials.
6. Voila! You've done the supabase config setup.

## Running the application
### Ingestion
Running the help command: `python run_ingestion.py -h` yields the following:
```
---- Reddits ingestion app ----

usage: run_ingestion.py [-h] [-b BATCH_SIZE] [--load_authors] phrase

Reddits ingestion Python 3.11 application.

positional arguments:
  phrase                phrase which contain reddits to do the ETL with

options:
  -h, --help            show this help message and exit
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        size of inserted batch of reddits into database, default: 10000
  --load_authors        flag whether to load reddit authors information, default: False

```

### Parameters overview
1. **phrase** -- required -- word or sentence fragment according to which the reddits should be ingested.
2. **-b**, **--batch_size** -- optional -- **10000** by default -- maximum number of entries inserted into database at once.
3. **--load_authors** -- optional -- **False** by default -- flag whether to insert authors into database. If unset the application will only insert reddits and their comments.

### Command examples
#### Simple
    python run_ingestion.py "corgi"
The application will ingest all JSON files according to "corgi" word however without ingestioning author JSON files.

#### Authors ingestion
    python run_ingestion.py "corgi" --load_authors
The application beside the "corgi" JSON files will ingest also author "corgi" JSONs.

### ETL
Running the help command: `python run_etl.py -h` yields the following:
```
---- Reddits ETL app ----

usage: run_etl.py [-h] [-b BATCH_SIZE] [--use_multiprocessing] [--num_processes NUM_PROCESSES] {sentiment_analysis,vectorization} phrase

Reddits ETL Python 3.11 application.

positional arguments:
  script                {sentiment_analysis,vectorization}
                        ETL script to run
  phrase                phrase which contain reddits to do the ETL with

options:
  -h, --help            show this help message and exit
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        size of inserted batch of reddits into database, default: 10000
  --use_multiprocessing
                        flag whether to use multiprocessing while processing entries, default: False
  --num_processes NUM_PROCESSES
                        number of processes if multiprocessing is used, default: 8

```

### Parameters overview
1. **script** -- required -- etl script to run. Currently, **"sentiment_analysis"** is only available. The _"vectorization"_ will be developed furtherly.  
2. **phrase** -- required -- word or sentence fragment according to which the reddits should be ingested.
3. **-b**, **--batch_size** -- optional -- **10000** by default -- maximum number of entries inserted into database at once.
4. **--use_multiprocessing** -- optional -- **False** by default -- flag whether to utilize multiprocess approach for results downloading. If set up the application will divide the list of reddit permalinks to download them from to separate processes. For 2xQuadCore processors the number should not be larger than 8.
5. **--num_processes** -- optional -- **8** by default -- number of processes for multiprocess approach, not applicable if _--use_multiprocessing_ flag is unset.

### Command examples
#### Simple
    python run_etl.py "corgi"
The application will load all reddits and comments according to "corgi", perform the sentiment analysis with one single process and store processed data into _sentiment_analysis_ table.

#### Multiprocessing
    python run_etl.py "corgi" --use_multiprocessing
The application will load all reddits and comments according to "corgi", perform the sentiment analysis using multi process approach and store processed data into _sentiment_analysis_ table.

### Testing
To perform application unit testing simply run the command `pytest` in main project directory. The output should look like the following:
```
================================ test session starts ================================
platform linux -- Python 3.11.14, pytest-9.0.2, pluggy-1.5.0
rootdir: /home/jakub/PycharmProjects/ETLReddit
plugins: mock-3.15.1, anyio-4.10.0
collected 14 items                                                                                                                                                                     

test/test_util.py ..............                                               [100%]

================================= 14 passed in 0.03s ================================
```

## Dataflow
![Dataflow diagram](/assets/images/reddits_dataflow_etl.png)
The illustration above shows the solution dataflow diagram. The dash-frame highlighted area denotes the reddits ETL process stages.

### Stages of reddits ETL processes
1. **JSON file contents loading** -- reading appropriate JSON files and loading the data via JSON objects.
2. **JSONs processing** -- selection of appropriate data from JSON objects so as to satisfy the _reddits_, _comments_ and _authors_ tables data storage rules.
3. **Ingestion** -- conversion of JSON objects into class objects and insertion of reddit, comment and author entries into database tables.
4. **ETL processes** -- loading data from tables into which the appropriate data have been ingested, processing them to expected data model and persisting in other tables.

## Data model
![Data model class diagram](/assets/images/reddits_data_model.png)
The illustration above shows the data model diagram class. The **Author**, **Reddit** and **Comment** class instances are used during JSON files ingestion (insertion) as well as ETL processes (reading). The **SentimentAnalysis** class instances are used (currently) only during persistence of processed reddits and comments (insertion).