from django.contrib import admin
from  .models import Project
from django.contrib.auth.models import User

admin.site.site_header="Team Firecode"
admin.site.site_title="TF"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

