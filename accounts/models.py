from django.db import models
from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _


class LoginEmailWidget(forms.Widget):
    email_field = '%s_user'

    def __init__(self, *args, **kwargs):
        super(LoginEmailWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, *args, **kwargs):
        out = ( forms.TextInput().render(self.email_field % name, None) )
	return out

    def value_from_datadict(self, data, files, name):
        email = data.get(self.email_field % name, None)
	if email:
	    return email
	return None

class LoginPasswordWidget(forms.Widget):
    password_field = '%s_pass'

    def __init__(self, *args, **kwargs):
        super(LoginPasswordWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, *args, **kwargs):
        out = ( forms.PasswordInput().render(self.password_field % name, None) )
        return out

    def value_from_datadict(self, data, files, name):
        password = data.get(self.password_field % name, None)
        if password:
	    return password
	return None

class LoginEmailField(forms.Field):
    widget = LoginEmailWidget()
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', _(' '))
	super(LoginEmailField, self).__init__(*args, **kwargs)

    def clean(self, email):
        super(LoginEmailField, self).clean(email)
	return email

class LoginPasswordField(forms.Field):
    widget = LoginPasswordWidget()
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', _(' '))
	super(LoginPasswordField, self).__init__(*args, **kwargs)

	def clean(self, email):
	    super(LoginPasswordField, self).clean(password)
	    return password

class DualPasswordWidget(forms.Widget):
    pass0_field = '%s_pass0'
    pass1_field = '%s_pass1'

    def __init__(self, *args, **kwargs):
        super(DualPasswordWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, *args, **kwargs):
        out = ( forms.PasswordInput().render(self.pass0_field % name, None),
                forms.PasswordInput().render(self.pass1_field % name, None) )
        return '<br />'.join(out)

    def value_from_datadict(self, data, files, name):
        pass0 = data.get(self.pass0_field % name, None)
        pass1 = data.get(self.pass1_field % name, None)
        if pass0 and pass1:
            return (pass0, pass1)
        return None

class DualPasswordField(forms.Field):
    """
    Field used to prevent password typos by asking the same password twice
    and checking if it's the same
    """
    widget = DualPasswordWidget()
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', _('<span class="info">re-enter password.</span>'))
        super(DualPasswordField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(DualPasswordField, self).clean(value)
        if value:
            pass0, pass1 = value
            if pass0 == pass1:
                return pass0
            raise forms.ValidationError(_('Password Missmatch.'))


class SignupForm(forms.Form):
  email = forms.EmailField()
  password = DualPasswordField(label=_(u"password"))
  captcha = CaptchaField(label=_(u"copy text from box into field"))

class LoginForm(forms.Form):
  email = LoginEmailField(label=_(u"Email"))
  password = LoginPasswordField(label=_(u"Password"))
 
class Account(models.Model):
  email = models.EmailField()
  password = models.CharField(max_length=75)
  hash = models.CharField(max_length=27)
  confirmed = models.BooleanField()

  def __unicode__(self):
    return u'%s' % (self.email)
