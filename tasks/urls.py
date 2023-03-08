from django.urls import path

from tasks.views import create, get, update



urlpatterns = [

    path('create_demo_classification_task/', create.CreateDemoClassificationTaskView.as_view()),
    path('get_demo_classification_task/<str:task_uid>', get.GetDemoClassificationTaskView.as_view()),

    path('create_forest_change_task/', create.CreateForestChangeTaskView.as_view()),
    path('get_forest_change_task_params/', get.GetForestChangeTaskParamsView.as_view()),

    path('update_forest_change_task/', update.UpdateForestChangeTaskResultsView.as_view()),
    path('update_task_status/', update.UpdateTaskStatusView.as_view()),

]
