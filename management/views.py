from rest_framework import viewsets, status

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Project, Task, Comment
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    TaskSerializer,
    CommentSerializer,
)

# Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Public access

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]  # Public access

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user_id": user.id,
                },
                status=status.HTTP_200_OK,
            )
        elif not user:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Incorrect password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Authenticated User ViewSet
class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Authentication required

    def retrieve(self, request):
        """Return the authenticated user's data."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        """Allow the authenticated user to update their data."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        request.user.delete()
        return Response(
            {"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request , format = None):
        projects = Project.objects.all()
        return Response(projects.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # Automatically sets the owner as the logged-in user while creating a project.
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # Check if it's a partial update (PATCH)
        instance = self.get_object()

        # Use the serializer for partial or full updates 
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True) # Validate the data
        self.perform_update(serializer)  # Save the updates

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request , *args , **kwargs ) :
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Project deleted successfully."}, status=status.HTTP_204_NO_CONTENT )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post'], url_path='projects/(?P<project_id>[^/.]+)/tasks', url_name='project-tasks')
    def project_tasks(self, request, id=None):
        """Handle listing and creation of tasks for a specific project."""
        project = Project.objects.get(id=id)
        if request.method == 'POST':
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(project=project)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Task deleted successfully!'}, status=status.HTTP_200_OK)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get', 'post'], url_path='comments', url_name='task-comments')
    def task_comments(self, request, id=None):

        task = get_object_or_404(Task, id=id)

        if request.method == 'POST':
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(task=task, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # List all comments for the task
        comments = Comment.objects.filter(task=task)
        if not comments.exists():
            return Response({"message": "No comments available for this task."}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Comment deleted successfully!'}, status=status.HTTP_200_OK)
