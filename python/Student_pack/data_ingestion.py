"""Data Ingestion

This script helps in retrieving the data from database and online .csv files.

This script requires multiple packages to be installed within the Python environment you are running this script in.

  * `SQLAlchemy` - conncecting to the database.
  * `pandas`     - handling DataFrames.
  * `logging`    - status logger for debugging issues.
"""

from sqlalchemy import create_engine, text
import logging
import pandas as pd
# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('data_ingestion')
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_db_engine(db_path):
    """Creates a database engine.

    Args:
        * db_path (str): url path for the database to be connected with.

    Raises:
        * e: ImportError
        * e: Exception

    Returns:
        * Engine: database engine.
    """
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well
    except ImportError: #If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e
    
def query_data(engine, sql_query):
    """Retrieves sql query output from the database.

    Args:
        * engine (Engine): database engine.
        * sql_query (str): SQL query.

    Raises:
        * ValueError: empty query.
        * e: failed query.
        * e: error while querying the database.

    Returns:
        * DataFrame: the SQL query output in a DataFrame.
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e
    
def read_from_web_CSV(URL):
    """Reads data from the .csv files.

    Args:
        * URL (str): url for .csv file.

    Raises:
        * e: URL errors.
        * e: failed reading the .csv file.

    Returns:
        * DataFrame: DataFrame of the retrieved data.
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e