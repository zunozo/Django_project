from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance,Language
# Register your models here.

#admin.site.register(Author)
class AuthorInline(admin.TabularInline):
    model = Book
    extra = 0
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth','date_of_death')]
    inlines = [AuthorInline]
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'display_genre', 'language')
    inlines = [BookInstanceInline]
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book','status','borrower','due_back','id') 
    fieldsets=(
        (None, {
            'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields':('status','due_back','borrower')
        }),
    )

admin.site.register(Language)

