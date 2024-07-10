from django.contrib import admin

from main.models import Contact, Certificate, Project

class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = (
        "id",
        "name",
        "email",
        "created_date",
    )
    list_filter = ("email",)
    ordering = ["-created_date"]
    search_fields = ["name", "email"]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Certificate)
admin.site.register(Project)
