from django.urls import path

from . import views


app_name = 'tarefas'

urlpatterns = [
    path('',views.home_page_view, name='home'),
    path('nova/', views.nova_tarefa_view, name='nova'),
    path('edita/<int:tarefa_id>', views.edita_tarefa_view, name='edita'),
    path('apaga/<int:tarefa_id>', views.apaga_tarefa_view, name='apaga'),
]