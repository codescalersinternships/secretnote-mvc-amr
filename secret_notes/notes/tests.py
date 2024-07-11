from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Note
from datetime import timedelta

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver

class NoteModelTests(TestCase):
    def test_note_expired(self):
        future_date = timezone.now() + timedelta(days=1)
        note = Note(exp_date=future_date, max_views=1)
        self.assertFalse(note.is_expired())
        
        past_date = timezone.now() - timedelta(days=1)
        note = Note(exp_date=past_date, max_views=1)
        self.assertTrue(note.is_expired())
        
class NoteViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_note(self):
        response = self.client.post(reverse('create_note'), {'content': 'New note', 'max_views': 1, 'expiration': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Note created!", response.content.decode())
    
    def test_view_note(self):
        note = Note.objects.create(note_text="New note", max_views=1, exp_date=timezone.now()+timedelta(days=1))
        response = self.client.get(reverse('view_note', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New note")

# class NoteEndToEndTests(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_create_view_note(self):
#         self.selenium.get(self.live_server_url + '/create')

#         self.selenium.find_element_by_name('content').send_keys('New note')
#         self.selenium.find_element_by_name('max_views').send_keys('1')
#         self.selenium.find_element_by_name('expiration').send_keys('1')
#         self.selenium.find_element_by_xpath('//button[contains(text(), "Submit")]').click()

#         self.assertIn("Note created!", self.selenium.page_source)

#         self.selenium.find_element_by_id('id_username').send_keys('testuser')
#         self.selenium.find_element_by_id('id_password').send_keys('testpass123')
#         self.selenium.find_element_by_id('login-button').click()

#         note_url = self.selenium.find_element_by_xpath('//a[contains(@href, "/note/")]')
#         note_url.click()
#         self.assertIn("New note", self.selenium.page_source)