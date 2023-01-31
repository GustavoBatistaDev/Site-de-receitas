from django.views import View
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm
from authors.decorators import no_login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.forms import ModelForm


@method_decorator(
        login_required(login_url='authors:login'),
        name='dispatch'
        )
class DashBoardRecipeEdit(View):
    def get_recipe(self, id: int) -> Recipe:
        recipe: None = None

        if id:
            recipe: QueryDict = Recipe.objects.filter(  # noqa
                    is_published=False,
                    author=self.request.user,
                    pk=id
                ).first()

            if not recipe:
                raise Http404()
        return recipe
    
    def render_recipe(self, form: ModelForm) -> HttpResponse:
        return render(
                self.request,
                'authors/pages/dashboard_recipe.html',
                context={'form': form}
            )  

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        recipe = self.get_recipe(id)
    
        form: AuthorRecipeForm = AuthorRecipeForm(instance=recipe)
       
        return self.render_recipe(form)
    
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        recipe: QueryDict = self.get_recipe(id)
    
        form: AuthorRecipeForm = AuthorRecipeForm(
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
        
        return self.render_recipe(form)


class DashBoardRecipeCreate(DashBoardRecipeEdit):
    def get(self, request):
        form: AuthorRecipeForm = AuthorRecipeForm()
        return self.render_recipe(form=form)  # noqa

    def post(self, request):
        form: AuthorRecipeForm = AuthorRecipeForm(
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
        return self.render_recipe(form)
    

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(View):
    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        recipe.delete()
        messages.success(request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))