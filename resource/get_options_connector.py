from wikigenerator.extractor import get_dataiku_client, list_project_datasets

def do(payload, config, plugin_config, inputs):
    """Populate choices in the initial macro interface"""
    
    parameter_name = payload.get('parameterName')

    client = get_dataiku_client()