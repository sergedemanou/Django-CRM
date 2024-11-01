from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()
    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, 'You have been logged In.')
            return redirect('home')
        else:
            # No backend authenticated the credentials
            messages.success(request, 'Invalid username or password.')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged Out.')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}. You are now able to log in.')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, f'You must be logged in to view that page...')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, f'Record deleted sucessfully...')
        return redirect('home')
    else:
        messages.success(request, f'You must be logged in to delete that record...')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, f'Record added successfully...')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, f'You must be logged in to add a record...')
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        record_to_update = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f'Record updated successfully...')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, f'You must be logged in to update that record...')
        return redirect('home')