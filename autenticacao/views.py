
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .utils import password_is_valid, email_html
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
# Import EMAILS
import os
from django.conf import settings
# Impor Models
from .models import Ativacao
from hashlib import sha256  #Token


def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated: #Autenticacao do usuario
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')
        # return HttpResponse(f"{usuario} e {email}")
        
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=senha,
                                            is_active=False)
            user.save()

            #Crinado tocken
            token = sha256(f"{username}{email}".encode()).hexdigest()   #concatenacao com usue/pass e convertendo em binario e Convertendo a stringo en exadecimail
            ativacao = Ativacao(token=token, user=user) # tokem é de qual usuario? 
            ativacao.save()

            # Funcao para o envio de Email
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            # email_html(path_template, 'Cadastro confirmado', [email,], username=username)
            email_html(path_template, 'Cadastro confirmado', [email,], username=username, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")

            # Criando um tokem para ativar a conta de email

            # MSG sucesso
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')

        # return HttpResponse(' testando confirmar_senha')
    # return HttpResponse("Ops! estou dentro da página de cadastro")
    # return render(request, 'cadastro.html')

    # LOGIN
# def logar(request):
    # return HttpResponse("Ops! estou dentro da página de LOGAR")
    # return render(request, 'login.html')
def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated: #Autenticacao do usuario
            return redirect('/')
        return render(request, 'logar.html')
        
    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)
        # return HttpResponse(f"{usuario}")

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username  ssssssssssss ou senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            # return redirect('/')
            return redirect('/pacientes')



def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')


# Ativando a conta
# def ativar_conta(request, token):
#     return HttpResponse(token)
def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/logar')
    
    
    user = User.objects.get(username=token.user.username)
    # print(user) Pegando o usuario deste token
   
    # return HttpResponse('Teste')
    
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/logar')