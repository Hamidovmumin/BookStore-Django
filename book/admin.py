from django.contrib import admin
from . models import Books,Writer,Post,Comment

# Register your models here.
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'slug', 'price', 'stock', 'category', 'is_available',)
    prepopulated_fields = {'slug': ('book_name',)}

@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('writer_name','slug',)
    prepopulated_fields = {'slug': ('writer_name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user','comment',)
