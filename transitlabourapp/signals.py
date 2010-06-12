from registration.signals import user_activated
from django.contrib.auth.models import Permission

def perms_on_activation(sender, user, request, **kwargs):
	#login to admin site
	user.is_staff = True

	#blogs
	user.user_permissions.add(Permission.objects.get(codename='add_blog'))
	user.user_permissions.add(Permission.objects.get(codename='change_blog'))
	user.user_permissions.add(Permission.objects.get(codename='delete_blog'))
	#events
	user.user_permissions.add(Permission.objects.get(codename='add_event'))
	user.user_permissions.add(Permission.objects.get(codename='change_event'))
	user.user_permissions.add(Permission.objects.get(codename='delete_event'))
	#user profile
	user.user_permissions.add(Permission.objects.get(codename='add_userprofile'))
	user.user_permissions.add(Permission.objects.get(codename='change_userprofile'))
	user.user_permissions.add(Permission.objects.get(codename='delete_userprofile'))
	
	user.save()

user_activated.connect(perms_on_activation)

