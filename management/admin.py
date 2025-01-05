from django.contrib import admin
from .models import User, Project, Task, Comment, ProjectMember


# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')


# Project Member Inline for Project Admin
class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [ProjectMemberInline]


# Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'status', 'priority', 'assigned_to', 'created_at', 'due_date')
    search_fields = ('title', 'project__name', 'assigned_to__username')
    list_filter = ('status', 'priority', 'created_at', 'due_date')
    ordering = ('-created_at',)


# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user', 'task', 'created_at')
    search_fields = ('content', 'user__username', 'task__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Project Member Admin
@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'user', 'role')
    search_fields = ('project__name', 'user__username', 'role')
    list_filter = ('role', 'project')
    ordering = ('project', 'role')
