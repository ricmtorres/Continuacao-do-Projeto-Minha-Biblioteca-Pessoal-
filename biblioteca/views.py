import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Biblioteca


def registro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        senha_encode = senha.encode('utf-8')
        sha256_hash = hashlib.sha256()
        sha256_hash.update(senha_encode)
        senha_cripto = sha256_hash.hexdigest()
        Usuario.objects.create(nome=nome, senha=senha_cripto)
    return render(request, 'biblioteca/registro.html')


def login(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        senha_encode = senha.encode('utf-8')
        sha256_hash = hashlib.sha256()
        sha256_hash.update(senha_encode)
        senha_cripto = sha256_hash.hexdigest()
        try:
            usuario = Usuario.objects.get(nome=nome, senha=senha_cripto)
            request.session['usuario_id'] = usuario.id
            return redirect('personalizar')
        except Usuario.DoesNotExist:
            return HttpResponse("Nome ou senha inválido")
    return render(request, 'biblioteca/login.html')


def personalizar(request):
    if request.method == 'POST':
        cor_favorita = request.POST.get('cor_favorita')
        request.session['cor_favorita'] = cor_favorita
        response = redirect('dashboard')
        response.set_cookie('cor_favorita', cor_favorita, max_age=3600)
        return response
    return render(request, 'biblioteca/personalizar.html')


def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    livros = Biblioteca.objects.filter(dono_id=usuario_id)
    lista = list(livros)
    usuario = Usuario.objects.get(id=usuario_id)
    cor_favorita = request.COOKIES.get('cor_favorita', 'default')
    return render(request, 'biblioteca/dashboard.html',
                  {'usuario': usuario, 'cor_favorita': cor_favorita, 'lista': lista})


def adicionar_livro(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    cor_favorita = request.COOKIES.get('cor_favorita', 'default')

    if not usuario_id:
        return redirect('login')
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        ano_livro = request.POST.get('ano_livro')
        categoria = request.POST.get('categoria')
        Biblioteca.objects.create(titulo=titulo, autor=autor, ano_livro=ano_livro, categoria=categoria, dono_id=usuario)
    return render(request, 'biblioteca/adicionar_livro.html', {'usuario': usuario, 'cor_favorita': cor_favorita})


def logout(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('cor_favorita')
    return response


def buscar(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id)
    cor_favorita = request.COOKIES.get('cor_favorita')
    lista = []
    if not usuario_id:
        return redirect('login')
    if request.method == 'POST':
        criterio_busca = request.POST.get('criterio_busca')
        busca = request.POST.get('busca')
        if criterio_busca == "titulo":
            resultados = Biblioteca.objects.filter(titulo__icontains=busca, dono_id=usuario_id)
        elif criterio_busca == "autor":
            resultados = Biblioteca.objects.filter(autor__icontains=busca, dono_id=usuario_id)
        elif criterio_busca == "ano_livro":
            resultados = Biblioteca.objects.filter(ano_livro__icontains=busca, dono_id=usuario_id)
        elif criterio_busca == "categoria":
            resultados = Biblioteca.objects.filter(categoria__icontains=busca, dono_id=usuario_id)

        for resposta in resultados:
            titulo = resposta.titulo
            autor = resposta.autor
            ano_livro = resposta.ano_livro
            categoria = resposta.categoria
            item = f"Titulo: {titulo}, Autor: {autor}, Ano: {ano_livro}, Categoria: {categoria}"
            lista.append(item)
    return render(request, 'biblioteca/buscar.html',
                  {'usuario': usuario, 'cor_favorita': cor_favorita, 'lista': lista})


def exibir(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    cor_favorita = request.COOKIES.get('cor_favorita')
    lista = []
    if request.method == 'POST':
        criterio_busca = request.POST.get('criterio_busca')
        livros_ordenados = Biblioteca.objects.order_by(criterio_busca)
        for livro in livros_ordenados:
            if livro.dono_id_id == usuario_id:
                lista.append(livro)
    return render(request, 'biblioteca/exibir.html',
                  {'usuario': usuario, 'cor_favorita': cor_favorita, 'livros_ordenados': lista})
