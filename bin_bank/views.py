from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.core import serializers

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bin_bank.models import Article, Feedback, MyUser, Transaction
from django.views.decorators.csrf import csrf_exempt
from bin_bank.forms import FeedbackForm, RegisterForm

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('bin_bank:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def homepage(request):
    data_article = Article.objects.all()
    return render(request, 'homepage.html', {'articles':data_article})


def article_detail(request, slug):
    return render(request, "article_detail.html")
    if request.method == "POST":
        if form.is_valid():  # Kondisi data pada field valid
            feedback = Feedback(
                feedback=form.cleaned_data['feedback'],
            )
            feedback.save()  # Menyimpan feedback ke database
            return HttpResponseRedirect(reverse("bin_bank:homepage"))
        else:
            form = FeedbackForm()

def feedback(request):     
    data_feedback = Feedback.objects.all() 
    data_article = Article.objects.all()
    response = {'articles': data_article, 'data_feedback': data_feedback}
    return render(request, 'feedback.html', response )

@csrf_exempt
def get_articles_json(request):
    data_article = Feedback.objects.all()
    return HttpResponse(serializers.serialize('json', data_article), content_type="application/json")

@csrf_exempt
def get_feedback_json(request):
    data_feedback = Article.objects.all()
    return HttpResponse(serializers.serialize('json', data_feedback), content_type="application/json")


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bin_bank:homepaage')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('bin_bank:login')


@login_required(login_url='/login/')
def show_history(request):
    # context = {
    #     'username': request.user.username,
    #     'last_login': request.COOKIES['last_login'],
    # }
    return render(request, "history.html")


@login_required(login_url='/login/')
def update_transaction(request, id):
    transaction_list = Transaction.objects.filter(id=id)
    transaction = transaction_list[0]
    transaction.isFinished = True
    transaction.save()
    return redirect('bin_bank:show_history')


@login_required(login_url='/login/')
def show_transaction_user(request):
    transactions = Transaction.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def show_transaction_user_ongoing(request):
    transactions = Transaction.objects.filter(user=request.user, isFinished=False)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def show_transaction_user_success(request):
    transactions = Transaction.objects.filter(user=request.user, isFinished=True)
    return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")


@login_required(login_url='/login/')
def show_transaction_user_range(request):
    if request.method == "POST":
        # transaction = Transaction(
        #     amountKg = 4,
        #     branchName = "New York"
        # )
        # transaction.save()
        transactions = Transaction.objects.filter(amountKg__range=(request.POST["Min"], request.POST["Max"]))
        return HttpResponse(serializers.serialize("json", transactions), content_type="application/json")
    return HttpResponse("Invalid method", status_code=405)


def deposit_sampah(request):
    return render(request, "deposit_sampah.html")

def show_leaderboard(request):
    user_data = MyUser.objects.all().order_by('-points')
    return HttpResponse(serializers.serialize("json", user_data), content_type="application/json")

def leaderboard(request):
    context = {}
    return render(request, "leaderboard.html", context)