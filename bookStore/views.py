from django.shortcuts import render
from navbar.models import navbar
from book.models import Books,Writer
from django.shortcuts import get_object_or_404

def index(request):
    n = navbar.objects.all()
    books = Books.objects.all()
    context = {
        'n': n,
        'books': books,
    }
    return render(request, 'index.html', context)


