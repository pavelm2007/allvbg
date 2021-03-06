# -*- coding: utf-8 -*-
from allvbg.models import *
from django.contrib import admin
from feincms.admin import editor
from mptt.admin import MPTTModelAdmin #зависимость для отображения материалов в виде дерева в админке
from allvbg.widgets import *  #подключаем все свои виджеты
from django import forms #зависимость для переопределения полей формы в админке
from modeltranslation.admin import TranslationAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class FirmAdmin(editor.TreeEditor): #класс для админ-панели фирм
	list_display = ('name', 'short', 'map_style', 'isstore', 'pub_date') #список полей, выводимых в админке
	#list_filter = ['pub_date'] #поле, по которому возможна фильрация
	search_fields = ['name'] #поле, по которому возможен поиск
	#date_hierarchy = 'pub_date' #порядок сортировки по умолчанию дял дат
	#ordering = ('-pub_date',) #поле и порядок сортировки
	ordering = ('-id',) #поле и порядок сортировки
	fieldsets = [ #наборы полей
		('Основное', {'fields': ['name', 'alias', 'parent', 'container', 'short', 'description']}),
		('Изображения', {'fields': ['image1', 'image2', 'image3', 'image4']}),
		#('Карта', {'fields': ['location', 'map_style'], 'classes': ['collapse']}),
		('Карта', {'fields': ['lat', 'lng', 'location', 'map_style']}),
		('Магазин', {'fields': ['isstore', 'ecwid'], 'classes': ['collapse']}),	
		('Мета', {'fields': ['meta_key'], 'classes': ['collapse']}),		
		('Дата', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	
	class form(forms.ModelForm): #вот этот кусок кода дополняет полее ввода картинки её превьюхой
		class Meta:
			widgets = {
				'image1': AdminImageWidget, #виджет определён в allvbg/widgets.py
				'image2': AdminImageWidget,
				'image3': AdminImageWidget,
				'image4': AdminImageWidget,
				'location':LocationWidget,
			}
			ordering = ['tree_id', 'lft']

class MyTranslatedFirmAdmin(FirmAdmin, TranslationAdmin):
    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }
    pass
			
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('name', 'short', 'pub_date')
	search_fields = ['name']
	list_filter = ['pub_date']
	ordering = ('-pub_date',)	
	fieldsets = [
		('Основное', {'fields': ['name', 'short', 'description']}),
		('Мета', {'fields': ['meta_key'], 'classes': ['collapse']}),		
		('Дата', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]	
	
class OrdersLisrtAdmin(admin.ModelAdmin):
	list_display = ('date', 'summ', 'user', 'lng')
	search_fields = ['user','date']
	list_filter = ['date','user']
	ordering = ('-date',)	
	
class EventAdmin(TranslationAdmin):
	list_display = ('name', 'short', 'start_date', 'end_date')
	search_fields = ['name']
	list_filter = ['start_date', 'end_date']
	ordering = ('-start_date',)	
	fieldsets = [
		('Основное', {'fields': ['name', 'short', 'description']}),
		('Дата', {'fields': ['start_date', 'end_date']}),
	]
	class Media:
		js = (
			'/static/modeltranslation/js/force_jquery.js',
			'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
			'/static/modeltranslation/js/tabbed_translation_fields.js',
		)
		css = {
			'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
		}	
	
class MapAdmin(admin.ModelAdmin):
	list_display = ('title', 'value')
	search_fields = ['title']
	list_filter = ['title']
	ordering = ('-title',)	

admin.site.unregister(User)
 
class UserProfileInline(admin.StackedInline):
	model = UserProfile
	raw_id_fields = ("editor_for",)
 
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
 
admin.site.register(User, UserProfileAdmin)	
admin.site.register(Firm, MyTranslatedFirmAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(MapStyle, MapAdmin)
admin.site.register(OrdersLisrt, OrdersLisrtAdmin)