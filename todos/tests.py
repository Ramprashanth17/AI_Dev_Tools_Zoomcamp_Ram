from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo
from datetime import date

class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test Description"
        )
    
    def test_todo_creation(self):
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.completed)
        
    def test_todo_str(self):
        self.assertEqual(str(self.todo), "Test TODO")

class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test Description",
            due_date=date.today()
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test TODO")
    
    def test_create_todo(self):
        response = self.client.post(reverse('create_todo'), {
            'title': 'New TODO',
            'description': 'New Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New TODO').exists())
    
    def test_edit_todo(self):
        response = self.client.post(reverse('edit_todo', kwargs={'pk': self.todo.pk}), {
            'title': 'Updated TODO',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated TODO')
    
    def test_delete_todo(self):
        response = self.client.get(reverse('delete_todo', kwargs={'pk': self.todo.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())
    
    def test_toggle_todo(self):
        response = self.client.get(reverse('toggle_todo', kwargs={'pk': self.todo.pk}))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)
