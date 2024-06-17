from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Usuario, Eventos
from .serializers import UsuarioSerializer, GetEventosSerializer


class TestUsuarioRegistrarView(APITestCase):
  def test_create_user(self):
    url = reverse('criar-usuario')
    data = {
      'nome': 'Usuario Teste',
      'sobrenome': 'Testador',
      'email': 'usuarioteste@testando.com',
      'senha': '123456',
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['nome'], data['nome'])
    self.assertEqual(response.data['sobrenome'], data['sobrenome'])
    self.assertEqual(response.data['email'], data['email'])

    created_user = Usuario.objects.get(email=data['email'])
    self.assertEqual(created_user.nome, data['nome'])
    self.assertEqual(created_user.sobrenome, data['sobrenome'])
    self.assertEqual(created_user.email, data['email'])

class TestListaEventos(APITestCase):
  def setUp(self):
    self.user = Usuario.objects.create_user(username='testuser', password='testpassword')
    self.client.force_authenticate(user=self.user)

  def test_create_evento(self):
    url = reverse('listar-eventos')
    data = {
      'titulo': 'Evento de Teste',
      'descricao': 'Descrição do evento de teste',
      'data': '2024-06-20',
      'hora': '10:00:00',
      'localizacao': 'Local do evento de teste',
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['titulo'], data['titulo'])

class TestInscrever(APITestCase):
  def setUp(self):
    self.user = Usuario.objects.create_user(username='testuser', password='testpassword')
    self.client.force_authenticate(user=self.user)

    self.evento = Eventos.objects.create(titulo="Test Evento", descricao="Descrição Teste", data='2024-06-20', hora='10:00:00', localizacao='Local Teste', autor_id=self.user.id)

  def test_subscribe_success(self):
    url = reverse('inscrever-evento', kwargs={'pk': self.evento.pk})
    response = self.client.post(url)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_subscribe_duplicate(self):
    url = reverse('inscrever-evento', kwargs={'pk': self.evento.pk})
    self.client.post(url)

    response = self.client.post(url)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('Você já está inscrito neste evento', str(response.content))


