from rest_framework import serializers
from .models import User, Project, ProjectMember, Task, Comment
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password' ,'date_joined']
        
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # If date_joined is not provided, use the current time
        validated_data['date_joined'] = validated_data.get('date_joined', now())
        
        # Create the user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        user.date_joined = validated_data['date_joined']
        user.save()
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
    )
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at']

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])

        # Create the project with the remaining data
        project = Project.objects.create(**validated_data)

        for member_data in members_data:
            try:
                user = User.objects.get(id=member_data['user_id'])
                ProjectMember.objects.create(project=project, user=user, role=member_data['role'])
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with ID {member_data['user_id']} does not exist.")

        return project

    def update(self, instance, validated_data):
    
        members_data = validated_data.pop('members', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update members
        if members_data:
            # Clear existing members
            instance.members.all().delete()
            for member_data in members_data:
                try:
                    user = User.objects.get(id=member_data['user_id'])
                    ProjectMember.objects.create(project=instance, user=user, role=member_data['role'])
                except User.DoesNotExist:
                    raise serializers.ValidationError(f"User with ID {member_data['user_id']} does not exist.")

        return instance

    def validate_members(self, members):

        if not isinstance(members, list):
            raise serializers.ValidationError("Members should be a list of user-role dictionaries.")

        for member in members:
            if not isinstance(member, dict):
                raise serializers.ValidationError("Each member should be a dictionary.")

            if 'user_id' not in member or 'role' not in member:
                raise serializers.ValidationError("Each member must have 'user_id' and 'role'.")

        return members
 

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']

class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
