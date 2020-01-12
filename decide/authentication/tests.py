from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from base import mods
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )

#class TestTestprivacypolicy():
#    def setup_method(self, method):
#        self.driver = webdriver.Firefox()
#        self.vars = {}
  
#    def teardown_method(self, method):
#        self.driver.quit()
  
#    def test_testprivacypolicy(self):
#        self.driver.get("http://egc-decide-moltres.herokuapp.com/authentication/"")
#        self.driver.set_window_size(641, 692)
#        self.driver.find_element(By.LINK_TEXT, "Our privacy policy").click()

#class TestLogin():
#    def setup_method(self, method):
#        self.driver = webdriver.Firefox()
#        self.vars = {}
#  
#    def teardown_method(self, method):
#        self.driver.quit()
#  
#    def test_login(self):
#        self.driver.get("http://egc-decide-moltres.herokuapp.com/authentication/")
#        self.driver.set_window_size(641, 696)
#        self.driver.find_element(By.LINK_TEXT, "Login").click()
#        self.driver.find_element(By.ID, "id_username").click()
#        self.driver.find_element(By.ID, "id_username").send_keys("prueba1")
#        self.driver.find_element(By.ID, "id_username").send_keys("prueba1")
#        self.driver.find_element(By.ID, "id_password").send_keys("UnaContraseña1")
#        self.driver.find_element(By.ID, "id_password").send_keys("UnaContraseña1")
#        element = self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)")
#        actions = ActionChains(self.driver)
#        actions.move_to_element(element).click_and_hold().perform()
#        element = self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)")
#        actions = ActionChains(self.driver)
#        actions.move_to_element(element).perform()
#        element = self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)")
#        actions = ActionChains(self.driver)
#        actions.move_to_element(element).release().perform()
#        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
#        self.driver.find_element(By.CSS_SELECTOR, "body").click()
#        self.driver.find_element(By.LINK_TEXT, "Terminar sesión").click()

#class TestLoginCorreo():
#    def setup_method(self, method):
#        self.driver = webdriver.Firefox()
#        self.vars = {}
#  
#    def teardown_method(self, method):
#        self.driver.quit()
#  
#    def test_loginCorreo(self):
#        self.driver.find_element(By.LINK_TEXT, "Login").click()
#        self.driver.find_element(By.ID, "id_username").send_keys("alejandro@gmail.com")
#        self.driver.find_element(By.ID, "id_password").click()
#        self.driver.find_element(By.ID, "id_password").send_keys("UnaContraseña1")
#        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
#        self.driver.find_element(By.CSS_SELECTOR, "html").click()
#        self.driver.find_element(By.LINK_TEXT, "Terminar sesión").click()
#        self.driver.get("http://egc-decide-moltres.herokuapp.com/authentication/")
