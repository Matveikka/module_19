from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import Buyer, Game, News


# Create your views here.
def platform(request):
    return render(request, 'fourth_task/platform.html')


def games(request):
    games = Game.objects.all()
    context = {'games': games}
    return render(request, 'fourth_task/games.html', context)


def cart(request):
    title = 'Cart'
    context = {
        'title': title,
    }
    return render(request, 'fourth_task/cart.html', context)


def sign_up_by_html(request):
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))

        buyers = Buyer.objects.values_list('name', flat=True)

        if password != repeat_password:
            info['error'] = "Пароли не совпадают"
            return HttpResponse('Пароли не совпадают')
        elif age < 18:
            info['error'] = "Вы должны быть старше 18"
            return HttpResponse('Вы должны быть старше 18')
        elif username in buyers:
            info['error'] = "Пользователь уже существует"
            return HttpResponse('Пользователь уже существует')
        else:
            Buyer.objects.create(name=username, age=age, balance=1000)
            info['welcome_message'] = f"Приветствуем, {username}!"

        return HttpResponse(f"Приветствуем, {username}!")

    return render(request, 'registration_page.html', context=info)


def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            buyers = Buyer.objects.values_list('name', flat=True)
            if password != repeat_password:
                info['error'] = "Пароли не совпадают"
                return HttpResponse('Пароли не совпадают')
            elif age < 18:
                info['error'] = "Вы должны быть старше 18"
                return HttpResponse('Вы должны быть старше 18')
            elif username in buyers:
                info['error'] = "Пользователь уже существует"
                return HttpResponse('Пользователь уже существует')
            else:
                Buyer.objects.create(name=username, age=age, balance=1000)
                info['welcome_message'] = f"Приветствуем, {username}!"
            return HttpResponse(f"Приветствуем, {username}!")
    else:
        form = UserRegister()
        info['message'] = form

    return render(request, 'registration_page.html', info)


def news(request):
    news_list = News.objects.all().order_by('-created_at')
    paginator = Paginator(news_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'news': page_obj})
