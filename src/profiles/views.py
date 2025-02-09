from django.http import HttpResponse
from django.shortcuts import redirect, render
from sqlalchemy import null
from .models import Customer
from .forms import EditProfileForm

# =============================================================


def myProfile(request):
    user = request.user
    try:
        profile = Customer.objects.get(user=user)
            
        context = {
            "profile": profile,

        }

        return render(request, "my-profile.html", context)

    except:
        
        return redirect('login-account')



# =============================================================


def editMyProfile(request, pk):

    currentUser = request.user
    profile = Customer.objects.get(user=currentUser)
    id = profile.id
    editProfileForm = EditProfileForm(instance=profile)

    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my-profile')



    context = {
        "form": editProfileForm,
        'profileID': id,
    }

    if id == int(pk):
        return render(request, "editProfile.html", context)

    else:
        return HttpResponse("You Can't Edit Other's Profile")

