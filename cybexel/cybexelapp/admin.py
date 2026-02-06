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

class LifeEventMediaInline(admin.TabularInline):
    model = LifeEventMedia
    extra = 1
    fields = ('file', 'media_type', 'order')
    ordering = ('order',)


@admin.register(LifeEvent)
class LifeEventAdmin(admin.ModelAdmin):
    inlines = [LifeEventMediaInline]
    list_display = ('heading', 'category')


admin.site.register(AdminProfile)
admin.site.register(PortfolioCategory)
admin.site.register(PortfolioDetail)
admin.site.register(PortfolioPoint)
admin.site.register(PortfolioWork)
admin.site.register(PortfolioProcessStep)
admin.site.register(Testimonial)