import logging
from django.contrib.auth import get_user_model

from airflow_aas.celery import app
from scm import get_client_for_dvcs


@app.task
def setup_repository(user_id, repo_name, vcs='github'):
    user = get_user_model().objects.get(pk=user_id)

    client = get_client_for_dvcs(vcs)(user)

    logging.info('Ensuring SSH key for %s://%s@%s', vcs, user.username, repo_name)

    if not client.repo_has_ssh_key(repo_name):
        logging.info('Key does not exist, creating')
        client.create_and_save_keys(repo_name)
        logging.info('Registering Commit Webhook')
        client.register_webhook(repo_name)
