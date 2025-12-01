from django.shortcuts import render,redirect
from .forms import CommentForm
from book.models import Books,Writer,Comment
from django.shortcuts import get_object_or_404
from accounts.models import Account

def get_writer(request,id):
    wrt =get_object_or_404(Writer,id=id)
    books = Books.objects.filter(writer_id=wrt)
    context = {
        'wrt': wrt,
        'books': books,
    }
    return render(request, 'writer.html', context)

def book_detail(request,id):
    book = get_object_or_404(Books,id=id)

    comments = book.comments.all()  # 💡 Bütün istifadəçilər görə bilir

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid(): # formun daxilindəki məlumatı yoxlayır və doğru olub-olmadığını müəyyən edir.
                new_comment = form.save(commit=False)
                # commit = False formu dərhal database - ə yazmamaq üçündürnki, əlavə
                # lazımlı məlumatları(book və user) biz özümüz əlavə edə bilək.
                new_comment.book = book
                new_comment.user = request.user
                new_comment.save()
                return redirect('book_detail', id=book.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, "book_detail.html", {
        "book": book,
        "comments": comments,
        "form": form,
    })

def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)

    # Yalnız koment sahibinə icazə ver
    if request.user == comment.user:
        comment.delete()

    return redirect('book_detail', id=comment.book.id)

