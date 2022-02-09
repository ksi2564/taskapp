from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from .models import Task, ChecklistItem
from django.utils import timezone
from django.core.paginator import Paginator


# Create your views here.


def index(request):
    context = {}
    return render(request, 'pages/index.html', context)


class TaskListView(TemplateView):
    template_name = 'pages/task_list.html'

    def get_context_data(self, **kwargs):
        tasks = Task.objects.filter(due__gte=timezone.now()).order_by('due').all()
        paginator = Paginator(tasks, 4)
        page_number = self.request.GET.get('page', '1')
        paging = paginator.get_page(page_number)

        return {
            'paging': paging
        }


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'type', 'due']
    template_name = 'pages/task_create.html'
    success_url = '/'


class TaskPreviousListView(ListView):
    model = Task
    template_name = 'pages/task_previous_list.html'
    queryset = Task.objects.filter(due__lt=timezone.now()).order_by('due')
    paginate_by = 4
