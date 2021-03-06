from django.shortcuts import redirect, render
from .models import Item, OrderItem, OTPs, UnconfirmOrders
from django.db.models import F
from django.contrib import messages
import math, random, smtplib
from datetime import datetime, timedelta
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

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email_address = request.POST['email_address']
        address = request.POST['address']
        message = request.POST['message']
        quantity = request.POST['quantity']
        contact_number = request.POST['contact_number']

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

            saveotp = OTPs.objects.create(otpcurrent=OTP, emailotp=emailid)
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

            ordermade = UnconfirmOrders.objects.create(firstname=firstname, lastname=lastname, email_address=email_address, address=address, item_name = name, message=message, quantity=quantity, contact_number=contact_number, order_itemid=id)
            ordermade.save()

            customers =  UnconfirmOrders.objects.filter(contact_number=contact_number)

            listvariables = zip(items, customers)
            context = {
                'listvariables' : listvariables,
            }

            return render(request,'otp-confirmation.html', context);

        elif checkquantity < int(quantity) and checkquantity > 1:
            messages.error(request, 'ORDER FAILED! You are trying to order a quantity above the current stocks')
            return redirect(back)

        else:
            messages.error(request, 'ORDER FAILED! You are trying to order on a sold out item')
            return redirect(back)
    else:
        return render(request,'home.html');

def otp_confirmation(request, id, name, contact_number):

    items = Item.objects.filter(id=id)
    back = "/order/{}".format(id)

    if request.method == 'POST':
        customerinput = request.POST['otp_confirm']
        checkotp = OTPs.objects.filter(otpcurrent=customerinput).exists()
        
        if checkotp == True:

            checkquantity2 = Item.objects.get(id=id).quantity
            quantity = UnconfirmOrders.objects.get(contact_number=contact_number).quantity

            if checkquantity2 >= int(quantity):
                firstname = UnconfirmOrders.objects.get(contact_number=contact_number).firstname
                lastname = UnconfirmOrders.objects.get(contact_number=contact_number).lastname
                email_address = UnconfirmOrders.objects.get(contact_number=contact_number).email_address
                address = UnconfirmOrders.objects.get(contact_number=contact_number).address
                message = UnconfirmOrders.objects.get(contact_number=contact_number).message
                quantity = UnconfirmOrders.objects.get(contact_number=contact_number).quantity
                contact_number = UnconfirmOrders.objects.get(contact_number=contact_number).contact_number
                order_itemid = UnconfirmOrders.objects.get(contact_number=contact_number).order_itemid
                item_name = UnconfirmOrders.objects.get(contact_number=contact_number).item_name
                orderdate = UnconfirmOrders.objects.get(contact_number=contact_number).orderdate

                confirmorder = OrderItem.objects.create(firstname=firstname, lastname=lastname, email_address=email_address, address=address, item_name = item_name, message=message, orderdate=orderdate, quantity=quantity, contact_number=contact_number, order_itemid=order_itemid)
                confirmorder.save()

                currentquantity = Item.objects.get(id=id)
                
                currentquantity.quantity = F('quantity') - quantity
                currentquantity.save()

                delete_otp = OTPs.objects.get(otpcurrent=customerinput)
                delete_otp.delete()
                UnconfirmOrders.objects.filter(contact_number=contact_number).delete()
                OTPs.objects.filter(otp_expire__lte=datetime.now()-timedelta(seconds=120)).delete()
                messages.success(request, 'Order was made successfully!')
                return render(request,'orderconfirm.html', {'items': items});

            elif checkquantity2 < int(quantity) and checkquantity2 > 1:
                UnconfirmOrders.objects.filter(contact_number=contact_number).delete()
                messages.error(request, 'ORDER FAILED! You are trying to order a quantity above the current stocks')
                return redirect(back)

            else:
                UnconfirmOrders.objects.filter(contact_number=contact_number).delete()
                messages.error(request, 'ORDER FAILED! You are trying to order on a sold out item')
                return redirect(back)

        else:
            checkexpire = OTPs.objects.filter(otp_expire__lte=datetime.now()).exists()

            if checkexpire == True:
                OTPs.objects.filter(otp_expire__lte=datetime.now()-timedelta(seconds=120)).delete()
                UnconfirmOrders.objects.filter(contact_number=contact_number).delete()
                messages.error(request, 'Uh-oh, You have entered an invalid OTP. Please Try to order again to generate new OTP')
                return redirect(back)

            else:
                UnconfirmOrders.objects.filter(contact_number=contact_number).delete()
                messages.error(request, 'Uh-oh, You have entered an invalid OTP. Please Try to order again to generate new OTP')
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