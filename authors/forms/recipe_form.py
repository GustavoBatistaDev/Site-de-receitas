from django import forms
from recipes.models import Recipe
from collections import defaultdict


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
            super_clean = super().clean()

