from wikigenerator.extractor import get_dataiku_client, list_dataset_tags, list_project_datasets

def do(payload, config, plugin_config, inputs):
    """Populate choices in the initial macro interface"""
    
    client = get_dataiku_client()
    project_key = client.get_default_project().project_key
    
    parameter_name = payload.get('parameterName')
    
    # Set project dropdown
    if parameter_name == "tags":
        return {"choices": append_dropdown_choices(projects, 'projectKey')}
    
    # Set dataset multiselect box
    elif parameter_name == "datasets":
        return {"choices": append_dropdown_choices(datasets, 'name')}