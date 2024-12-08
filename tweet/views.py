from django.shortcuts import render
from .models import tweets , register_user
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request , 'index.html')

def get_user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = register_user.objects.get(user=request.user)  # Fetch the related profile
            return {
                'email': profile.user.email,  # Access email from the User model
                'contact_number': profile.contact_number,  # Access contact number
                'profile_picture': profile.profile_picture,  # Access profile picture
            }
        except register_user.DoesNotExist:
            return {
                'email': request.user.email,  # Fallback to User email if profile doesn't exist
                'contact_number': None,
                'profile_picture': None,
            }
    return None

@login_required
def tweet_list(request):
    customers = get_user_profile(request)  # Fetch customer data for authenticated users

    if request.user.is_authenticated:
        user_tweets_list = tweets.objects.filter(user=request.user).order_by('-created_at')  # Fetch only the logged-in user's tweets
        all_tweets_list = tweets.objects.exclude(user=request.user).order_by('-created_at')
    else:
        user_tweets_list = tweets.objects.none()  # Start with an empty queryset if not authenticated
        all_tweets_list = tweets.objects.all().order_by('-created_at')

    return render(request, 'tweet_list.html', {
        'user_tweets_list': user_tweets_list,
        'all_tweets_list': all_tweets_list,
        'customers': customers,
    })

@login_required
def tweet_create(request):
    if request.method == "POST":
      form = TweetForm(request.POST,request.FILES)
      if form.is_valid():
          
          tweet = form.save(commit = False)
          tweet.user = request.user
          tweet.save()#saving the data in database
          return redirect('tweet_list')
    else: #if user giving an empaty form
        form = TweetForm()
    return render(request , 'tweet_form.html',{'form': form})
    

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(tweets ,pk = tweet_id , user = request.user)
    if request.method  =='POST':
        form = TweetForm(request.POST , request.FILES, instance = tweet)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance = tweet)
    return render(request , 'tweet_form.html',{'form': form})

@login_required
def tweet_delete(request ,tweet_id):
    tweet = get_object_or_404(tweets,pk=tweet_id ,user = request.user)
    if request.method =='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request , 'tweet_confirm_delete.html',{'tweet':tweet})           


# view for the registration of the user
def registration(request):
    if request.method == "POST":
        # taking data from the form
        uname = request.POST['username']
        ucontactno = request.POST['contactno']
        uemail = request.POST['email']
        upassword = request.POST['password']
        uprofile_pic = request.FILES['profile_pic']
        
        # creating a active user using inbuit model
        usr = User.objects.create_user(uname , uemail , upassword)
        usr.save()
        #register table linked with user table
        reg = register_user(user = usr , contact_number =  ucontactno , profile_picture = uprofile_pic)
        reg.save()
        return render(request , "registration/logging.html" , {"status" : "{uname} your are registered successfully "})
    return render(request , 'registration/registeration.html')


def user_login(request):
    if request.method == "POST":
        un = request.POST['username']
        pwd = request.POST['password']

        user = authenticate(username = un , password = pwd)
        if user:
            login(request , user)#inbuilt function for login
            return redirect('tweet_list')
        else:
            return render(request , 'registration/logging.html' ,{"status": "invalid user"})
    
    return render(request , 'registration/logging.html')



def user_logout(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")  # Set a success message
    return redirect('tweet_list')  

