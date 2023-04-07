from django.urls import path

from tasks.views import create, get, update



urlpatterns = [

    path('create_demo_classification_task/', create.CreateDemoClassificationTaskView.as_view()),

    path('get_demo_classification_task/<str:task_id>', get.GetDemoClassificationTaskView.as_view()),

    path('update_demo_classification_task/', update.UpdateDemoClassificationTaskView.as_view()),
    path('update_task_status/', update.UpdateTaskStatusView.as_view()),

]
