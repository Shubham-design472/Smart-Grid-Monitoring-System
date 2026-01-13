from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import GridData
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from .utils import detect_attack
import random
from django.utils import timezone
from .decorators import role_required

from django.http import JsonResponse
from rest_framework import generics
from .serializers import GridDataSerializer


class GridDataAPI(generics.ListAPIView):
    queryset = GridData.objects.all().order_by('-timestamp')
    serializer_class = GridDataSerializer

@login_required
def latest_grid_data(request):
    latest_data = GridData.objects.order_by('-timestamp')[:20]
    serializer = GridDataSerializer(latest_data, many=True)
    # convert timestamps to string
    data = serializer.data
    for d in data:
        d['timestamp'] = d['timestamp']  # Already string in DRF JSON
    return JsonResponse(data[::-1], safe=False)  # reverse for chronological order



def custom_logout(request):
    logout(request)  # clear the user session
    return redirect('login')  # after logout, go to login page



def home(request):
    return render(request, 'monitoring/home.html')





# ✅ Group-based access control
def group_required(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists() or user.is_superuser
    return user_passes_test(check)


@group_required('admin')
def admin_only_view(request):
    return render(request, 'monitoring/admin.html')
    





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # after login, go to dashboard
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'monitoring/login.html')




def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'

def is_operator(user):
    return hasattr(user, 'profile') and user.profile.role == 'operator'



@login_required
def dashboard(request):
    """Dashboard view for Admins/Operators"""
    
    # Latest 20 data points (oldest first)
    data = list(GridData.objects.all().order_by('-timestamp')[:20][::-1])

    # Detect attack/anomaly
    attack, anomaly = detect_attack(data)

    # Prepare lists for charts
    timestamps = [d.timestamp.strftime('%H:%M:%S') for d in data]
    voltages = [d.voltage for d in data]
    currents = [d.current for d in data]

    context = {
        "data": data,
        "attack": attack,
        "anomaly": anomaly,
        "timestamps": timestamps,
        "voltages": voltages,
        "currents": currents,
    }

    return render(request, "monitoring/dashboard.html", context)
    
    
@login_required
def admin_panel(request):
    """Only Admins can view this page"""
    if not is_admin(request.user):
        return render(request, "monitoring/access_denied.html")
    
    # Example: show all users and grid data
    return render(request, "monitoring/admin_panel.html", {
        "users": [u.profile for u in request.user.__class__.objects.all()],
        "data": GridData.objects.all()
    })
    
    
    
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created! Please login.")
            return redirect("login")
    return render(request, "monitoring/register.html")








@role_required(['admin', 'operator'])
def inject_attack(request):
    """
    Simple UI to inject synthetic anomalous GridData rows for testing.
    Only 'admin' and 'operator' roles can use this.
    """
    if request.method == "POST":
        # parse form values with safe defaults
        try:
            count = int(request.POST.get('count', 1))
        except ValueError:
            count = 1
        severity = request.POST.get('severity', 'medium')  # low/medium/high

        created = 0
        for _ in range(max(1, min(count, 100))):  # cap at 100 inserts
            # choose voltage/current ranges based on severity
            if severity == 'low':
                voltage = random.uniform(200.0, 230.0)
                current = random.uniform(3.0, 6.0)
            elif severity == 'high':
                voltage = random.uniform(260.0, 320.0)
                current = random.uniform(8.0, 15.0)
            else:  # medium
                voltage = random.uniform(240.0, 260.0)
                current = random.uniform(6.0, 9.0)

            # Insert anomalous record
            GridData.objects.create(
                timestamp=timezone.now(),
                voltage=round(voltage, 2),
                current=round(current, 2),
                anomaly=True
            )
            created += 1

        messages.success(request, f"Injected {created} anomalous record(s) (severity: {severity}).")
        return redirect('dashboard')

    # GET => show small form
    return render(request, 'monitoring/inject_attack.html', {})
