from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Department, User, Ticket

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('manage_tickets')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        department_id = request.POST['department']
        role = request.POST['role']
        department = Department.objects.get(id=department_id)
        user = User.objects.create_user(name=name, email=email, phone_number=phone_number,
                                        password=password, department=department, role=role)
        return redirect('manage_users')
    departments = Department.objects.all()
    return render(request, 'create_user.html', {'departments': departments})

@login_required
def create_department(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        department = Department.objects.create(name=name, description=description)
        return redirect('manage_departments')
    return render(request, 'create_department.html')

@login_required
def manage_tickets(request):
    if request.user.role == 'admin':
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'manage_tickets.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        priority = request.POST['priority']
        user = request.user
        ticket = Ticket.objects.create(subject=subject, body=body, priority=priority, user=user)
        # Code to post ticket to Zendesk API
        return render(request, 'ticket_confirmation.html', {'ticket': ticket})
    return render(request, 'create_ticket.html')
