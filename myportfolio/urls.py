
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('tasks/', include('task_manager.urls')),
    path('network/', include('network.urls')),

]
