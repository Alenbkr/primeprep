from django.contrib import admin
from .models import Dish, Ration, RationDish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories_per_100g', 'protein_per_100g', 'fat_per_100g', 'carbs_per_100g')
    search_fields = ('name',)


class RationDishInline(admin.TabularInline):
    model = RationDish
    extra = 2
    fields = ('day_number', 'dish', 'weight')


@admin.register(Ration)
class RationAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories_tag', 'price', 'is_active')
    list_filter = ('calories_tag', 'is_active')
    inlines = [RationDishInline]