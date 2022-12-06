from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('docs/', views.docs, name='docs'),
    path('upload/', views.upload, name='upload'),
    path('preview/<doc_id>', views.preview, name='preview'),
    path('download/<doc_id>', views.download, name='download'),
    path('delete/<doc_id>', views.deleteDoc, name='delete'),
    path('update/<doc_id>', views.updateDoc, name='update'),
    path('request/', views.requestAccess, name='request-access'),
    path('request/delete/<req_id>', views.deleteRequest, name='delete-request'),
    path('request/<req_id>/<action>', views.approveOrDeny, name='approve-or-deny'),
    path('verify/', views.requestVerify, name='request-verify'),
    path('verify/<req_id>/<action>', views.approveOrDenyVerify,
         name='approve-or-deny-verify'),

    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name='register'),
    path('profile/', views.profilePage, name='profile'),
    path('profile/edit/', views.editProfile, name='edit-profile'),
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/logout/', views.logoutUser, name='logout'),
    path('accounts/verify/<uidb64>/<token>', views.verifyUser, name='verify'),
]
