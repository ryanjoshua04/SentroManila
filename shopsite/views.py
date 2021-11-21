from django.shortcuts import redirect, render
from .models import Items
from .models import OrderItems
# Create your views here.
def home(request):
    shoe = Items.objects.all()
    return render(request,'home.html', {'shoe': shoe});

def order(request, id):
    items = Items.objects.filter(id=id)

    return render(request,'makeorder.html', {'items': items});

def makeorder(request, id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email_address = request.POST['email_address']
        address = request.POST['address']
        message = request.POST['message']
        quantity = request.POST['quantity']
        contact_number = request.POST['contact_number']

        ordermade = OrderItems.objects.create(firstname=firstname, lastname=lastname, email_address=email_address, address=address, message=message, quantity=quantity, contact_number=contact_number, order_itemid=id)
        ordermade.save();

        return render(request,'home.html');
    else:
        return render(request,'home.html');

#def otp(request):