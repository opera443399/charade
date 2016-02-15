# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-15
# @ pc
###################################

from django.contrib import admin

from .models import Vocabulary, GameTemporaryTable, GameScoreBoard

# Register your models here.

class VocabularyAdmin(admin.ModelAdmin):
    date_hierarchy = 'dt'
    list_display = ('id', 'en', 'zh', 'exp', 'dt', 'was_added_recently')
    list_filter = ['dt']
    search_fields = ['en']
    fieldsets = [
        (None, {'fields': ['en']}),
        ('Explanation', {'fields':['zh', 'exp']}),
    ]


class GameTemporaryTableInline(admin.TabularInline):
    model = GameTemporaryTable
    extra = 0

class GameScoreBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'scores', 'dt_start', 'dt_end')
    fieldsets = [
        ('Summary',               {'fields': ['amount', 'scores']}),
    ]
    inlines = [GameTemporaryTableInline]


admin.site.register(Vocabulary, VocabularyAdmin)
admin.site.register(GameScoreBoard, GameScoreBoardAdmin)
