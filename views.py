
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from login.models import Task,Details
# Create your views here.
def home(request):
    context={'success':False}
    if request.method == 'POST':
       title = request.POST['title']
       desc= request.POST['desc']
       ins=Task(taskTitle=title,taskdesc=desc)
       ins.save();
       context = {'success':True}
    return render(request, 'home.html',context)
      
def task(request):
   allTasks=Task.objects.all() 
   if request.method=="POST":
       title = request.POST['title']
       desc= request.POST['desc']
       Task.objects.create(taskTitle=title,taskdesc=desc)
       messages.info(request,"task is added")
   context = {'tasks':allTasks}
   return render(request, 'task.html',context)

# def add(request):
#    if request.method == 'POST':
#        if "add" in request.POST:
#           title = request.POST.get('title')
#           desc= request.POST.get('desc')
#           Task.objects.create(taskTitle=title,taskdesc=desc)
          
#    return render(request,'task.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        user = auth.authenticate(username=username,password=password)
        if user is not None:
          auth.login(request,user)
          return redirect("/")
        else:
           messages.info(request,"invalid credentials")
           return redirect('login')
    else:
      return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if(password1==password2):
             if User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('register')
             elif User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('register')
             else:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                user.save();
                #print('user created')
                return redirect('login')
        else:
             messages.info(request,'password not matching.....')
             return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')

def logout(request):
   auth.logout(request)
   return redirect('/')         
