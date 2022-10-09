from django.urls import path

from account.views import account, tokens


urlpatterns = [

    path('login/', tokens.LoginView.as_view()),
    path('logout/', tokens.LogoutView.as_view()),
    path('refresh/', tokens.RefreshView.as_view()),
    path('register/', account.RegisterView.as_view()),

]