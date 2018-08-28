from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category
from django.contrib.auth.models import User, Group
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
# Create your views here.
def allProd_Cat(request,c_slug=None):
    c_page = None
    prod = None
    if c_slug!=None:
        c_page= get_object_or_404(Category,slug=c_slug)
        prod =Product.objects.filter(category=c_page,available=True)
    else:
        prod = Product.objects.filter(available=True)
    return render(request,'shop/categories.html',{'category':c_page,'product_by_category':prod})



def prod_details(request,c_slug,p_slug):
    try:
        product = Product.objects.get(category__slug=c_slug,slug=p_slug)

    except Exception as e :

        raise e

    return render(request,'shop/products.html',{'product':product})

def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)


    else:
            form = SignupForm()
    return render(request,'accounts/signup.html', {'form':form})


def signinView(request):
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('shop:allProd_Cat')
            else:
                return redirect('signup')

    else:
        form =AuthenticationForm()
    return render(request,'accounts/signin.html',{'form':form})

def signoutView(request):
    logout(request)
    return redirect('signin')

