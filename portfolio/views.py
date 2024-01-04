from django.shortcuts import render, redirect, resolve_url
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
import uuid
from django.views.decorators.csrf import csrf_exempt
from network.models import UserProfile

def index(request):
    return render(request, 'portfolio/index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                next_url = request.GET.get('next')
                if next_url:
                    # Check if the next_url is safe to redirect to
                    return redirect(resolve_url(next_url))
                else:
                    return redirect('index')
    else:
        form = AuthenticationForm()
            
    return render(request, 'portfolio/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            new_user.email = f"{username}@example.com"
            
            new_user.save()
            
            login(request, new_user)
            
            next_url = request.GET.get('next')  # Get the 'next' parameter or default to index
            if not next_url:  # If 'next' is empty or not provided, set a default
                next_url = 'index'       
            
            messages.success(request, f'Account created for {username}')
            
            return redirect(next_url)
        else:
            messages.error(request, 'An error occurred during registration.')
    else:
        form = UserCreationForm()
        next_url = request.GET.get('next', '')
    return render(request, 'portfolio/register.html', {'form': form})

def logout_view(request):
    if 'is_guest' in request.session:
        User.objects.filter(username=request.user.username).delete()
        del request.session['is_guest']
    logout(request)
    return redirect('index')

def continue_as_guest(request):
    if request.method == 'POST':
        user = new_guest()

        if user is not None:
            login(request, user)
            request.session['is_guest'] = True
            project_url = request.POST.get('project_url', '/')

            return JsonResponse({'redirect_url': project_url})
        else:
            # Handle the error or redirect to an error page
            return JsonResponse({'error': 'Authentication failed'}, status=401)
    else:
        # Return an error if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def new_guest():
    unique_username = f"guest_{uuid.uuid4()}"
    unique_password = f"password_{uuid.uuid4()}"
     
    user = User.objects.create_user(username=unique_username, password=unique_password)
    UserProfile.objects.create(user=user)

    return user

@csrf_exempt
def send_contact_email(request):
    if request.method == "POST":
        name = request.POST.get('name')
        sender_email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            subject=f"Message from {name}",
            message=message,
            from_email=sender_email,
            recipient_list=['mgomzq@gmail.com'],
            fail_silently=False,
        )
        return JsonResponse({"success": "Email sent successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)