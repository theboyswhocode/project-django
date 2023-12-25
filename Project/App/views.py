from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, HttpResponse
# from django.contrib.auth.models import User
from App.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from Project_GRI import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def signin(request):
    if request.method == "POST":
        email = request.POST['user-email']
        password = request.POST['user-password']
        user = authenticate(username= email, password= password)
        if user is not None:
            login(request, user)
            name = request.user.name
            return redirect('/profile')
        
        else:
            messages.error(request, "Bad Credentials")
            return redirect('/home')


    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.method == "POST":
        name = request.POST['user-name']
        email = request.POST['user-email']
        password1 = request.POST['user-password']
        passsword2 = request.POST['user-password2']
        if CustomUser.objects.filter(email = email):
            messages.error(request, "Already registered")
            redirect('/home')
        if password1 != passsword2:
            messages.error(request, "Password doesn't match")
            redirect('/home')

        # myuser = User.objects.create_user(username= email, email=email, password= password1)
        # User = CustomUser()
        myuser = get_user_model().objects.create_user(email, password1)
        myuser.name = name
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Account successfully created")

        subject = "Welcome to Gotham Regency Inn"
        message = f"Hello {myuser.name},\n\nWe thank you for becoming a member of GRI. We provide experience for handcrafted luxury.\nPlease activate your account from the next mail.\n\nThank You,\nGotham Regency Inn"
        from_email = settings.EMAIL_HOST_USER
        to_mail = [myuser.email]
        send_mail(subject, message, from_email, recipient_list=to_mail, fail_silently=False)

        #confirmation mail
        current_site = get_current_site(request)
        email_subject = "Confirm Email for GRI"
        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        token = generate_token.make_token(myuser)
        activation_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        email_message = render_to_string('email_confirmation.html', 
        {
            'name': myuser.name,
            'domain': current_site.domain,
            'activation_url': activation_url,
        })
        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.send(fail_silently= True)
        return redirect('/login')
    return render(request, 'signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser) 
        messages.success(request, "Email Confirmation successfull")
        return redirect("/home")
    else:
        messages.error(request, "Email not confirmed")
        return redirect('/home')
    
def check_and_append(string, processed_string) -> str:
    str_list = string.split("_")
    pro_list = processed_string.split("_")
    if processed_string == "":
        if processed_string not in str_list:
            for item in pro_list:
                if item not in str_list:
                    str_list.append(item)
        str_list.pop(str_list.index(""))
    else:
        if processed_string not in str_list:
            for item in pro_list:
                if item not in str_list:
                    str_list.append(item)
    return str("_".join(str_list))


def find(request):
    hotel_dict = {
        'dubai': 'dub',
        'abudhabi': 'abd',
        'newyork': 'nyc',
        'tokyo': 'tok',
        'amsterdam': 'ams',
        'pyongyang': 'pyo',
        'riodejanerio': 'rdj',
        'munich': 'mch',
        'venice': 'vnc',
    }
    hotels = []
    if request.method == "POST":
        if 'hotel' in request.POST:
            select = request.POST['hotel']
            if select in hotel_dict:
                hotels.append(hotel_dict[select])
            if len(hotels) != 1:
                hotels_str = str("_".join(hotels))
            else:
                hotels_str = ""
                for item in hotels:
                    hotels_str = hotels_str + item
        if not request.user.is_authenticated:
            messages.error(request, "Please login")
        user_hotels = request.user.hotel
        new_hotels = check_and_append(user_hotels, hotels_str)
        print(new_hotels)
        request.user.hotel = new_hotels
        request.user.credit_points -= 1000
        request.user.save()
        messages.success(request, "Booked")

    return render(request, 'find.html')


def terms(request):
    return render(request, 'terms.html')

def about(request):
    if request.method == "POST":
        select = request.POST['handleButton']
        if select == 'redirect':
            return redirect('/find')
    return render(request, "about_us.html")

def home(request):
    if request.method == "POST":
        select = request.POST['handleButton']
        if select == 'redirect':
            return redirect('/find')
    return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        hotel_dict = {
            'dub': 'GRI, Dubai, UAE',
            'abd': 'GRI, Abu Dhabi, UAE',
            'nyc': 'GRI, New York, USA',
            'tok': 'GRI, Tokyo, Japan',
            'ams': 'GRI, Amsterdam, Netherlands',
            'pyo': 'GRI, Pyongyang, North Korea',
            'rdj': 'GRI, Rio de Janerio, Brazil',
            'mch': 'GRI, Munich, Germany',
            'vnc': 'GRI, Venice, Italy',
        }
        name = request.user.name
        username = request.user.email
        user_membership = request.user.membership
        credits = request.user.credit_points
        # hotels = ["GRI, Dubai, UAE", "GRI, Abu Dhabi, UAE"]
        usr_hotels =  request.user.hotel
        tmp = usr_hotels.split("_")
        if "" in tmp:
            tmp.pop(tmp.index(""))
        hotels = []
        for item in tmp:
            hotels.append(hotel_dict[item])
        if request.method == "POST":
            button = request.POST['handle_button']
            if button == "gold":
                request.user.membership = 'Gold'
                request.user.save()
                messages.success(request, f"Upgraded membership to {request.user.membership}")
            elif button == "goldpro":
                request.user.membership = 'GoldPro'
                request.user.save()
                messages.success(request, f"Upgraded membership to {request.user.membership}")
            elif button == "renew":
                messages.success(request, f"Renewed membership. Current membership status {user_membership}")
            elif button == "logout":
                request.user.save()
                logout(request)
                messages.warning(request, "Account Logged Out")
                return redirect("/home")
            elif button == "delete":
                get_user_model().objects.get(email= username).delete()
                messages.warning(request, "Account Deleted")
                return redirect("/home")
            elif button == "addcredits":
                request.user.credit_points += 10000
                request.user.save()
            elif button == "remove_mem":
                messages.warning(request, "Removed Membership")
                request.user.membership = "None"
                request.user.save()
        return render(request, 'profile.html', {'username': request.user.name, 'membership': request.user.membership, 'credits': request.user.credit_points, 'hotel': hotels})
    else:
        messages.error(request, "Please Login first")
        return redirect("/home")