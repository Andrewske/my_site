from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import SpotifyUser, SpotifyTasks
from . import repeat

class TaskAdmin(admin.ModelAdmin):
    fields = ['task_id', 'task_name', 'next_run_time']
    list_display = ['task_id', 'task_name', 'next_run_time']
    change_list_template = 'admin/music_minion/spotifytasks/spotify_tasks_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('start/<str:task>/', self.start_task),
            path('end/<str:task>/', self.stop_task)
        ]
        return custom_urls + urls
    
    def start_task(self, request, task):
        if task == 'dw_task':
            message = repeat.start_task(task)
            self.message_user(request, message)
        return HttpResponseRedirect("/admin/music_minion/spotifytasks/")

    def stop_task(self, request, task):
        if task == 'dw_task':
            message = repeat.stop_task('dw_task')
            self.message_user(request, message)
        return HttpResponseRedirect("/admin/music_minion/spotifytasks/")

    

# Register your models here.
admin.site.register(SpotifyUser)
admin.site.register(SpotifyTasks, TaskAdmin)