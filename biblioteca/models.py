from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome


class Biblioteca(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    ano_livro = models.IntegerField(blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    dono_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'biblioteca'

    def __str__(self):
        return f"Título: {self.titulo}, Autor: {self.autor}, Ano: {self.ano_livro}, Categoria: {self.categoria}"



