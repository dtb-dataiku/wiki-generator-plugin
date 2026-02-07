# This file is the actual code for the custom Python dataset wiki-generator_metadata-dataset
import dataiku

# import the base class for the custom dataset
from six.moves import xrange
from dataiku.connector import Connector

from wikigenerator import extractor

"""
A custom Python dataset is a subclass of Connector.

The parameters it expects and some flags to control its handling by DSS are
specified in the connector.json file.

Note: the name of the class itself is not relevant.
"""
class MyConnector(Connector):

    def __init__(self, config, plugin_config):
        """
        The configuration parameters set up by the user in the settings tab of the
        dataset are passed as a json object 'config' to the constructor.
        The static configuration parameters set up by the developer in the optional
        file settings.json at the root of the plugin directory are passed as a json
        object 'plugin_config' to the constructor
        """
        
        Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class

        self.project_key = self.config.get("project", None)
        
        self.COLUMNS = [
            'project_key', 'project_name',
            'dataset_name', 'dataset_project_key', 'dataset_project_name', 'dataset_columns', 'dataset_sources',
            'connection_type', 'connection_name'
        ]
        self.TYPES = ['string'] * len(self.COLUMNS)

    def get_read_schema(self):
        """
        Returns the schema that this connector generates when returning rows.

        The returned schema may be None if the schema is not known in advance.
        In that case, the dataset schema will be infered from the first rows.

        If you do provide a schema here, all columns defined in the schema
        will always be present in the output (with None value),
        even if you don't provide a value in generate_rows

        The schema must be a dict, with a single key: "columns", containing an array of
        {'name':name, 'type' : type}.

        Example:
            return {"columns" : [ {"name": "col1", "type" : "string"}, {"name" :"col2", "type" : "float"}]}

        Supported types are: string, int, bigint, float, double, date, boolean
        """

        columns_specs = [{'name': c[0], 'type': c[1]} for c in zip(self.COLUMNS, self.TYPES)]
        return {"columns": types}

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        """
        The main reading method.

        Returns a generator over the rows of the dataset (or partition)
        Each yielded row must be a dictionary, indexed by column name.

        The dataset schema and partitioning are given for information purpose.
        """
        
        client = extractor.get_dataiku_client() 
        rows = extractor.get_project_datasets_metadata(client, self.project_key)

        for row in rows:
            yield row

