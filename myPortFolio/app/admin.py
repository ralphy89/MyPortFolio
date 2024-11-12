from django.contrib import admin
from .models import User, Skill, Framework, Resume, Education, Message, Experience

# Register your models here.

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Framework)
admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(Message)
admin.site.register(Experience)