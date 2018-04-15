from django.contrib import admin
from .models import Post, Category, Author, Subcategory


class PostAdmin(admin.ModelAdmin):
    list_display   = ('titre', 'category', 'auteur', 'date')
    list_filter    = ('auteur', 'category', )
    date_hierarchy = 'date'
    ordering       = ('date', )
    search_fields  = ('titre', 'content')
    prepopulated_fields = {"slug": ("title",)}

    # Edition form management
    fieldsets = (
       ('General', {
            'classes': ['collapse', ],
            'fields': ('title', 'author', 'category', 'header_img', 'views', 'publish_date', 'last_modif_date')
        }),
        # Fieldset 2: post content
        ('Post content', {
           'fields': ('content', )
        }),
    )


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("lastname" "firstname",)}
    # Should use
    # prepopulated_fields = {'slug': (unidecode("lastname", "firstname"),)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    # Should use
    # prepopulated_fields = {'slug': (unidecode('name'),)}


class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    # Should use
    # prepopulated_fields = {'slug': (unidecode('name'),)}


# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Subcategory)

