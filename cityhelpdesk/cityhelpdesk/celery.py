from __future__ import absolute_import
import os
from celery import Celery
from celery.utils.log import get_task_logger
from utility.annoying import get_str, fetch_env

if os.environ.get("DJANGO_SETTINGS_MODULE", None) is None:
    # Configure environment
    env_file = get_str("ENV_FILE", os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../.env")))
    env = fetch_env(env_file)
    os.environ.update(env)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cityhelpdesk.settings")


from django.conf import settings

app = Celery("cityhelpdesk")
# logger = get_task_logger("celery.task")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    # logger.info("Ending tasks")
