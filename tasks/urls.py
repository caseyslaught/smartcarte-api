from django.urls import path

from tasks.views import create, get



urlpatterns = [

    path('create_forest_change_task/', create.CreateForestChangeTaskView.as_view()),
    path('get_forest_change_task_params', get.GetForestChangeTaskParamsView.as_view())

]
