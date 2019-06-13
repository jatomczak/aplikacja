from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UsernameField
from .models import User

EMPTY_ELEMENT = "Pole %s nie może być puste"

class RegisterForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': "Hasła nie są identyczne",
    }

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
                    'placeholder':'Podaj haslo',}))
    password2 = forms.CharField(label='Potwierdź hasło', widget =forms.PasswordInput(attrs={
                    'placeholder':'Potwierdź haslo',}))

    class Meta:
        model = User
        fields = ('email','name', 'surname', 'user_id', 'group')
        widgets = {
                'email': forms.fields.EmailInput(attrs={
                    'placeholder':'wpisz adres email',}),
                'name': forms.fields.TextInput (attrs={
                    'placeholder': 'wpisz imię',}),
                'surname': forms.fields.TextInput(attrs={
                    'placeholder':'wpisz nazwisko',}),
                'user_id': forms.fields.TextInput(attrs={
                    'placeholder':'wpisz id użytkownika',}),
        }
        error_messages = {
            'email': {'required' : EMPTY_ELEMENT%'adres email',}
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email jest zajęty.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są identyczne")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(
        label=("Hasło"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder':'wpisz hasło'
        }),
    )
    error_messages = {
        'invalid_login': ('Wprowadż poprawne hasło. Wielkośc liter może mieć znaczenie.'),
        'inactive': ("Twoje konto jest nieaktywne."),
    }
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'wpisz adres email'}))