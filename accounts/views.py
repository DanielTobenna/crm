from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from django.contrib import messages

from .forms import OrderForm, CreateUserForm, CustomerForm

from .models import *
from .filters import OrderFilter

from .decorators import unauthenticated_user, allowed_users, adminonly

# Create your views here.

@unauthenticated_user
def registerpage(request):
	form= CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username= form.cleaned_data.get('username')
			messages.success(request, "Account was created for " + username)

			'''group= Group.objects.get(name='customer')
				
			user.groups.add(group)

			Customer.objects.create(

				user=user,
				name= user.username,
				email= user.email,

				)
				In the signals.py file is where we did all this code inour comment
				'''


			return redirect('login')

	context={'form':form}

	return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginpage(request):

	if request.user.is_authenticated:
		return redirect('/')

	else:
		if request.method == "POST":
			username= request.POST.get('username')
			password= request.POST.get('password')

			user= authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('/')

			else:
				messages.error(request, "username or password is incorrect")


		context={}

		return render(request, "accounts/login.html", context)


def logoutuser(request):
	logout(request)
	return redirect('login')



@login_required(login_url='login')
@adminonly
def home(request):
	customers= Customer.objects.all()

	total_customers= customers.count()
	
	orders= Order.objects.all()

	total_orders= orders.count()

	delivered= orders.filter(status='Delivered').count()

	pending= orders.filter(status='Pending').count()

	context= {
		'pending': pending,
		'delivered': delivered,
		'total_orders': total_orders,
		'customers': customers,
		'orders': orders,
	}
	return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userprofile(request):

	orders= request.user.customer.order_set.all()

	total_orders= orders.count()

	delivered= orders.filter(status='Delivered').count()

	pending= orders.filter(status='Pending').count()

	context= {  'orders': orders,
				'total_orders': total_orders,
				'delivered': delivered,
				'pending': pending,
			}

	return render(request, "accounts/user_profile.html", context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer= request.user.customer

	form=CustomerForm(instance=customer)

	if request.method=='POST':
		form= CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context= {"form":form}

	return render(request, 'accounts/account_settings.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products= Product.objects.all()
	context= {
		'products': products
	}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):

	customer= Customer.objects.get(id=pk)

	orders= customer.order_set.all()

	orders_count= orders.count()

	myFilter= OrderFilter(request.GET, queryset=orders)

	orders= myFilter.qs

	context= {
		'customer': customer,
		'orders': orders,
		'orders_count': orders_count,
		"myFilter": myFilter
		}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet= inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
	customer= Customer.objects.get(id=pk)
	#form= OrderForm(initial={'customer':customer})
	formset= OrderFormSet(queryset=Order.objects.none(),instance=customer)

	if request.method == 'POST':
		#form= OrderForm(request.POST)
		formset= OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context= {'formset':formset}

	return render(request, "accounts/orderform.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, pk):
	order= Order.objects.get(id=pk)
	
	form= OrderForm(instance=order)

	if request.method == 'POST':
		form= OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context= {'form':form, 'order':order}

	return render(request, "accounts/orderform.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request, pk):
	order= Order.objects.get(id=pk)

	if request.method == 'POST':

		order.delete()

		return redirect('/')

	context= {'order':order}


	return render(request, "accounts/deleteform.html", context)