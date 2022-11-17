from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SubmissionForm, CustomerUserCreateForm
from .models import User, Event, Submission
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse


# Create your views here.

def login_page(request):
    """
    function for logging in a user
    """
    page = 'login'

    if request.method == "POST":
        user=authenticate(email=request.POST['email'],
        password = request.POST['password'])

        if user is not None:
            login(request,user)
            return redirect('home')

    context = {'page':page}
    return render(request, 'login_register.html',context)


def register_page(request):
    """
    function for register in a user
    """
    page = 'register'
    form = CustomerUserCreateForm()
    if request.method =='POST':
        form =CustomerUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')


    context = {'page':page,'form':form}


    return render(request, 'login_register.html',context)

def logout_user(request):
    """
    function for logging out of the session
    """
    logout(request )
    return redirect('login')

def home_page(request):
    """
    function for the launch page
    """

    users =  User.objects.filter(hackathon_participant = True)
    events = Event.objects.all()
    context = {'users':users,'events':events}
    return render(request, 'home.html',context)

@login_required()
def event_Page(request, pk):
    """
    function for the event page defination
    """
    
    event = Event.objects.get(id=pk)
    registered = request.user.events.filter(id = event.id).exists()

    submitted =Submission.objects.filter(participant=request.user, event = event).exists()     
    context={'event':event,'registered':registered, "submitted":submitted}
    return render(request, 'event.html',context)

@login_required()
def registration_confirmation(request, pk):
    """
    function for event confirmation and registration
    """

    event = Event.objects.get(id=pk)

    if request.method == "POST":
        event.participant.add(request.user)
        return redirect('event', pk=event.id)
    context = {"event":event}
    return render(request,  'event_confirmation.html',context)

@login_required(login_url='login')
def account_page(request):
    """
    function for the account of the user
    """
    user = request.user

    context = {"user": user}
    return render(request, 'account.html', context)

def user_page(request, pk):
    """
    function for the user
    """

    user = User.objects.get(id=pk)
    context = {'user':user} 
    return render(request, 'profile.html', context)

@login_required()
def project_submission(request, pk):
    """
    function for submission of the projects
    """
    event = Event.objects.get(id=pk)
    form = SubmissionForm()

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():  
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()

            return redirect('account')

    context = {'event':event,'form':form}
    return render(request, 'submit_form.html', context)


def update_submission(request, pk): 
    """
    function for updating
    """
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You cant be here!!')

    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')
 

    context={'form':form,"event":event}

    return render(request, 'submit_form.html', context)