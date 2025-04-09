from django.shortcuts import render,redirect
from .forms import JoinForm,LoginForm
from django.contrib.auth import login,logout
from .models import CustomUser
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def home(request):
    return render(request, 'home/home.html')

#the join view that recive the user input and cheach for the user than log him in
def join(request):
    if request.method=='POST':
        form=JoinForm(request.POST)
        if form.is_valid(): #cheak if user input valid vai the form fields
            user=form.save()
            login(request,user)

            return redirect('home')
        else:
            print(form.errors)
    form=JoinForm()
    return render(request,"home/join.html",{"form":form})

#Cartview
def CartView(request):
    return render(request,'home/CartView.html')



#login view    
def custom_login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=CustomUser.objects.get(Username=username)
            if user is not None:
                print("success")
                login(request,user)  
                return redirect('home')
            else:
                return render(request,'home/login.html',{'form':form})

        else:
            return render(request,'home/login.html',{'form':form})
            
    else:
        form=LoginForm()
        return render(request,'home/login.html',{'form':form})
#logout view
def logout_view(request):
    logout(request)
    return redirect('home')