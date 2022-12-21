from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import Categories, Course, Level, Video, UserCourse, Payment
from django.template.loader import render_to_string
from django.http import JsonResponse
from app.EmailBackEnd import EmailBackEnd
from django.db.models import Sum 
from time import time
import razorpay
from .settings import *

client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))
def BASE(request):
    return render(request,'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status ='PUBLISH').order_by('-id')
    context ={
        'category' : category,
        'course' : course,
    }
    return render(request,'main/home.html',context)

def SINGLE_COURSE(request):
    level = Level.objects.all()
    category = Categories.get_all_category(Categories)
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price =0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context= {
        'category' : category,
        'level' : level,
        'course' : course,
        'FreeCourse_count' : FreeCourse_count,
        'PaidCourse_count' : PaidCourse_count,
         
    }
    return render(request,'main/single_course.html',context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')



    if price == ['PriceFree']:
       course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})
    

def CONTACT_US(request):
    category = Categories.get_all_category(Categories)
    context ={
        'category': category
    }
    return render(request,'main/contact_us.html',context) 
    
def ABOUT_US(request):
    category = Categories.get_all_category(Categories)
    context ={
        'category': category
    }
    return render(request,'main/about_us.html',context) 

def DO_LOGIN(request):
    if request.method == "post":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(username, password)
        user = authenticate(request,username=username,password=password)
        
        if user!=None:
            login(request,user)
            return redirect ('home')
        else:
           messages.error(request,'Username and Password Are Invalid !')
           return redirect ('login')
    

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email Already Exists !')
           return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'Username Already exists !')
           return redirect('register')
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'registration/register.html') 

def PROFILE(request):
    return render(request,'registration/profile.html')

def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        user = User.objects.get(id=user_id) 
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password != None and password != "":
                user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')
    
def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
        if user!=None:
           login(request,user)
           return redirect('home')
        else:
           messages.error(request,'Username and Password Are Invalid !')
           return redirect('login')
       
def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    category = Categories.get_all_category(Categories)
    context ={
        'course':course,
        'category': category
    }
    return render(request, 'search/search.html',context)

def COURSE_DETAILS(request,slug):
    course = Course.objects.filter(slug = slug)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    category = Categories.get_all_category(Categories)
    
    course_id = Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user=request.user,course=course_id )
    except UserCourse.DoesNotExist:
        check_enroll = None
        
    
    if course.exists():
        course = course.first()
    else:
        return redirect ('404')
    context = {
        'course':course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        }
    return render(request, 'course/course_details.html',context)

def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context ={
        'category': category
    }
    return render(request, 'error/404.html',context)

def CHECKOUT(request,slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request,'Course enrolled successfully!')
        return redirect ('my_course')
    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments =request.POST.get('order_comments')
            
            amount= course.price
            currency = "USD"
            notes = {
                "name": f'{first_name} {last_name} ',
                "country": country,
                "address_1": f'{address_1} {address_2}',
                "city": city,
                "state": state,
                "postcode": postcode,
                "phone": phone,
                "email": email,
                "order_comments": order_comments,
            }
            receipt = f"ThirdEye-{int(time())}"
            
            payment = Payment(
                course=course,
                user=request.user,
                
            )
            payment.save()
            usercourse = UserCourse(
                user = payment.user,
                course = payment.course,
                
            )
            usercourse.save()
            return redirect ('my_course')
            
            
            
            
    context = {
        'course':course,
        
        }
    return render (request, 'checkout/checkout.html',context)

def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)
    context = {
        'course': course
        }
    return render(request, 'course/my-course.html',context)

def EVENTS(request):
    return render(request, 'events/events.html')
	
	

    

    
    