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
    path('request/delete/<req_id>', views.deleteRequest, name='delete-request'),
    path('request/<req_id>/<action>', views.approveOrDeny, name='approve-or-deny'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name='register'),
]
