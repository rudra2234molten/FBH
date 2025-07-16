from django.shortcuts import render, redirect, HttpResponse
from .models import Account
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def Index(request):
  return render(request,'index.html')

def Create(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    dob = request.POST.get('dob')
    mail = request.POST.get('mail')
    adhar = request.POST.get('adhar')
    pan = request.POST.get('pan')
    mobile = request.POST.get('phone')
    address = request.POST.get('address')
    data = Account.objects.create(name = name,DOB = dob,mail = mail, aadhar = adhar, pan = pan, mobile = mobile, address = address)
    data.save()

    subject = f"Thank You For Account Creation Mr/Ms {name}"
    body = (
        f"Dear {name},\n\n"
        "We are delighted to inform you that your new FBH (Fraud Bank of Hyderabad) account has been successfully opened! 🎉\n\n"
        "Account Details:\n"
        f"Account Holder: {name}\n"
        "Account Type: [Savings/Current]\n"
        "Branch: [Hyderabad Main Branch]\n\n"
        "You can now enjoy seamless banking services, including:\n"
        "✔ Instant fund transfers\n"
        "✔ 24/7 online banking\n"
        "✔ Exclusive customer support\n"
        "✔ High-security fraud protection (just kidding—or are we?)\n\n"
        "To activate your online banking, please log in here using your credentials. For any assistance, contact our customer care at 1800-FBH-HELP or visit your nearest branch.\n\n"
        "Thank you for choosing FBH—where your trust is our greatest asset (and possibly our only one).\n\n"
        "Warm regards,\n"
        "FBH Customer Support Team\n"
        "📞 1800-FBH-HELP | ✉ support@fbh.com | 🌐 www.fbh.com"
    )
    try:
        send_mail(
                subject, body, settings.EMAIL_HOST_USER,
                [mail], fail_silently=False
            )
        print('EMAIL SENT SUCCESSFULLY')
    except Exception as e:
      print(f'EMAIL FAILED: {e}') 

    return redirect('home')
  return render(request,'create.html')

def Pin(request):
  if request.method == 'POST':
    otp = random.randint(100000,999999)
    acc = request.POST.get('accountnum')
    data = Account.objects.get(acc = acc)
    email = data.mail
    title = f"Hello {data.name}," 
    body = f"\n Your OTP(one time password) is {otp}, \n Please dont share it with anyone. \n Thank You. \n FBH(Fraud Bank Of Hyderabad)"
    send_mail(title,body,settings.EMAIL_HOST_USER,[email],fail_silently = False)
    print('otp send')
    data.otp = otp
    data.save()
    return redirect('pin_valid')
  return render(request,'pin.html')

def Otp(request):
  if request.method == 'POST':
    acc = request.POST.get('accountnum')
    otp = int(request.POST.get('otp'))
    pinn = int(request.POST.get('pinn'))
    con_pin = int(request.POST.get('con_pin'))
    if pinn == con_pin:
      data = Account.objects.get(acc = acc)
      if data.otp == otp:
        data.pin = con_pin
        data.save()
        title = f"Hello {data.name},"
        body = f"\n Congratulation, you have Generated pin successfully. \n Your pin is {con_pin} \n Please dont share it with anyone. \n Thank You. \n FBH(Fraud Bank Of Hyderabad)" 
        send_mail(title,body,settings.EMAIL_HOST_USER,[data.mail],fail_silently=False)
        return redirect('home')
  return render(request,'pin_validation.html')

def Balance(request):
  data = None
  bal = 0
  msg = ''
  check = False
  check1 = False
  if request.method == 'POST':
    acc = int(request.POST.get('acc'))
    pin = int(request.POST.get('pinn'))
    try:
      data = Account.objects.get(acc = acc)
    except Exception as e:
      print(e)
    if data is not None:
      if data.pin == pin:
        bal = data.balance
        check = True
      else:
        check1 = True
        msg = 'Please Enter Currect Pin'
    else:
      check1 = True
      msg = 'Please Enter Valid Account Number'
  
  context = {
    'msg':msg,
    'bal':bal,
    'check':check,
    'check1':check1
  }
      
  return render(request,'balance.html',context)

def Withdraw(request):
  if request.method == 'POST':
    acc = int(request.POST.get('acc'))
    pin = int(request.POST.get('pin'))
    amount = int(request.POST.get('amount'))

    try:
      data = Account.objects.get(acc = acc)
    except Exception as e:
      print(e)

    if data.pin == pin:
      if amount < data.balance:
        data.balance -= amount
        data.save()
        title = f"Hello {data.name},"
        body = f"\n Your Account Depited Amount Of {amount} \n Current Balance is {data.balance} \n Thank You. \n FBH(Fraud Bank Of Hyderabad)" 
        send_mail(title,body,settings.EMAIL_HOST_USER,[data.mail],fail_silently=False)
        return redirect('home')
      ...
    else:
      ...
  return render(request,'withdraw.html')

def Deposite(request):
  if request.method == 'POST':
    acc = int(request.POST.get('acc'))
    pin = int(request.POST.get('pin'))
    amount = int(request.POST.get('amount'))
    try:
      data = Account.objects.get(acc = acc)
    except Exception as e:
      print(e)
    if amount >= 100 and amount <= 10000:
      data.balance += amount
      data.save()
      title = f"Hello {data.name},"
      body = f"\n Your Account Credited Amount Of {amount} \n Current Balance is {data.balance} \n Thank You. \n FBH(Fraud Bank Of Hyderabad)"  
      send_mail(title,body,settings.EMAIL_HOST_USER,[data.mail],fail_silently=False)
      return redirect('home')
  return render(request,'deposite.html')

def Transfer(request):
    if request.method == 'POST':
        sender_acc = int(request.POST.get('sender_acc'))
        pin = int(request.POST.get('pin'))
        receiver_acc = int(request.POST.get('receiver_acc'))
        amount = int(request.POST.get('amount'))

        try:
            sender = Account.objects.get(acc=sender_acc)
        except Account.DoesNotExist:
            print("Sender account not found.")
            return render(request, 'transfer.html', {'error': 'Invalid sender account'})

        if sender.pin != pin:
            return render(request, 'transfer.html', {'error': 'Incorrect PIN'})

        try:
            receiver = Account.objects.get(acc=receiver_acc)
        except Account.DoesNotExist:
            print("Receiver account not found.")
            return render(request, 'transfer.html', {'error': 'Invalid receiver account'})

        if sender.balance < amount:
            return render(request, 'transfer.html', {'error': 'Insufficient Balance'})

        # Perform transfer
        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        # Send confirmation emails
        sender_title = f"Hi {sender.name},"
        sender_body = f"₹{amount} has been debited from your account.\nNew Balance: ₹{sender.balance}\nThank you.\nFBH"

        receiver_title = f"Hi {receiver.name},"
        receiver_body = f"₹{amount} has been credited to your account.\nNew Balance: ₹{receiver.balance}\nThank you.\nFBH"

        send_mail(sender_title, sender_body, settings.EMAIL_HOST_USER, [sender.mail], fail_silently=False)
        send_mail(receiver_title, receiver_body, settings.EMAIL_HOST_USER, [receiver.mail], fail_silently=False)

        return redirect('home')

    return render(request, 'transfer.html')
