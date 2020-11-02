from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib import messages
import datetime
from datetime import date
from . forms import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.crypto import get_random_string


from django.core.mail import send_mail
import math, random



def forgotpassword(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        print(email)
        # res=send_mail(
        #     'Subject here',
        #     'Click here. http://127.0.0.1:8000/',
        #     'minu@antonal.com',
        #     [email],
        #     fail_silently=False,

        # )
        digits = "0123456789"
        OTP = ""

        # length of password can be chaged
        # by changing value in range
        OTP=otp = get_random_string(6, allowed_chars='0123456789')

        print(OTP)
        res = send_mail(
            'Subject here',
            'OTP is '+ OTP,
            'minu@antonal.com',
            [email],
            fail_silently=False,


        )
        return HttpResponse('%s' %res)
    # return HttpResponse('%s'%res)

    return render(request,'forgotpassword.html')

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('expense_list')
        else:
            return redirect('view_expense')
    elif request.method == 'POST':
        form=AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(request.user.is_active)
        if user is not None:
            form = login(request, user)
            if request.user.is_active:
                if request.user.is_superuser:
                    return redirect('expense_list')
                else:
                    return redirect('view_expense')
            else:
                print(request.user.is_active)
                messages.info(request, 'Admin has not approved')
                return redirect('index')
        else:
            messages.info(request,'User does not exist or admin has not approved')
            return redirect('register')
    else:
        form = AuthenticationForm()
        return render(request,'index.html',{'form':form})

def register(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('expense_list')
        else:
            return redirect('view_expense')
    elif request.method == 'POST':
        f=UserCreation(request.POST)
        f.is_active='False'
        print(" status",f.is_active)
        if f.is_valid():
            f.save()
            print("success")
            messages.success(request,'Registered successfully')
            return redirect('register')
    else:
        f=UserCreation()
    return render(request,'register.html',{'form':f})


@login_required(login_url='/')
def add_expense(request):
    today = datetime.datetime.now()
    y = today.strftime("%Y-%m-%d")
    if request.method == 'POST':
        f=Detailsform(request.POST)
        if f.is_valid():
            user = request.user
            ex = Expense()
            ex.date = y
            ex.description = f.cleaned_data['description']
            ex.category = f.cleaned_data['category']
            ex.amount = f.cleaned_data['amount']
            ex.username = user
            ex.gsttot=ex.amount*ex.category.gst/100
            ex.save()
            messages.success(request, 'Expense added')
            f=Detailsform()
            return render(request, 'add-expense.html',{'f':f})
    f=Detailsform()
    return render(request, 'add-expense.html',{'f':f})

@login_required(login_url='/')
def view_expense(request):
    f=Filterform()
    ab = Expense.objects.filter(username=request.user)
    sum = 0
    for i in ab:
        sum = sum + i.gsttot
    return render(request, 'view_expense.html', {'ab': ab, 'sum': sum,'f':f})


@login_required(login_url='/')
def filter_expense(request):
    f = Filterform(request.POST)
    if(f.is_valid()):
        fromdate = request.POST.get('fdate')
        print(fromdate)
        todate = request.POST.get('tdate')
        category = f.cleaned_data['category']
        print(fromdate,todate,category)
        ab = Expense.objects.filter(date__lte=todate, date__gte=fromdate, category__category__contains=category,
                                    username=request.user)
        return redirect('view_expense')



@login_required(login_url='/')
def edit_expense(request,id):
    ex=Expense.objects.get(id=id)
    f=Detailsform(instance=ex)
    if ex.username==request.user.username:
        if request.method == 'POST':
            f = Detailsform(request.POST)
            if f.is_valid():
                ex.description = f.cleaned_data['description']
                ex.category = f.cleaned_data['category']
                ex.amount = f.cleaned_data['amount']
                ex.gsttot = ex.amount * ex.category.gst / 100
                ex.save()
                messages.success(request, 'Expense edited')
                f = Detailsform()
                ab = Expense.objects.filter(username=request.user)
                return redirect('view_expense')
        return render(request, 'edit_expense.html', {'f': f})
    messages.info(request,'Sorry, id not found')
    return redirect('view_expense')

@login_required(login_url='/')
def delete_expense(request,id):
    ab=Expense.objects.get(id=id).delete()
    ab = Expense.objects.filter(username=request.user)
    messages.success(request, 'Expense deleted')
    return redirect('view_expense')

@login_required(login_url='/')
def expense_list(request):
    f=Filterform()
    ab = Expense.objects.all()
    sum = 0
    for i in ab:
        sum = sum + i.amount
    return render(request,'expense-list.html', {'ab': ab, 'sum': sum,'f':f})

@login_required(login_url='/')
def admin_filter_expense(request):
    f = Filterform(request.POST)
    if (f.is_valid()):
        fromdate = request.POST.get('fdate')
        print(fromdate)
        todate = request.POST.get('tdate')
        category = f.cleaned_data['category']
        print(fromdate, todate, category)
        ab = Expense.objects.filter(date__lte=todate, date__gte=fromdate, category__category__contains=category)
        sum = 0
        for i in ab:
            sum = sum + i.amount
        return render(request, 'expense-list.html', {'ab': ab, 'sum': sum, 'f': f})

@login_required(login_url='/')
def admin_edit_expense(request,id):
    ab=Expense.objects.get(id=id)
    print(ab.date)
    if request.method == 'POST':
        description = request.POST.get('des')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        ab.description = description
        ab.category = category
        ab.amount = amount
        ab.save()
        messages.success(request, 'Expense edited')
        return redirect('expense_list')
    else:
        return render(request,'admin_edit_expense.html',{'ab':ab})

@login_required(login_url='/')
def admin_delete_expense(request,id):
    ab=Expense.objects.get(id=id).delete()
    ab = Expense.objects.all()
    messages.success(request, 'Expense deleted')
    return redirect('expense_list')

@login_required(login_url='/')
def users_list(request):
    if request.user==request.user.is_superuser:
        ab=User.objects.exclude(username=request.user)
        return render(request,'users_list.html',{'ab':ab})
    else:
        messages.info(request, 'Sorry, not found')
        return redirect('index')

@login_required(login_url='/')
def approve(request,id):
    cd=User.objects.get(id=id)
    cd.is_active=True
    cd.save()
    messages.success(request, "Approved")
    ab=User.objects.exclude(username=request.user)
    return render(request,'users_list.html',{'ab':ab})

@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('index')

