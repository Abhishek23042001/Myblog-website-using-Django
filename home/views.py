from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact,UserProfile
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import forms
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,send_mass_mail,mail_admins,mail_managers

# Create your views here.
def home(request):
    return render(request,'home/home.html')

def about(request):
    messages.success(request,'This is About Us')
    return render(request,'home/about.html')

    
def contact(request):
    #messages.error(request,'Welcome to Contact Us')
    if request.method=='POST':
        name= request.POST.get('name','')
        email=request.POST.get('email','')
        phone= request.POST.get('phone','')
        Disc= request.POST.get('Disc','')
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(Disc)<4:
            messages.error(request,'Please fill all the details Correctly!!')
        else:
            contact = Contact(name=name,email=email,phone=phone,Disc=Disc)
            contact.save()
            messages.success(request,'Your details has been Sent Successfully!')
    
    return render(request,'home/contact.html')


def search(request):
    query= request.GET.get('query')
    if len(query) > 100:
        allposts= Post.objects.none()
    else:
        allpoststitle= Post.objects.filter(title__icontains= query)
        allpostscontent= Post.objects.filter(content__icontains= query)        
        allpostsauthor= Post.objects.filter(author__icontains= query)        

        allpost= allpoststitle.union(allpostscontent) # Merge the search result of two queryset allposttitle and allpostcontent
        allposts= allpost.union(allpostsauthor)
    if  allposts.count() == 0:
        messages.warning(request,'No search results found. Please enter correct keyword in search !!!')
    params={'allposts': allposts,'query':query}
    
    return render(request,'home/search.html',params)


def handlesignup(request):
    if request.method == 'POST':
        username= request.POST.get('username','')
        fname= request.POST.get('fname','')
        lname= request.POST.get('lname','')
        email= request.POST.get('email','')
        pass1= request.POST.get('pass1','')
        pass2= request.POST.get('pass2','')

        #Checks for validation of user information in Signup page
        if len(username) > 15:
            messages.error(request,"Username must be under 15 characters")
            return redirect('home')

        if not username.isalnum:
            messages.error(request,"Username must contain aplphabets or atleast one number  ")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request,"Confirmed password do not matched with Above password ")
        
        if len(pass1)<= 8 or len(pass2)<= 8:
            messages.error(request,"Length of password should be greater than or equal to 8")
            return redirect('home')
        
        # Create The User
        if User.objects.filter(username__iexact= username).exists():
            #raise forms.ValidationError('Username already exists')
            messages.error(request,'Username already exists!')
        else:
            myuser= User.objects.create_user(username, email, pass1)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            messages.success(request,"Your Account has been Successfully Created")
        return redirect('home') # redirect to '/' i.e home page here name='home' is used
    else:
       return HttpResponse('404-Error Authentication Not Allowed')

def handlelogin(request):
    if request.method == 'POST':
        loginusername= request.POST.get('loginusername','')
        loginpassword= request.POST.get('loginpass','')

        user= authenticate(username=loginusername,password=loginpassword)

        if  user is not None:
            login(request, user)
            messages.success(request,"Successfully Loged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Username and Password, please try again!")
            return redirect('home')
             
    return HttpResponse('404 - Not found')

def handlelogout(request):
    #if request.method == "POST":
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
    return HttpResponse('handlelogout')

@login_required
def password_change(request):
    if request.method == 'POST':
        
        form = PasswordChangeForm(user= request.user,data= request.POST)
         #request.user means current user which is logged in
        if form.is_valid():
            print( 'form validisTrue')            # request.POST means accept the post request
            user = form.save()
            update_session_auth_hash(request, user)  # Important! # We have change the password but we have to change the hash form of password also in admin panel
            messages.success(request, 'Your password was successfully updated!')   # so we change hash form using update_session_auth_hash
            return redirect('password_change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/change_password.html', {'form': form})
    
    
def send_mails(request):
    mail= send_mail('test', 'test', 'test@test.com', ['my-personal-email@gmail.com'],fail_silently=False)
    if mail:
        return HttpResponse(mail)
    else:
        raise Exception("Error")

def password_reset(request):
    return render(request,'home/password_reset_form.html')

def index(request):
    users= UserProfile.objects.all()
    context={'users': users}
    return render(request,'home/index.html',context)


def upload(request):
    pic= request.FILES['image']
    name= request.POST.get('name')
    user= UserProfile(name=name,pic= pic)
    user.save()
    
    return render(request,'home/index.html')