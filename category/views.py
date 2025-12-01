from django.shortcuts import render
from book.models import Books
from category.models import Category
from django.shortcuts import get_object_or_404

# Create your views here.
# def get_category(request, id):
#
#     books =  Books.objects.filter(category_id=id)
#     context = {
#         'books':books,
#     }
#
#     return render(request,'category.html',context)
def get_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books =  Books.objects.filter(category=category)
    context = {
        'books':books,
    }

    return render(request,'category.html',context)
