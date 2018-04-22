from django.db import models
import uuid

# Create your models here.
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify

GENDER_CHOICES = [(0, "Keep secret"), (1, "Women"), (2, "Men"), (3, "Transgender")]
IDENTITY_CHOOSE_CHOICES = [(True, "Print Firstname"), (False, "Print pseudo")]


class Post(models.Model):
    title = models.CharField(max_length=200, default="")
    subtitle = models.CharField(max_length=200, default="", null=True)
    author = models.ForeignKey('Author', on_delete='Mr-X')
    views = models.IntegerField(default=0, blank=True, editable=False)

    # Can be use for personal notes - won't be seen in the post except by admin
    notes = models.CharField(max_length=200, null=True)
    publish_date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                        verbose_name="Publish date")
    last_modif_date = models.DateTimeField(auto_now_add=False, auto_now=True,
                                           verbose_name="Last modification date")

    has_header = models.BooleanField(default=False)
    if has_header:
        header_img = models.ImageField(upload_to="post_img", blank=True)

    category = models.ForeignKey('Category', on_delete='Others')

    content = RichTextUploadingField()

    slug = models.SlugField(unique=True, max_length=25, editable=False)
    is_published = models.BooleanField(default=True, help_text="Stick and the article will be publish online")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=200, null=True)

    slug = models.SlugField(unique=True, max_length=25, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30, unique=True)
    # name = str(firstname) + str(lastname)
    pseudo = models.CharField(max_length=30, null=True)

    # True = name will be print // False = pseudo will be print
    identify_choose = models.NullBooleanField(default=True, choices=IDENTITY_CHOOSE_CHOICES)
    email = models.EmailField()
    picture = models.ImageField(upload_to="picture_admin/", blank=True,
                                default="picture_admin/default_icon.png")

    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)

    slug = models.SlugField(unique=True, max_length=60, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.lastname) + '-' + slugify(self.firstname)
        super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.firstname


class Subcategory(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True)
    father_category = models.ForeignKey('Category', on_delete='Others')

    slug = models.SlugField(unique=True, max_length=25, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
