from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, EventForm, DonationForm
from .models import BlogPost, Event, Donation, User
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    search_query = request.GET.get('search_query', '')
    blog_section = BlogPost.objects.all()
    event_section = Event.objects.all()
    user_participation = {}
    if request.user.is_authenticated:
        user_participation = {
            event.id: True for event in Event.objects.filter(participants=request.user)
        }
    if search_query:
        blog_section = blog_section.filter(
            Q(title__icontains=search_query)
        )
        event_section = event_section.filter(
            Q(name__icontains=search_query)
        )
    context = {
        'blog_section': blog_section,
        'event_section': event_section,
        'search_query': search_query,
        'user_participation': user_participation,
    }
    return render(request, 'post/home.html', context)


@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user_donations = Donation.objects.filter(user=request.user)
    joined_events = Event.objects.filter(participants=request.user) 
    return render(request, 'post/dashboard.html', {
        'dashboard': {'donations': user_donations},
        'joined_events': joined_events,
    })


@login_required
def blogpost(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid:
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm
    return render(request, 'post/blog.html',{'form':form})

@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid:
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'post/blog.html', {'form':form})

@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'post/delete.html', {'blog':blog})



@login_required
def donate(request, blog_id):
    blog_post = get_object_or_404(BlogPost, pk=blog_id)
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.blog_post = blog_post
            donation.save()
            return redirect('home')
    else:
        form = DonationForm()

    return render(request, 'post/donate.html', {
        'form': form, 
        'blog_post': blog_post,
        })

@login_required
def approve_donations(request):
    pending_donations = Donation.objects.filter(status='Pending')
    user_donations = Donation.objects.filter(status__in=['Approved', 'Rejected'])
    if request.method == "POST":
        donation_id = request.POST.get('donation_id')
        action = request.POST.get('action')
        
        donation = get_object_or_404(Donation, id=donation_id)
        
        if action == "approve":
            donation.status = 'Approved'
        elif action == "reject":
            donation.status = 'Rejected'
        
        donation.approver = request.user
        donation.save()
        
        return redirect('approve_donations')

    return render(request, 'post/approve_donations.html', {
        'dashboard': {'donations': user_donations},
        'pending_donations': pending_donations
        })



@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid:
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'post/event.html', {'form': form})


@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id, organizer=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event.save()
            return redirect('home')  
    else:
        form = EventForm(instance=event)
    return render(request, 'post/event.html', {'form': form})


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id, organizer=request.user) 
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'post/delete.html', {'event': event})


@login_required
def event_participants(request):
    events = Event.objects.all()
    return render(request, 'post/participants.html', {'events': events})

@login_required
def remove_participant(request, event_id, participant_id):
    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(User, id=participant_id)
    event.participants.remove(participant)
    return redirect('event_participants')

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
    else:
        event.participants.add(request.user)
    return redirect('home')  

@login_required
def freeze_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user.is_superuser :  
        event.is_frozen = not event.is_frozen
        event.save()
    return redirect('home')
