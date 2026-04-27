from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('news/', include('apps.news.urls.v1', namespace='news')),
    path('shared/', include('apps.shared.urls.v1', namespace='shared')),
]
