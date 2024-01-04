from django.urls import path
from . import views

app_name = 'task_manager'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add-task/', views.add_task, name='add_task'),
    path('completed-tasks/', views.completed_tasks, name='completed_tasks'),
    path('deleted-tasks/', views.deleted_tasks, name='deleted_tasks'),
    path('update_task/', views.update_task, name='update_task'),
    path('deleting_task/', views.deleting_task, name='deleting_task'),
    path('restore_task/', views.restore_task, name='restore_task'),
    path('update_importance/', views.update_importance, name='update_importance'),
]