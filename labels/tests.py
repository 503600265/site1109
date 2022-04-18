from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse
from django.core import mail
from .models import Labeling
from .forms import LabelingForm
from cloudinary.models import CloudinaryField

# Create your tests here.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2

    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

class LogInTest(TestCase):
    # Login User
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('123456789')
        user.save()

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='123456789')
        self.assertTrue(logged_in)

    def test_authentification(self):
        c = Client() #annoying how I have to respecify this
        c.login(username='testuser', password='123456789')
        User = get_user_model()
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        c = Client()
        logged_in = c.login(username='testuser', password='123456789')
        self.assertTrue(logged_in) #making sure logged_in works for logout to also work
        User = get_user_model()
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated) #necessary to test before testing logout
        c.logout()
        self.assertFalse(user.is_anonymous)

class Submission(TestCase):
    #testing object creation
    def createLableing(self, name="test", description="test_desc",publishDate=datetime.now()):
        return Labeling.objects.create(name=name,description=description,publishDate=publishDate)

    #testing if object was created correctly using getters
    def test_creation_and_getters(self):
        test_object = self.createLableing()
        self.assertTrue(isinstance(test_object, Labeling))
        self.assertEqual(test_object.__str__(), test_object.name)
        self.assertEqual(test_object.get_description(), test_object.description)

    #tests validity of this form
    def test_valid_form(self):
        test_object = Labeling.objects.create(name="Test", description="Test_Desc")
        data = {'name':test_object.name, 'description':test_object.description}
        form = LabelingForm(data=data)
        self.assertTrue(form.is_valid())

    #correctly returns false for an invalid form
    def test_invalid_form(self):
        test_object = Labeling.objects.create(name="Test", description="")
        data = {'name': test_object.name, 'description': test_object.description}
        form = LabelingForm(data=data)
        self.assertFalse(form.is_valid())
