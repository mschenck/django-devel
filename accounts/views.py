from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django import forms
from base64 import urlsafe_b64encode, urlsafe_b64decode

from captcha.fields import CaptchaField
from accounts.models import Account, SignupForm, LoginForm

################################################################################
# Hash code
################################################################################
def uri_b64encode(s):
     return urlsafe_b64encode(s).strip('=')

def uri_b64decode(s):
     return urlsafe_b64decode(s + '=' * (4 - len(s) % 4))


################################################################################
# Login functions
################################################################################
def loggedIn(request):
    login_status = 0 
    message = ""

    try:
      sess_hash = request.session['hash_id']
    except:
      sess_hash = None

    if sess_hash != None:
      try:
        account = Account.objects.get(hash__iexact=sess_hash)
      except:
        account = None

      if account != None:
        message = "Logged in (" + account.email + ")"
        login_status = 1
      else:
        login_status = 0
    else:
      login_status = 0
    
    return (login_status, message)


################################################################################
# Views
################################################################################
def index(request):
  status, message = loggedIn(request)
  if status == 1:
    return render_to_response('accounts/index.html')
  else:
    return signup(request)

def confirmation(request):
  return render_to_response('accounts/confirmation.html')

def confirmed(request,message):
  return render_to_response('accounts/confirmed.html', {
    'confirm_message': message,
  })

def exists(request):
  return render_to_response('accounts/exists.html')


########################################
# Sign-up view
########################################
def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      new_email = form.cleaned_data['email']
      new_password = form.cleaned_data['password']
      new_hash=uri_b64encode(new_email)

      # Check that e-mail is unique
      try:
        email_check = Account.objects.get(email__iexact=new_email)
      except Account.DoesNotExist:
        email_check = None 

      if email_check:
        return HttpResponseRedirect('/accounts/exists.html')

      else:
        # Create unconfirmed account
        account		= Account(
  	  email		= new_email,
	  password	= new_password,
	  hash		= new_hash,
	  confirmed	= False
        )
        account.save()

        # Send confirmation e-mail
        msg = "Confirmation message\nClick here to confirm your account: localhost:8000/accounts/confirm/"+new_hash
        send_mail('AzureJay account confirmation', 
	  msg, 
	  'AzureJay <no-reply@azurejay.com>',
	  [ form.cleaned_data['email'] ],
	  fail_silently=False
        )
        return HttpResponseRedirect('/accounts/confirmation.html')

  else:
    form = SignupForm()

  return render_to_response('accounts/signup.html', {
    'form': form,
  })



########################################
# Login view
########################################
def login(request):
  logged_in = 0

  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']

      try:
	account = Account.objects.get(email__iexact=email)
      except Account.DoesNotExist:
        error = "That account does not exist, please sign-up."
	return render_to_response('accounts/login.html', { 'form': form, 'error': error, 'logged_in': logged_in, })

      if account.password == password:
	request.session['hash_id'] = account.hash
	results = "Login successful."
	loginStatus, login_message = loggedIn(request)
	form = login_message
	logged_in = loginStatus
	return render_to_response('accounts/login.html', { 'form': form, 'results': results, 'logged_in': logged_in, })
      else:
        error = "Password incorrect."
	return render_to_response('accounts/login.html', { 'form': form, 'error': error, 'logged_in': logged_in, })

  else:
    loginStatus, login_message = loggedIn(request)
    if loginStatus == 1:
      form = login_message
      logged_in = 1
    else:
      form = LoginForm()

  return render_to_response('accounts/login.html', {
    'form': form,
    'logged_in': logged_in,
  })

########################################
# Logout view
########################################
def logout(request):
  try:
    del request.session['hash_id']
  except:
    pass
  return HttpResponseRedirect('/accounts/login.html')

########################################
# Confirm view
########################################
def confirm(request, hash):
  message = ""

  try:
    account = Account.objects.get(hash__exact=hash)
  except Account.DoesNotExist:
    account = None 

  if account:
    if account.confirmed == True:
      message = "Account has already been confirmed"

    else: 
      message = "Account is now confirmed, log in and start sending e-mail"
      account.confirmed = True
      account.save()
  else:
    message = "Account does not exist, please signup again"

  return confirmed(request, message)

