from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, 
    TaskViewSet, 
    CommentViewSet, 
    RegisterView, 
    LoginView, 
    UserProfileViewSet
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')

user_profile_view = UserProfileViewSet.as_view({
    'get': 'retrieve',  # Retrieve authenticated user data
    'put': 'update',    # Update authenticated user data
    'delete': 'destroy' # Delete authenticated user account
})

# i create this because i want seprate user creation and it's conflicting with permission i choose this 


urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:id>/tasks/', TaskViewSet.as_view({'get': 'project_tasks', 'post': 'project_tasks'}), name='project-tasks'),
    path('tasks/<int:id>/comments/', CommentViewSet.as_view({'get': 'task_comments', 'post': 'task_comments'}), name='task-comments'),
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/', user_profile_view, name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
