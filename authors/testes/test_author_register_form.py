from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Your password'),
        ('password2', 'Your password again'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        atual_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(atual_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'Endereço de email'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_label_is_correct(self, field, label):
        form = RegisterForm()
        atual_label = form[field].field.label
        self.assertEqual(atual_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'userr',
            'first_name': 'Gustavo',
            'last_name': 'Batista',
            'email': 'gustavobatistadev@gmail.com.br.nns',
            'password': '82077877Ab',
            'password2': '82077877Ab'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'O campo Username é obrigatório.'),
        ('first_name', 'O campo First Name é obrigatório.'),
        ('last_name', 'O campo Last Name é obrigatório.'),
        ('email', 'O campo Email é obrigatório.'),
        ('password2', 'Check the two password fields.'),
        ('password', 'Check the two password fields, please.')

        
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        self.assertIn(msg, response.content.decode('utf-8'))
    
    def test_username_field_test_min_length(self):
        self.form_data['username'] = 'gus'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'Username must be 4 to 150 characters long.'  # noqa
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_max_length(self):
        self.form_data['username'] = 'g'*151
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'Username must be 4 to 150 characters long.'  # noqa
        self.assertIn(msg, response.content.decode('utf-8'))

    # implementar teste se o usuário é cadastrado se o form for valido
    def test_whether_the_data_sent_correctly_will_be_saved(self):
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )

        msg = 'Your user is created, please log in.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_passoword_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = '82077877'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )

        msg = 'Password must be 8 characters long, including uppercase and lowercase letters.'  # noqa
        self.assertIn(msg, response.content.decode('utf-8'))
        
        self.form_data['password'] = '82077877Ab'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'Password must be 8 characters long, including uppercase and lowercase letters.'  # noqa
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_password_field_and_password2_are_equal(self):
        self.form_data['password'] = '82077877Ab'
        self.form_data['password2'] = '82077877Ab2'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'Password and password2 do not match'  # noqa
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '82077877Ab'
        self.form_data['password2'] = '82077877Ab'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_if_the_request_get_return_404(self):
        response = self.client.get('authors:create')
        self.assertEqual(404, response.status_code)

    def test_email_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)  
        self.assertIn('User email is already in use.', response.content.decode('utf-8'))  # noqa

    def test_author_created_can_login(self):
        url = reverse('authors:create')
        self.form_data.update({
            "username": "testuser",
            'password': '82077877Ab',
            'password2': '82077877Ab'
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='82077877Ab'
        )

        self.assertTrue(
            is_authenticated
        )