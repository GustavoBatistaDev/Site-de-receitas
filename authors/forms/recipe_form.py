from django import forms
from recipes.models import Recipe
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = 'title', 'description',\
                 'preparation_time',\
                 'preparation_time_unit',\
                 'servings', \
                 'servings_unit',\
                 'preparation_steps',\
                 'cover',
        widgets = {
            'cover': forms.FileInput(),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas')
                    )
            ),
            'preparation_time_unit': forms.Select(
                    choices=(
                        ('Minutos', 'Minutos'),
                        ('Horas', 'Horas'),
                        )
            )
           
        }

        title = forms.CharField(
            required=True,
            widget=forms.CharField(),
            error_messages={
                'required': 'eu sou o erro'
            },
       
        )

    def clean(self):
        cd = self.cleaned_data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        elif len(title) < 5:
            self._my_errors['title'].append('Title must be 5 characters or more')  # 

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return cd

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        is_positivo = is_positive_number(preparation_time)
        if not is_positivo:
            self._my_errors['preparation_time'].append('Preparation time must be a number integer')

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        is_positivo = is_positive_number(servings)
        if not is_positivo:
            self._my_errors['servings'].append('servings must be a number integer')

        return servings


            


