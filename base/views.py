from .models import Usuario, Eventos, Inscricao
from rest_framework.response import Response
from .serializers import UsuarioSerializer, PerfilUsuarioSerializer, GetEventosSerializer, InscricaoSerializer
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from .tasks import notificacao_email_atualizar_evento, notificacao_email_inscricao_evento

class UsuarioRegistrarView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]

class GetInfoUsuario(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ListaEventos(generics.ListCreateAPIView):
    queryset = Eventos.objects.all().order_by('-id')
    serializer_class = GetEventosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class AtualizarEvento(generics.RetrieveUpdateAPIView):
    serializer_class = GetEventosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs['pk']
        return Eventos.objects.filter(pk=id)
    
    def put(self, request, *args, **kwargs):
        evento = self.get_queryset()
        objeto_evento = self.get_object()

        participantes = objeto_evento.participantes.all()

        emails_participantes = [participante.email for participante in participantes]

        if evento.exists() and evento.first().autor != request.user:
            raise ValidationError('Somente o autor do evento pode alterá-lo.')
        # self.update(request, *args, **kwargs)

        response = super().put(request, *args, **kwargs)

        for email in emails_participantes:
            notificacao_email_atualizar_evento.delay(email, evento)

        return response
        
    def perform_update(self, serializer):
        serializer.save()

    # def notificacao_email(self, usuario, evento):
    #     objeto_evento = self.get_object()

    #     assunto = 'Evento Alterado'
    #     mensagem = f'Olá {usuario},\n\nO evento em que você se inscreveu foi alterado: {objeto_evento.titulo}\n\n Novos Detalhes do Evento:\nData: {objeto_evento.data}\nHora: {objeto_evento.hora}\nLocalização: {objeto_evento.localizacao}\n\nObrigado e aproveite!'
    #     remetente = 'remetente@gmail.com'
    #     destinatario = [usuario]

    #     notificacao_email_inscricao_evento.delay(assunto, mensagem, remetente, destinatario)
        
class Inscrever(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = InscricaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        evento = Eventos.objects.get(pk=self.kwargs['pk'])
        return Inscricao.objects.filter(participante=usuario, evento=evento)
    
    def perform_create(self, serializer):
        usuario = self.request.user
        evento = Eventos.objects.get(pk=self.kwargs['pk'])
        if self.get_queryset().exists():
            raise ValidationError('Você já está inscrito neste evento')
        serializer.save(participante=usuario, evento=evento)
        usuario_serializado = UsuarioSerializer(usuario).data
        evento_serializado = GetEventosSerializer(evento).data
        notificacao_email_inscricao_evento.delay(usuario_serializado, evento_serializado)

    def desinscrever(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Não há o que deletar - vazio')
        
    # def notificacao_email(self, usuario, evento):
    #     assunto = 'Inscrição Confirmada'
    #     mensagem = f'Olá {usuario.nome},\n\nVocê se inscreveu com sucesso no evento {evento.titulo}\n\nDetalhes do Evento:\nData: {evento.data}\nHora: {evento.hora}\nLocalização: {evento.localizacao}\n\nObrigado por se inscrever!'
    #     remetente = 'remetente@gmail.com'
    #     destinatario = [usuario.email]
    #     notificacao_email_inscricao_evento.delay(assunto, mensagem, remetente, destinatario)
        
class EventoDestroy(generics.RetrieveDestroyAPIView):
    queryset = Eventos.objects.all()
    serializer_class = GetEventosSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        evento = Eventos.objects.filter(pk=kwargs['pk'], autor=self.request.user)
        if evento.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Somente o autor do evento pode deletá-lo')