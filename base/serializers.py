from datetime import datetime
from rest_framework import serializers
from .models import Usuario, Inscricao, Eventos
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nome', 'sobrenome', 'email', 'criado_em', 'senha']
        read_only_fields = ['senha', 'criado_em']

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    eventos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        fields = ['nome', 'sobrenome', 'email', 'criado_em', 'eventos']
    
    def get_eventos(self, obj):
        return Eventos.objects.filter(autor_id=obj.id).values_list('titulo', flat=True)

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'email']
    
class GetEventosSerializer(serializers.ModelSerializer):
    autor = serializers.ReadOnlyField(source='autor.email')
    id_autor = serializers.ReadOnlyField(source='autor.id')
    inscritos = serializers.SerializerMethodField(read_only=True)
    participantes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Eventos
        fields = ['id', 'titulo', 'criado_em', 'descricao', 'autor', 'id_autor', 'data', 'hora', 'localizacao', 'atualizado_em', 'inscritos', 'participantes']

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.data = validated_data.get('data', instance.data)
        instance.hora = validated_data.get('hora', instance.hora)
        instance.localizacao = validated_data.get('localizacao', instance.localizacao)
        instance.atualizado_em = datetime.now()
        instance.save()
        return instance
    
    def get_inscritos(self, evento):
        return Inscricao.objects.filter(evento=evento).count()
    
    def get_participantes(self, evento):
        # logger.debug(f'Pegando os participantes do evento ID: {evento.id}')

        participantes = evento.participantes.all()
        # participantes = cache.get(f'participantes_evento_{evento.id}')
        # if not participantes:
        #     logger.debug(f'Chamando a task do Celery')
        #     from .tasks import carregar_participantes
        #     carregar_participantes.delay(evento.id)
        #     return 'Carregando participantes...'
        return ParticipanteSerializer(participantes, many=True).data
        # logger.debug(f'Cache encontrado para o evento ID: {evento.id}')
        # return participantes
    
class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = ['participante', 'evento']