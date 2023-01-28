from django import forms
from recipes.models import Recipe


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

