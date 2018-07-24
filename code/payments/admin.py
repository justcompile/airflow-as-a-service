from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Plan, Feature, PlanFeature

class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 0

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    model = Plan
    exclude = ('stripe_id', )
    inlines = [PlanFeatureInline]


class PlanInline(admin.StackedInline):
    model = Plan
    extra = 1
    exclude = ('stripe_id', )
    readonly_fields = ['edit_link']

    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name',]
    inlines = [PlanInline]

admin.site.register(Feature)
