# This file is the actual code for the Python runnable datasets-wiki-generator
from dataiku.runnables import Runnable
from wikigenerator import extractor, formatter, publisher

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        
        # Get macro parameters
        select_all = self.config.get("select_all", True)
        use_filter = self.config.get("use_filter", False)
        exclude = self.config.get("exclude", False)
        tags = self.config.get("tags", [])
        datasets = self.config.get("datasets", [])
        
        # Get client and project
        client = extractor.get_dataiku_client()
        project_key = client.get_default_project().project_key
        
        # Generate wiki for datasets
        if not datasets or select_all:
            if use_filter:
                selected_datasets = list_project_datasets(client, project_key, tag_filter=tags)
            else:
                selected_datasets = list_project_datasets(client, project_key)
        else:
            selected_datasets = [d for d in datasets]
            
        for ds_name in datasets:
            ds_metadata = extractor.get_dataset_metadata(client, project_key, ds_name)
            ds_content = formatter.dataset_to_markdown(ds_metadata)
            publisher.publish_to_dataiku_wiki(client, project_key, ds_name, ds_content)