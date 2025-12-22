def _get_or_create_parent_article(wiki, article_name='Data Dictionary'):
    '''Get or create a parent article in a wiki.'''

    articles = wiki.list_articles()

    # Search for existing parent article
    for article in articles:
        name = article.get_data().article_data['article']['name']
        if name == article_name:
            return article.article_id

    # Create parent article if missing
    content = '\n'.join([
        "# List of Datasets",
        "*Automated documentation for project datasets.*"
    ])
    article = wiki.create_article(article_name, content=content)

    return article.article_id

def _find_article_id_by_name(wiki, article_name):
    '''Find article ID by article name.'''
    for article in wiki.list_articles():
        name = article.get_data().article_data['article']['name']
        if name == article_name:
            return article.article_id
    return None

def publish_to_dataiku_wiki(client, project_key, article_title, markdown_content):
    '''Publish article to a Dataiku project wiki.'''

    try:
        project = client.get_project(project_key)
        wiki = project.get_wiki()

        parent_id = _get_or_create_parent_article(wiki)
        article_id = _find_article_id_by_name(wiki, article_title)

        if article_id:
            print(f'Delete existing article: {article_title}')
            article = wiki.get_article(article_id)
            article.delete()

        print(f'Create new article: {article_title}')
        article = wiki.create_article(
            article_title,
            parent_id=parent_id,
            content=markdown_content
        )
    except Exception as e:
        print(f'Error publishing {article_title} in {project_key}: {e}')