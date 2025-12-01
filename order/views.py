from django.shortcuts import render,redirect,get_object_or_404
from cart.models import Cart, CartItem
from .forms import OrderForm
from django.http import JsonResponse, Http404
from .models import District, OrderItem
from accounts.models import Account
from cart.views import _cart_id
import random
from django.views import View
from .pdfcreator import renderPdf
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Order

# Create your views here.
def order(request):
    cart_count = 0
    tax = 0.0
    total = 0.0
    cemi = 0.0
    number = random.randint(1000000, 9999999)
    customer = get_object_or_404(Account, id=request.user.id) # request.user.id → login olunan user-in id-si dir.

    if request.user.is_authenticated:
        form = OrderForm(initial={
            "name": customer.last_name + ' ' + customer.first_name,
            "phone": customer.phone_number,
            "email": customer.email,
            "account_no": number,
        })

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = Account.objects.get(id=request.user.id)
                cart_1 = Cart.objects.filter(cart_id=_cart_id(request))
                cart_items_1 = CartItem.objects.all().filter(cart=cart_1[:1])
                for cart_item in cart_items_1:
                    cart_count += cart_item.quantity
                    total += cart_item.quantity * cart_item.product.price
                    tax = float(2 * total / 100)
                    cemi = float(total + tax)
                order.payable = float(cemi)
                order.totalbook = cart_count
                order.save()

                cart_2 = Cart.objects.get(cart_id=_cart_id(request))
                cart_items_2 = CartItem.objects.filter(cart=cart_2, is_active=True)

                for item in cart_items_2:
                    OrderItem.objects.create(
                        order=order,
                        book=item.product,  # CartItem.product → Books FK
                        price=item.product.price,  # kitabın qiyməti
                        quantity=item.quantity
                    )
                cart_items_2.delete()
                return render(request, 'order/successFull.html', {'order': order})

    else:
        form = OrderForm()

    context = {
        'form': form,
    }

    return render(request, 'order/order.html', context)


# Ajax view - division seçiləndə district-ları qaytarır
def load_districts(request):
    division_id = request.GET.get('division_id') # bu division-un id-sini alır.
    districts = District.objects.filter(division_id=division_id).values('id', 'name') # [{'id': 1, 'name': 'Yasamal'}, {'id': 2, 'name': 'Nərimanov'}, {'id': 3, 'name': 'Xətai'}]
    return JsonResponse(list(districts), safe=False)

    # JsonResponse → serverdən browser - a JSON formatında cavab göndərir.

    # safe=True (default): Django yalnız dictionary (dict) tipli obyektləri JSON-a çevirə bilir.
    # Məsələn: {"key": "value"} ✅
    # List ([{"id":1,"name":"A"},{"id":2,"name":"B"}]) ❌ → TypeError verir.

    # safe=False: Django dict olmayan obyektləri (list, tuple və s.) JSON-a çevirməyə icazə verir.
    # Bizim districts queryset-i list(districts) → list tipindədir.
    # Ona görə safe=False qoyuruq ki, Django bunu JSON-a çevirsin.

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     response = HttpResponse(content_type='application/pdf')
#     pisa_status = pisa.CreatePDF(html,dest=response)
#     return response
#
#
# def order_pdf(request,order_id):
#     order = Order.objects.get(id=order_id)
#     order_items = order.items.all()
#
#     context = {
#         "order": order,
#         "items": order_items,
#     }
#
#     pdf = render_to_pdf('order/order_pdf.html', context)
#     pdf['Content-Disposition'] = f'attachment; filename="order_{order_items}_pdf"'
#     return pdf

# views.py
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Order
from .pdfcreator import renderPdf


class OrderPDFView(View):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)

        # related_name yoxdursa fallback edirik
        if hasattr(order, 'items'):
            items = order.items.all()
        else:
            items = order.orderitem_set.all()

        context = {
            'order': order,
            'items': items,
        }

        # renderPdf artıq HttpResponse qaytarır — onu birbaşa return et
        pdf_response = renderPdf('order/order_pdf.html', context)
        return pdf_response

