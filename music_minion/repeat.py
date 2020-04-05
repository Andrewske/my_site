from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from django_apscheduler.models import DjangoJobExecution
  
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


from . import spotify
from .models import SpotifyUser, SpotifyTasks

repeat_tasks = spotify.SpotifyRepeatTasks()
DjangoJobExecution.objects.delete_old_job_executions(604_800)

def start_task(task_id):
    try:
        scheduler.add_job(repeat_tasks.dw_repeat_task, 'interval', minutes=60, id=task_id, replace_existing=True)
        register_events(scheduler)
        scheduler.start()
    except:
       return "Couldn't Create Job"
    try:
        job = DjangoJobStore().lookup_job('dw_task')
        task = SpotifyTasks(task_id=job.id,task_name=job.name, next_run_time=job.next_run_time)
        task.save()
       
        scheduler.print_jobs()
        return "DW Task Created"
    except:
       return "Couldn't Save Job"


def stop_task(task_id):
    try:
        scheduler.remove_job(task_id)
        SpotifyTasks.objects.filter(task_id=task_id).delete()
        register_events(scheduler)
        scheduler.print_jobs()
        return "Job Deleted"
    except Exception as e:
        return str(e)

    
def show():
    return scheduler.get_jobs()