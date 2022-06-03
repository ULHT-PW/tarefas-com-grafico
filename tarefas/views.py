from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import Tarefa
from .forms import TarefaForm

# imports para imprimir grafico
from matplotlib import pyplot as plt
import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')


# Create your views here.

def cria_grafico():
    tarefas = Tarefa.objects.all().order_by('prioridade')

    titulos = [tarefa.titulo for tarefa in tarefas]
    prioridades = [tarefa.prioridade for tarefa in tarefas]

    plt.barh(titulos, prioridades)
    plt.ylabel("Prioridade")
    plt.autoscale()

    fig = plt.gcf()
    plt.close()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')


    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri



def home_page_view(request):

    context = {
        'tarefas': Tarefa.objects.all(),
        'data':cria_grafico()
    }
    return render(request, 'tarefas/home.html', context)


def nova_tarefa_view(request):
    form = TarefaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('tarefas:home'))

    context = {'form': form}

    return render(request, 'tarefas/nova.html', context)


def edita_tarefa_view(request, tarefa_id):
    tarefa = Tarefa.objects.get(id=tarefa_id)
    form = TarefaForm(request.POST or None, instance=tarefa)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('tarefas:home'))

    context = {'form': form, 'tarefa_id': tarefa_id}
    return render(request, 'tarefas/edita.html', context)


def apaga_tarefa_view(request, tarefa_id):
    Tarefa.objects.get(id=tarefa_id).delete()
    return HttpResponseRedirect(reverse('tarefas:home'))