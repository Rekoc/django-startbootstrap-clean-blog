from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django_startbootstrap_clean_blog.models import Post, Category, Subcategory, Author
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .form import ContactForm
from django import forms
from .models import GENDER_CHOICES

# https://pypi.python.org/pypi/Unidecode
# from unidecode import unidecode

# def slug(value):
#     return slugify(unidecode(value))
# register.filter('slug', slug)


def clean(self):
    # Set forbidden string in subject and message fields
    forbidden_string = ["I don't like France", "France"]
    cleaned_data = super(ContactForm, self).clean()
    subject = cleaned_data.get('subject')
    message = cleaned_data.get('message')

    if subject and message:
        if subject in forbidden_string and message in forbidden_string:
            raise forms.ValidationError(
                "Stop talking about France !"
            )
    return cleaned_data


class Index(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = "index.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        posts = Post.objects.all()
        page = self.request.GET.get('page')
        paginator = Paginator(posts, self.paginate_by)

        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(Paginator.num_pages)

        context['post_list'] = post_list
        context['list_category'] = Category.objects.all()
        return context


def Contact(request):
    try:
        list_category = Category.objects.all()
    except Category.DoesNotExist:
        pass

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['rekoc13@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return redirect('success')
            envoi = True
    return render(request, 'contact.html', locals())


def successView(request):
    return HttpResponse('Success! Thank you for your message.')


def About(request):
    try:
        list_category = Category.objects.all()
    except Category.DoesNotExist:
        pass
    return render(request, 'about.html', locals())


def ViewPost(request, category_slug, post_slug):
    try:
        post = Post.objects.get(slug=post_slug)
        list_category = Category.objects.all()
    except Post.DoesNotExist:
        raise Http404
    except Category.DoesNotExist:
        pass
    if post.has_header:
        return render(request, 'post.html', locals())
    else:
        return render(request, 'post_no_header.html', locals())


def ViewCategory(request, category_slug):
    try:
        cat = Category.objects.get(slug=category_slug)
        posts = Post.objects.all().filter(category__id=cat.id).order_by('-publish_date')
        list_category = Category.objects.all()

        paginator = Paginator(posts, 1)
        page = request.GET.get('page')
        list_post = paginator.get_page(page)
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'category.html', locals())


def Portfolio(request):
    try:
        categories = Category.objects.all()
        list_category = categories
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'portfolio.html', locals())

