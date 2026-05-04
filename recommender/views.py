from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
                
                #basic validation
        if not name or not email or not phone or not password:
            messages.error(request, "PLease fill all requires fields. ")
            return redirect("signup")
        if len(password)< 6:
            messages.error(request,"password should be at least 6 character")
            return redirect("signup")
        if User.objects.filter(username=email).exists():
            messages.error(request,"Account already exist with this email")
            return redirect("signup")
        
        user = User.objects.create_user(username=email,password=password)
        print("USER SAVED:", user)
        if " " in name:
            first, last = name.split(" ",1)

        else:
            first,last = name,""
        user.first_name, user.last_name = first, last
        user.save()
        
        print("CREATING PROFILE")
        UserProfile.objects.create(user=user, phone=phone)
        print("PROFILE CREATED")
        login(request,user)
        messages.success(request, "Account created sucessfully. Welcome! ")
        return redirect ("predict")
            

    return render(request, "signup.html") 

from .ml.loader import predict_one, load_bundle
from django.contrib.auth.decorators import login_required ,user_passes_test


@login_required 
def predict_view (request):
    feature_order = load_bundle()["feature_cols"]
    result = None
    last_data = None


    if request.method == "POST":
        data = {}
        try:
            for c in feature_order:
                data[c] = float(request.POST.get(c))

        except ValueError:
            messages.error(request,"Please enter valid numeric values.")
            return redirect("predict")
        label = predict_one(data)


        Prediction.objects.create(user=request.user, **data , predicted_label= label) #**data => kwargs unpacking
        result = label 
        last_data = data
        messages.success(request,f"Reccommded Crop: {label}")

    return render(request, "predict.html",locals())




def logout_view (request):
    logout(request)
    messages.success(request, "Logout sucessfully !")
    return redirect ("login")




def login_view (request):
     if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if not user:
            messages.error(request, "invalid login Credentials")
            return redirect("login")
        login(request,user)
        messages.success(request, "Logged in sucessfully. ")
        return redirect("predict")
    
     return render(request, "login.html")


@login_required 
def user_history_view (request):
  predictions = Prediction.objects.filter(user=request.user)


  return render(request, "history.html",locals())




from django.shortcuts import get_object_or_404
@login_required 
def user_delete_prediction (request,id):
  prediction = get_object_or_404(Prediction,id=id, user=request.user)
  prediction.delete()
  messages.success(request, "Delete prediction sucessfully. ")


  return redirect("user_history")



@login_required 
def profile_view (request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        if name:
            parts = name.split(" ",1)
            request.user.first_name = parts[0]
            request.user.last_name = parts[1] if len(parts) > 1 else ""
        
        profile.phone = phone
        request.user.save()
        profile.save()

        messages.success(request,"Profile Updated.")
    full_name = request.user.get_full_name()


    return render(request,"profile.html",locals() )


@login_required 
def change_password_view (request):
   
    if request.method == 'POST':
        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")
        if not request.user.check_password(current):
            messages.error(request,"Incorrect password")
            return redirect("change_password")
        
        if len(new) < 6:
            messages.error(request,"New password must be at least 6 digit")
            return redirect("change_password")
        
        if new != confirm:
            messages.error(request,"password do not match.")
            return redirect("change_password")
        
        request.user.set_password(new)
        request.user.save()
        user = authenticate(request,username=request.user.username,password=new)

        if user:
            login(request,user)
            messages.success(request, "Password Change sucessfully. ")
            return redirect("change_password")
    return render(request,"change_password.html",locals() )




def admin_login_view (request):
     if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if not user:
            messages.error(request, "invalid login Credentials")
            return redirect("admin_login")
        if not user.is_staff:
            messages.error(request, "You are not authorized for admin panel")
            return redirect("admin_login")
        login(request,user)
        messages.success(request, "Logged in sucessfully. ")
        return redirect("admin_dashboard")
    
     return render(request, "admin_login.html")




def is_staff(user):
    return user.is_authenticated and user.is_staff



@user_passes_test(is_staff, login_url='admin_login')
def admin_dashboard_view (request):
    total_users = User.objects.filter(is_staff=False).count()
    total_predictions = Prediction.objects.count()

    return render(request,"admin_dashboard.html",locals() )



