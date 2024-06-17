from celery import shared_task
from django.core.mail import send_mail
from .models import Eventos, Usuario
from django.core.cache import cache

@shared_task
def notificacao_email_atualizar_evento(usuario, evento):
    assunto = 'Evento Alterado'
    mensagem = f'Olá {usuario},\n\nO evento em que você se inscreveu foi alterado: {evento.titulo}\n\n Novos Detalhes do Evento:\nData: {evento.data}\nHora: {evento.hora}\nLocalização: {evento.localizacao}\n\nObrigado e aproveite!'
    remetente = 'remetente@gmail.com'
    destinatario = [usuario.email]
    send_mail(assunto, mensagem, remetente, destinatario)

@shared_task
def notificacao_email_inscricao_evento(usuario, evento):
    assunto = 'Inscrição Confirmada'
    mensagem = f'Olá {usuario},\n\nVocê se inscreveu com sucesso no evento {evento.titulo}\n\nDetalhes do Evento:\nData: {evento.data}\nHora: {evento.hora}\nLocalização: {evento.localizacao}\n\nObrigado por se inscrever!'
    remetente = 'remetente@gmail.com'
    destinatario = [usuario]
    send_mail(assunto, mensagem, remetente, destinatario)

@shared_task
def carregar_participantes(evento_id):
    from .serializers import ParticipanteSerializer

    try:
        evento = Eventos.objects.get(id=evento_id)
        participantes = evento.participantes.all()
        participantes_serializers = ParticipanteSerializer(participantes, many=True).data
        cache.set(f'participantes_evento_{evento_id}', participantes_serializers, timeout=3600)
        return participantes_serializers
    except Eventos.DoesNotExist:
        return []