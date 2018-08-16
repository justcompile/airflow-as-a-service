def get_client_for_dvcs(name):
    from .git import GitClient

    if name in ['git', 'github']:
        return GitClient
    raise ValueError(f'{name} is not a supported DVCS')
