from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_placeholder(field, placeholder_val: str):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            "Password must be 8 characters long, including uppercase and lowercase letters." # noqa E:501 
        ))
        

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Your password again')

    username = forms.CharField(
            required=True,
            widget=forms.TextInput(),
            error_messages={
                'required': 'O campo Username é obrigatório.',
                'min_length': 'Username must be 4 to 150 characters long.',
                'max_length': 'Username must be 4 to 150 characters long.'
            },
            label='Username',
            min_length=4,
            max_length=150
        )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Check the two password fields, please.'
        },
        label='Password',
       
        validators=[strong_password]
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Check the two password fields.'
        },
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(),
        label='First Name',
        error_messages={
            'required': 'O campo First Name é obrigatório.'
        },
    )

    email = forms.EmailField(
        required=True,
        label='Endereço de email',
        error_messages={
            'required': 'O campo Email é obrigatório.'
        },
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(),
        label='Last Name',
        error_messages={
            'required': 'O campo Last Name é obrigatório.'
        },
    )
    
    class Meta:
        model = User
        fields = [
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'password'
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        
    # esse metodo valida apenas um campo... a sintaxe 'e: clean + nome_do_campo
    # este metodo 'e so de exemplo
    def clean_password(self) -> str:
        data: str = self.cleaned_data.get('password')
        if 'atencao' in data:
            raise ValidationError('Nao digite "atencao"', code='invalid')

        return data

    # este metodo valida campos que precisam de outro
    def clean(self) -> None:
        data = super().clean()
        password: str = data.get('password')
        password2: str = data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and password2 do not match',
                'password2': 'Password and password2 do not match'
            })

        else:
            return None

    def clean_email(self) -> str:
        email: str = self.cleaned_data.get('email', '')
        exists: bool = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User email is already in use.',
                code='invalid'
            )

        return email
