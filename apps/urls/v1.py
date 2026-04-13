from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('shared/', include('apps.shared.urls.v1', namespace='shared')),
    path('media-test/', include('apps.media_test.urls.v1', namespace='media_test')),
]
