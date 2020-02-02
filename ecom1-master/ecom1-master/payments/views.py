from django.shortcuts import render

def checkout_payment(request):
    return render(request,'payments/payment_checkout.html')
