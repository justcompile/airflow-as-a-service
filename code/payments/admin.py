from django.contrib import admin

from .models import Product, Plan


class PlanInline(admin.StackedInline):
    model = Plan
    extra = 1
    exclude = ('stripe_id', )


class ProductAdmin(admin.ModelAdmin):
    fields = ['name',]
    inlines = [PlanInline]

admin.site.register(Product, ProductAdmin)
