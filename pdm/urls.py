from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('docs/<doc_id>/', views.docView, name='docView'),
    # path('login/', views.loginPage, name='login'),
    # path('logout/', views.logoutPage, name='logout'),

    path('accounts/', include('django.contrib.auth.urls')),
]
