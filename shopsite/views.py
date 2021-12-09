from django.shortcuts import redirect, render
from .models import Item, OrderItem, OTPs
from django.db.models import F
from django.contrib import messages
import math, random, smtplib
# Create your views here.
def home(request):
    shoe = Item.objects.all()
    return render(request,'home.html', {'shoe': shoe});

def order(request, id):
    items = Item.objects.filter(id=id)

    return render(request,'makeorder.html', {'items': items});

def makeorder(request, id, name):
    items = Item.objects.filter(id=id)
    back = "/order/{}".format(id)

    global firstname, lastname, email_address, address, message, quantity, contact_number, orderverification, OTP, ordermade, emailid
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email_address = request.POST['email_address']
        address = request.POST['address']
        message = request.POST['message']
        quantity = request.POST['quantity']
        contact_number = request.POST['contact_number']

        global email
        def email():
            return email_address

        checkquantity = Item.objects.get(id=id).quantity
        if checkquantity >= int(quantity):
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("inquiresentromanila@gmail.com", "lmvhvthoqmonrnnt")

            emailid = email_address

            digits="ABCDEFG0123456789"
            OTP=""
            for i in range(6):
                OTP+=digits[math.floor(random.random()*10)]

            saveotp = OTPs.objects.create(otpcurrent=OTP, emailotp=email_address)
            saveotp.save()

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

        elif checkquantity < int(quantity) and checkquantity > 1:
            messages.error(request, 'ORDER FAILED! You are trying to order a quantity above the current stocks')
            return redirect(back)

        else:
            messages.error(request, 'ORDER FAILED! You are trying to order on a sold out item')
            return redirect(back)
    else:
        return render(request,'home.html');

def otp_confirmation(request, id, name):
    items = Item.objects.filter(id=id)
    back = "/order/{}".format(id)
    if request.method == 'POST':
        customerinput = request.POST['otp_confirm']
        emailid = email()
        checkotp = OTPs.objects.get(emailotp=emailid).otpcurrent
        if customerinput == checkotp:
            ordermade = OrderItem.objects.create(firstname=firstname, lastname=lastname, email_address=email_address, address=address, item_name = name, message=message, quantity=quantity, contact_number=contact_number, order_itemid=id)
            ordermade.save()
            currentquantity = Item.objects.get(id=id)
            
            currentquantity.quantity = F('quantity') - quantity
            currentquantity.save()

            delete_otp = OTPs.objects.get(emailotp=emailid)
            delete_otp.delete()
            messages.success(request, 'Order was made successfully!')
            return render(request,'orderconfirm.html', {'items': items});
        else:
            messages.error(request, 'Uh-oh, You have entered an invalid OTP. Please Try to order again to generate new OTP')
            delete_otp = OTPs.objects.get(emailotp=emailid)
            delete_otp.delete()
            return redirect(back)
    else:
        return render(request,'otp-confirmation.html');

def searchItem(request):
    if request.method == 'POST':
        search = request.POST['search']
        if Item.objects.filter(name__icontains=search).exists():
            shoe = Item.objects.filter(name__icontains=search)
            messages.success(request, 'Result for searched item: '+ search)
            return render(request,'home.html', {'shoe': shoe});
        else:
            shoe = Item.objects.all()
            messages.info(request, 'Sorry, no result for footware item: '+ search)
            return redirect('/')
    else:
        shoe = Item.objects.all()
        return redirect('/')