from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
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


class TaskDetailView(DetailView):
    model = Task
    template_name = 'pages/task_detail.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checklists'] = ChecklistItem.objects.filter(task=self.object).all()
        return context


class ChecklistCreateView(CreateView):
    model = ChecklistItem
    fields = ['content']
    template_name = 'pages/checklist_create.html'
    success_url = '/task/'

    def get_success_url(self):
        return self.success_url + str(self.kwargs['task_id']) + '/'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.task = Task.objects.get(id=self.kwargs['task_id'])
        data.save()
        return redirect(self.get_success_url())


class ChecklistUpdateView(UpdateView):
    model = ChecklistItem
    fields = ['checked']
    template_name = 'pages/checklist_update.html'
    success_url = '/task/'
    pk_url_kwarg = 'check_id'

    def get(self, request, *args, **kwargs):
        data = super().get_object()
        data.checked = not data.checked
        data.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('view-task', kwargs={'task_id': str(self.kwargs['task_id'])})
        # return self.success_url + str(self.kwargs['task_id']) + '/' 비슷한 기능


class ChecklistDeleteView(DeleteView):
    model = ChecklistItem
    pk_url_kwarg = 'check_id'
    template_name = 'pages/checklist_delete.html'
    success_url = '/task/'

    def get_success_url(self):
        return reverse('view-task', kwargs={'task_id': str(self.kwargs['task_id'])})


class TaskDeleteView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'pages/task_delete.html'
    success_url = '/'
