from wikigenerator.extractor import get_dataiku_client, list_project_datasets

def do(payload, config, plugin_config, inputs):
    """Populate choices in the initial macro interface"""
    
    parameter_name = payload.get('parameterName')
    project_key = config.get("project", None)

    client = get_dataiku_client()
    
    # Set dataset multiselect box
    if parameter_name == "datasets":
        if project_key:
            available_datasets = list_project_datasets(client, project_key)
            
        choices = [
            {'value': f'{d[0]}.{d[1]}', 'label': f"{d[1]} [{d[0]}]"}
            for d in available_datasets
        ]
        return {"choices": choices}