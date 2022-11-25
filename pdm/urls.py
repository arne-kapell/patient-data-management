from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('download/<doc_id>', views.download, name='download'),

    path('accounts/', include('django.contrib.auth.urls'))
]
