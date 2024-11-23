from django.contrib import admin
from netflixapp.models import CustomUser , Profile , Movie , Video


# Register the CustomUser model to make it accessible in the admin interface
admin.site.register(CustomUser)

# Register the Profile model to allow management of user profiles in the admin
admin.site.register(Profile)

# Register the Movie model to enable movie management through the admin interface
admin.site.register(Movie)

# Register the Video model to allow video file management in the admin
admin.site.register(Video)

# Register your models here.
