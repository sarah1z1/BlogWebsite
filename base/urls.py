from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    
    path('post/create/', views.createPost, name="create-post"),
    path('post/<int:pk>', views.viewPost, name="view-post"),
    path('post/<int:pk>/update/', views.updatePost, name='update-post'),
    path('post/<int:pk>/delete/', views.deletePost, name='delete-post'),
    
    path('post/<int:pk>/comment/<int:commentId>/delete/', views.deleteComment, name="delete-comment"),
    
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.updateProfile, name="update-profile"),
    path('profile/delete/', views.deleteProfile, name='delete-profile'),
    
    path('change_password/', views.changePassword, name='change-password'),
    path('delete_account/', views.deleteAccount, name='delete-account'),
    
    path('user_profile/<int:pk>/', views.userProfile, name='user-profile'),

]
