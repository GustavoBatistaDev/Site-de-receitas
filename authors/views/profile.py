from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from authors.models import Profile
from django.shortcuts import render, redirect


def profile_view(request, id: int):
    template_name = 'authors/pages/profile.html'
    profile = get_object_or_404(Profile, pk=id)
    return render(
        request,
        template_name=template_name,
        context={
   
            'author': profile.author.username,
            'bio': profile.bio
        }
        )

