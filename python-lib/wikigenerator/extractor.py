import dataiku
import dataikuapi

def get_dataiku_client(host=None, api_key=None):
    '''Get a Dataiku client object.'''

    try:
        if host and api_key:
            return dataikuapi.DSSClient(host, api_key)
        else:
            return dataiku.api_client()
    except Exception as e:
        print(f'Error getting Dataiku client: {e}')
        return None
    

def list_project_datasets(client, project_key, tag_filter=None, exclude_tags=False):
    '''List datasets in a Dataiku project.'''

    try:
        project = client.get_project(project_key)
        dataset_objects = project.list_datasets(as_type='objects', include_shared=False) # NEED TO REVISIT THIS

        datasets = [d.name for d in dataset_objects]

        if not tag_filter:
            return sorted(datasets)

        if isinstance(tag_filter, str):
            target_tags = {tag_filter}
        
        if isinstance(tag_filter, list):
            target_tags = set(tag_filter)

        filtered_datasets = []
        for d in dataset_objects:
            dataset_tags = set(d.get_metadata().get('tags', []))

            # Check intersection: do they share any tags?
            has_overlap = not target_tags.isdisjoint(dataset_tags)

            if exclude_tags:
                # EXCLUDE mode: keep dataset only if there is no overlap
                if not has_overlap:
                    filtered_datasets.append(d.name)
            else:
                # INCLUDE mode: keep dataset only if there is overlap
                if has_overlap:
                    filtered_datasets.append(d.name)

        return sorted(filtered_datasets)
    except Exception as e:
        print(f'Error getting datasets in {project_key}: {e}')
        return None

def list_dataset_tags(client, project_key):
    '''List all tags associated with datasets in a Dataiku project.'''

    try:
        project = client.get_project(project_key)
        dataset_objects = project.list_datasets(as_type='objects', include_shared=True)

        datasets = [d.name for d in dataset_objects]

        tags = []
        for d in dataset_objects:
            tags.extend(d.get_metadata().get('tags', []))

        tags = sorted(list(filter(lambda t: t, set(tags))))

        return tags
    except Exception as e:
        print(f'Error getting dataset tags in {project_key}: {e}')
        return None

def get_dataset_metadata(client, project_key, dataset_name):
    '''Get dataset information.'''

    metadata = {
        'name': dataset_name,
        'project_key': project_key,
        'project_name': None,
        'type': None,
        'connection': None,
        'short_description': None,
        'long_description': None,
        'columns': []
    }

    try:
        project = client.get_project(project_key)
        dataset = project.get_dataset(dataset_name)
        dataset_info = dataset.get_info().info['dataset']

        metadata['name'] = dataset_info['name']
        metadata['project_key'] = dataset_info['projectKey']
        metadata['project_name'] = project.get_metadata()['label']
        metadata['type'] = dataset_info['type']
        metadata['connection'] = dataset_info['params']['connection']
        metadata['short_description'] = dataset_info.get('shortDesc', 'No description provided.').strip()
        metadata['long_description'] = dataset_info.get('description', 'No description provided.').strip()
        metadata['columns'] = [{'name': c['name'], 'type': c['type'],  'description': c.get('comment', '')} for c in dataset_info['schema']['columns']]

        return metadata
    except Exception as e:
        print(f'Error getting metadata for {dataset_name}: {e}')
        return None