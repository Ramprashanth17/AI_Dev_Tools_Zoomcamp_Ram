from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from django.contrib import messages

def home(request):
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todos/home.html', {'todos': todos})

def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date') or None
        
        Todo.objects.create(
            title=title,
            description=description,
            due_date=due_date
        )
        messages.success(request, 'Todo created successfully!')
        return redirect('home')
    return render(request, 'todos/create.html')

def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.due_date = request.POST.get('due_date') or None
        todo.save()
        messages.success(request, 'Todo updated successfully!')
        return redirect('home')
    return render(request, 'todos/edit.html', {'todo': todo})

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return redirect('home')

def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('home')