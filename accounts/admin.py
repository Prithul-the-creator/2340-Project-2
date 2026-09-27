from django.contrib import admin, messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

recruiter_name = 'Recruiter'

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username','email','first_name','last_name']
    ordering = ['username']
    actions = ['add_recruiter', 'take_away_recruiter', 'deactivate', 'reactivate']
    list_filter = ['groups', 'is_active', 'is_staff', 'is_superuser']


    @admin.action(description='Suspend selected users')
    def deactivate(self, request, users):
        if users.filter(pk=request.user.pk).exists():
            self.message_user(request, 'You cannot suspend your own account.', messages.WARNING)
        count = users.exclude(pk=request.user.pk).update(is_active=False)
        self.message_user(request, f'{count} user(s) suspended.')

    @admin.display(description='Roles')
    def user_role(self, u):
        role_list = []
        for g in u.groups.all():
            role_list.append(g.name)
        if u.is_staff: role_list.append('Admin')
        return ', '.join(role_list) or 'Job Seeker'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('groups')

    @admin.action(description='Give selected users the Recruiter role')
    def add_recruiter(self, request, users):
        grp, created = Group.objects.get_or_create(name=recruiter_name)
        grp.user_set.add(*users)
        self.message_user(request, f'{users.count()} user(s) are now recruiters.')
    @admin.action(description='Restore selected users')
    def reactivate(self, request, users):
        count = users.update(is_active=True)
        self.message_user(request, f'{count} user(s) restored.')

    @admin.action(description='Remove the Recruiter role from selected users')
    def take_away_recruiter(self, request, users):
        grp, created = Group.objects.get_or_create(name=recruiter_name)
        grp.user_set.remove(*users)
        self.message_user(request,
            f'{users.count()} user(s) are no longer recruiters.')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
