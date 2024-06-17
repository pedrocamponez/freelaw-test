from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(null=True, max_length=50)
    sobrenome = models.CharField(null=True, max_length=50)
    email = models.EmailField(null=True, unique=True)
    criado_em = models.DateTimeField(null=True, auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuário'

class Eventos(models.Model):
    titulo = models.CharField(max_length=155)
    descricao = models.TextField()
    data = models.DateField()
    hora = models.TimeField()
    localizacao = models.TextField()
    criado_em = models.DateTimeField(null=True, auto_now_add=True)
    atualizado_em = models.DateTimeField(null=True, auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_autor')
    participantes = models.ManyToManyField(Usuario, blank=True, related_name='eventos_participantes')
    tags = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Eventos"
        verbose_name = "Evento"

    def __str__(self) -> str:
        return self.titulo
    
class Inscricao(models.Model):
    participante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Inscrito"
