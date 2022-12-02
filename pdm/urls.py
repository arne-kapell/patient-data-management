from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('upload/', views.upload, name='upload'),
    path('preview/<doc_id>', views.preview, name='preview'),
    path('download/<doc_id>', views.download, name='download'),
    path('delete/<doc_id>', views.deleteDoc, name='delete'),
    path('request/', views.requestAccess, name='request-access'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name='register'),
]
