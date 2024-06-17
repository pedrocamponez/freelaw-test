from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.ListaEventos.as_view(), name='listar-eventos'),
    path(r'<int:pk>', views.AtualizarEvento.as_view(), name='atualizar-evento'),
    path(r'usuario/perfil/', views.GetInfoUsuario.as_view(), name='usuario-perfil'),
    path(r'usuario/registrar/', views.UsuarioRegistrarView.as_view(), name='criar-usuario'),
    path(r'<int:pk>/inscrever', views.Inscrever.as_view(), name='inscrever-evento'),
    path(r'<int:pk>/participantes', views.Inscrever.as_view(), name='participantes-eventos'),
    path(r'<int:pk>/delete', views.EventoDestroy.as_view(), name='deletar-evento'),
]
