from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Question, Answer
from .forms import QuestionForm, AnswerForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    if request.user.is_authenticated:
        form = QuestionForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, ("Your question has been posted!!!"))
            return redirect('home')

        questions = Question.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"questions":questions, "form":form})

    questions = Question.objects.all().order_by("-created_at")
    return render(request, 'home.html', {"questions":questions})

def fav_questions(request):
    if request.user.is_authenticated:
        form = QuestionForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, ("Your question has been posted!!!"))
            return redirect('home')

        questions = request.user.questions_followed.order_by("-created_at")
        return render(request, 'home.html', {"questions":questions, "form":form})

    questions = Question.objects.all().order_by("-created_at")
    return render(request, 'home.html', {"questions":questions})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    messages.success(request, ("You must be logged in to view this page!!!"))
    return redirect('home')

def fav_profiles(request):
    if request.user.is_authenticated:
        profiles = request.user.profile.follows.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    messages.success(request, ("You must be logged in to view this page!!!"))
    return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        questions = Question.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, "profile.html", {"profile":profile, "questions":questions})
    messages.success(request, ("You must be logged in to view this page!!!"))
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, ("You have been logged in!!!"))
            return redirect('home')
        else:
            messages.success(request, ("Please try again!!!"))
            return redirect('login')

    return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!!!"))
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	return render(request, "register.html", {'form':form})
    
def question_follow(request, pk):
    if request.user.is_authenticated:
        question = get_object_or_404(Question, id=pk)
        if question.followers.filter(id=request.user.id):
            question.followers.remove(request.user)
        else:
            question.followers.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    messages.success(request, ("You must be logged in to perform this action!!!"))
    return redirect('home')
    
def question_info(request, pk):
    if request.user.is_authenticated:
        try:
            question = get_object_or_404(Question, id=pk)
            form = AnswerForm(request.POST or None)
            if request.method == "POST" and form.is_valid():
                answer = form.save(commit=False)
                answer.user = request.user
                answer.question = question
                answer.save()
                messages.success(request, ("Your answer has been posted!!!"))
                return redirect(request.META.get("HTTP_REFERER"))
            answers = Answer.objects.filter(question_id=pk).order_by("-created_at")
            return render(request, "question_info.html", {'question':question,'answers':answers, "form":form})
        except:
            messages.success(request, ("Requested question does not exist!!!"))
            return redirect('home')
    messages.success(request, ("You must be logged in to perform this action!!!"))
    return redirect('home')

def question_delete(request, pk):

    if request.user.is_authenticated:
        try:
            question = get_object_or_404(Question, id=pk)
            if request.user == question.user:
                question.delete()
                messages.success(request, ("Deleted Successfully!!!"))
                return redirect(request.META.get("HTTP_REFERER"))
            messages.success(request, ("Denied Permission!!!"))
            return redirect('home')
        
        except:
            messages.success(request, ("Requested question does not exist!!!"))
            return redirect('home')
    
    messages.success(request, ("You must be logged in to perform this action!!!"))
    return redirect('home')

def answer_like(request, pk):
    if request.user.is_authenticated:
        answer = get_object_or_404(Answer, id=pk)
        if answer.likes.filter(id=request.user.id):
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    messages.success(request, ("You must be logged in to perform this action!!!"))
    return redirect('home')


def answer_delete(request, pk):

    if request.user.is_authenticated:
        try:
            answer = get_object_or_404(Answer, id=pk)
            if request.user == answer.user:
                answer.delete()
                messages.success(request, ("Deleted Successfully!!!"))
                return redirect(request.META.get("HTTP_REFERER"))
            messages.success(request, ("Denied Permission!!!"))
            return redirect('home')
        
        except:
            messages.success(request, ("Requested answer does not exist!!!"))
            return redirect('home')
    
    messages.success(request, ("You must be logged in to perform this action!!!"))
    return redirect('home')
