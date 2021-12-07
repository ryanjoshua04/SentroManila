from django.shortcuts import redirect, render
from .models import Items
from .models import OrderItems
from django.db.models import F
from django.contrib import messages
import math, random, smtplib
# Create your views here.
def home(request):
    shoe = Items.objects.all()
    return render(request,'home.html', {'shoe': shoe});

def order(request, id):
    items = Items.objects.filter(id=id)

    return render(request,'makeorder.html', {'items': items});

def makeorder(request, id, name):
    items = Items.objects.filter(id=id)

    global firstname, lastname, email_address, address, message, quantity, contact_number, orderverification, OTP, ordermade
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email_address = request.POST['email_address']
        address = request.POST['address']
        message = request.POST['message']
        quantity = request.POST['quantity']
        contact_number = request.POST['contact_number']

        digits="ABCDEFG0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("inquiresentromanila@gmail.com", "lmvhvthoqmonrnnt")

        emailid = email_address

        msg = """From: Sentro Manila <inquiresentromanila@gmail.com>
To: Customer <{}>
MIME-Version: 1.0
Content-type: text/html
Subject: OTP for order confirmation

<h2>This is your One-Time Password:</h2> -------------------- \n <h1>{}</h1> -------------------- \n <br>

<i>IMPORTANT: The contents of this email and any attachments are confidential. It is strictly forbidden to share any part of this message with any third party, without a written consent of the sender. If you received this message by mistake, please reply to this message and follow with its deletion, so that we can ensure such a mistake does not occur in the future.</i>
""".format(emailid,OTP)

        s.sendmail('&&&&&&&&&&&',emailid,msg)
        return render(request,'otp-confirmation.html', {'items': items});
    else:
        return render(request,'home.html');

def otp_confirmation(request, id, name):
    items = Items.objects.filter(id=id)
    if request.method == 'POST':
        customerinput = request.POST['otp_confirm']
        if customerinput == OTP:
            ordermade = OrderItems.objects.create(firstname=firstname, lastname=lastname, email_address=email_address, address=address, item_name = name, message=message, quantity=quantity, contact_number=contact_number, order_itemid=id)
            ordermade.save()
            currentquantity = Items.objects.get(id=id)
            
            currentquantity.quantity = F('quantity') - quantity
            currentquantity.save()
            messages.success(request, 'Order was made successfully!')
            return render(request,'orderconfirm.html', {'items': items});
        else:
            messages.warning(request, 'Uh-oh, You have entered an invalid OTP. Please Try to order again')
            return render(request,'orderdenied.html', {'items': items});
    else:
        return render(request,'otp-confirmation.html');