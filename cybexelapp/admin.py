from django.contrib import admin
from .models import *

admin.site.register(ContactSubmission)
admin.site.register(Department)
admin.site.register(Experience)
admin.site.register(JobVacancy)
admin.site.register(Statistic)
admin.site.register(JobApplication)
admin.site.register(Blog)
admin.site.register(ClientLogo)

class LifeEventImageInline(admin.TabularInline):
    model = LifeEventImage
    extra = 1

@admin.register(LifeEvent)
class LifeEventAdmin(admin.ModelAdmin):
    inlines = [LifeEventImageInline]
    list_display = ('heading', 'category')


admin.site.register(AdminProfile)