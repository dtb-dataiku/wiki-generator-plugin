from wikigenerator.extractor import get_dataiku_client, list_dataset_tags, list_project_datasets

def do(payload, config, plugin_config, inputs):
    """Populate choices in the initial macro interface"""
    
    client = get_dataiku_client()
    project_key = client.get_default_project().project_key
    
    parameter_name = payload.get('parameterName')
    
    # Set project dropdown
    if parameter_name == "tags":
        available_tags = list_dataset_tags(client, project_key)
        choices = [{'value': t, 'label': t} for t in available_tags]
        return {"choices": choices}
    
    # Set dataset multiselect box
    elif parameter_name == "datasets":
        selected_tags = config.get("tags", [])
        if selected_tags:
            available_datasets = list_project_datasets(client, project_key, tag_filter=selected_tags)
        else:
            available_datasets = list_project_datasets(client, project_key)
            
        choices = [
            {'value': f'{d[0]}.{d[1]}', 'label': f"{d[1]} [{d[0]}]"}
            for d in available_datasets
        ]
        return {"choices": choices}