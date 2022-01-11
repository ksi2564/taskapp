from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Task, ChecklistItem

# Create your views here.


def index(request):
    context = {}
    return render(request, 'pages/index.html', context)


class TaskListView(TemplateView):
    template_name = 'pages/task_list.html'

    def get_context_data(self, **kwargs):
        tasks = Task.objects.all()
        return {
            'tasks': tasks
        }