from celery.decorators import task, periodic_task
from celery.schedules import crontab
from django.conf import settings
from datetime import datetime, timedelta
from repo.models import RepoFile
import os

@periodic_task(run_every=crontab(minute="*/1", hour="*", day_of_week="*"))
def cleanup():
    """
    Performs a cleanup of expired downloads
    """
    # get list of RepoFiles to clear -- only older than 5 minutes
    deleted = []
    expires = datetime.now()-timedelta(minutes=2)
    for rf in RepoFile.objects.filter(date_created__lt=expires):
        print('Removing {0} ({1})'.format(rf.uuid, rf.filename))
        deleted.append(rf.filename)
        rf_file = os.path.join(settings.UPLOADS_DIR, rf.uuid)
        if os.path.exists(rf_file):
            os.remove(rf_file)
        # clear db entry
        rf.delete()
    if len(deleted) > 0:
        return 'Removed: {0}. Cleanup complete'.format(','.join(deleted))
    else:
        return 'Cleanup task complete'
