import pandas as pd
from data_ingestion import create_db_engine, query_data, read_from_web_CSV
import logging


class FieldDataProcessor:
    """
    Field Data Processor class

    used to apply all needed processes on Field Data
    * ingest_sql_data.
    * rename_columns.
    * apply_corrections.
    * weather_station_mapping.
    """

    def __init__(
        self, config_params, logging_level="INFO"
    ):  # When we instantiate this class, we can optionally specify what logs we want to see
        # Initialising class with attributes we need. Refer to the code above to understand how each attribute relates to the code
        self.db_path = config_params["db_path"]
        self.sql_query = config_params["sql_query"]
        self.columns_to_rename = config_params["columns_to_rename"]
        self.values_to_rename = config_params["values_to_rename"]
        self.weather_map_data = config_params["weather_mapping_csv"]

        self.initialize_logging(logging_level)

        # We create empty objects to store the DataFrame and engine in
        self.df = None
        self.engine = None

    # This method enables logging in the class.
    def initialize_logging(self, logging_level):
        """
        Sets up logging for this instance of FieldDataProcessor.
        """
        logger_name = __name__ + ".FieldDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = (
            False  # Prevents log messages from being propagated to the root logger
        )

        # Set logging level
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":  # Option to disable logging
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO  # Default to INFO

        self.logger.setLevel(log_level)

        # Only add handler if not already added to avoid duplicate messages
        if not self.logger.handlers:
            ch = logging.StreamHandler()  # Create console handler
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        # Use self.logger.info(), self.logger.debug(), etc.

    # let's focus only on this part from now on
    def ingest_sql_data(self):
        """Gets access to the SQL data and save it a DataFrame.

        Returns:
            * DataFrame: SQL output saved into a DataFrame.
        """
        self.engine = create_db_engine(self.db_path)
        self.df = query_data(self.engine, self.sql_query)
        self.logger.info("Sucessfully loaded data.")
        return self.df

    def rename_columns(self):
        """Rename specific columns."""
        # Extract the columns to rename from the configuration
        column1, column2 = (
            list(self.columns_to_rename.keys())[0],
            list(self.columns_to_rename.values())[0],
        )

        # Temporarily rename one of the columns to avoid a naming conflict
        temp_name = "__temp_name_for_swap__"
        while temp_name in self.df.columns:
            temp_name += "_"

        # Perform the swap
        self.df = self.df.rename(columns={column1: temp_name, column2: column1})
        self.df = self.df.rename(columns={temp_name: column2})

        self.logger.info(f"Swapped columns: {column1} with {column2}")

    def apply_corrections(self, column_name="Crop_type", abs_column="Elevation"):
        """Apply some column corrections

        Args:
            column_name (str, optional): column name. Defaults to 'Crop_type'.
            abs_column (str, optional): column name. Defaults to 'Elevation'.
        """
        self.df[abs_column] = self.df[abs_column].abs()
        self.df[column_name] = self.df[column_name].apply(
            lambda crop: self.values_to_rename.get(crop, crop)
        )
        self.df[column_name] = self.df[column_name].str.strip()

    def weather_station_mapping(self):
        """Merging the weather data to the main DataFrame."""
        # Merge the weather station data to the main DataFrame
        weather_data = read_from_web_CSV(self.weather_map_data)
        self.df = self.df.merge(weather_data, on="Field_ID", how="left")
        self.df = self.df.drop(columns="Unnamed: 0")

    def process(self):
        """Runs all process."""
        # This process calls the correct methods, and applies the changes, step by step. THis is the method we will call, and it will call the other methods in order.
        self.ingest_sql_data()
        self.rename_columns()
        self.apply_corrections()
        self.weather_station_mapping()

