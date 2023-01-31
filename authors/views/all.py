from django.shortcuts import render
from authors.forms import RegisterForm, LoginForm
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import QueryDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm
from authors.decorators import no_login_required
from utils.unique_slug import verify_slug


def register_view(request: HttpRequest) -> HttpResponse:
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(
        request,
        'authors/pages/register_view.html',
        context={'form': form, 'form_action': reverse('authors:create')}
        ) 


def register_create(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()

    POST: QueryDict = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')
        del(request.session['register_form_data']) # noqa
        return redirect(reverse('authors:login_view'))
    return redirect('authors:register')


@no_login_required
def login_view(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {'form': form, 'form_action': reverse('authors:login_create')})  # noqa:E501


def login_create(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        raise Http404()

    url = reverse('authors:login_view')
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        
        if authenticated_user is not None:
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)
            return redirect('authors:dashboard')

        messages.error(request, 'invalid credentials.') 
        return redirect(url)

    messages.error(request, 'Invalid username or password. ')
    return redirect(url)


@login_required(login_url='authors:login_view')
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        messages.error(request, 'Click to logout button')
        return redirect(reverse('authors:login_view'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user.')
        return redirect(reverse('authors:login_view'))

    logout(request)
    messages.success(request, 'Logout successfully.')
    return redirect(reverse('authors:login_view'))


@login_required(login_url='authors:login_view')
def dashboard(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'authors/pages/dashboard.html',
        context={'recipes': recipes}
        )  # noqa:E501


@login_required(login_url='authors:login_view')
def dashboard_recipe_edit(request: HttpRequest, id: int) -> HttpResponse:
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe

    )
    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, 'Your recipe has been successfully saved')
        return redirect(reverse('authors:dashboard_recipe_edit', kwargs={'id': id}))  # noqa
    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={'form': form}

       
        )  # noqa:E501


@login_required(login_url='authors:login_view')
def dashboard_create_recipe(request: HttpRequest) -> HttpResponse:
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Your recipe has been successfully saved')
        return redirect(reverse('authors:dashboard_recipe_edit', kwargs={'id': recipe.id}))  # noqa

    return render(
        request,
        'authors/pages/dashboard_create_recipe.html', 
        context={'form': form}   
    )  # noqa:E501


@login_required(login_url='authors:login_view')
def dashboard_recipe_delete(request: HttpRequest, id: int) -> HttpResponse:
    # code by gustav batista
    match request.method:
        case 'GET':
            raise Http404()

    recipe: Recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    match recipe.author:
        case request.user:
            recipe.delete()
            messages.success(request, 'Your recipe has been successfully deleted')
            return redirect(reverse('authors:dashboard'))
        case _:
            messages.error(request, 'This recipe is not yours.')





