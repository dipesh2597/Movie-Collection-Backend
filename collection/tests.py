from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import json
from collection.models import Collection,RequestCounter

class RegisterUserTest(TestCase):

    def test(self):
        request = self.client.post('/register/', {'username':'test', 'password':'test@credy'})
        user = get_user_model().objects.get(username='test')
        token = Token.objects.get(user=user)
        self.assertEqual(token.key,request.data['access_token'], f"User Registered and user's token is: {token.key}")

class GetMoviesTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)

    def test(self):
        request = self.client.get('/movies/',HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(request.status_code,200,"request failed")
        self.assertEqual(len(request.data['data']),10,"Giving list of not equal 10 movies")

class GetCollectionUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)
        self.collection = Collection.objects.create(title="test collection",description='test description',user=self.user)

    def test(self):
        request = self.client.get(f'/collection/',HTTP_AUTHORIZATION=self.auth)
        individual_request = self.client.get(f'/collection/{self.collection.uuid}/',HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(request.status_code,200,"request failed")
        self.assertEqual(individual_request.status_code,200,"request failed")
        

class CreatingCollectionUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)

    def test(self):
        collection_data = {
            "title":"My Collection - 3",
            "description":"Third COllection",
            "movies":[
                {
                    "title": "test-movie",
                    "description": "test-description",
                    "genres": "action,Thriller"
                    },
                ]
            }
        request = self.client.post('/collection/', json.dumps(collection_data),content_type="application/json",HTTP_AUTHORIZATION=self.auth)
        try:
            uuid = request.data['collection_uuid']
            self.assertTrue(True)
        except:
            self.assertTrue(False,"No UUID found for collection")
        self.assertEqual(request.status_code,201,"request failed")


class UpdatingCollectionUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)
        self.collection = Collection.objects.create(title="test collection",description='test description',user=self.user)

    def test(self):
        collection_data = {
            "title":"My Collection - 3 Updated",
            "description":"Third COllection",
            "movies":[
                {
                    "title": "test-movie new",
                    "description": "test-description",
                    "genres": "action,Thriller"
                    },
                ]
            }
        request = self.client.put(f'/collection/{self.collection.uuid}/', json.dumps(collection_data),content_type="application/json",HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(request.status_code,200,"request failed")
        self.assertEqual(request.data['title'],collection_data['title'],"request failed")
        self.assertEqual(request.data['description'],collection_data['description'],"request failed")

        for movie in request.data['movies']:
            if movie['title']==collection_data['movies'][0]['title']:
                self.assertTrue(True)
                break
            else:
                continue
            self.assertTrue(False,"Movie not added")

class DeleteCollectionUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)
        self.collection = Collection.objects.create(title="test collection",description='test description',user=self.user)

    def test(self):
        request = self.client.delete(f'/collection/{self.collection.uuid}/',HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(request.status_code,200,"request failed")
        try:
            Collection.objects.get(uuid=self.collection.uuid)
            self.assertTrue(False,"Collection not deleted")
        except:
            self.assertTrue(True,"Collection deleted")

class RequestCounterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)

    def test(self):
        request = self.client.get(f'/request-count/',HTTP_AUTHORIZATION=self.auth)
        request_count = RequestCounter.objects.all()[0].count
        self.assertEqual(request.status_code,200,"request failed")
        self.assertEqual(request.data['requests'],request_count,"request count is incorrect")

class ResetRequestCountTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password='test@credy')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.auth =  "Token {0}".format(self.token.key)

    def test(self):
        request = self.client.post(f'/request-count/',HTTP_AUTHORIZATION=self.auth)
        request_count = RequestCounter.objects.all()[0].count
        self.assertEqual(request.status_code,200,"request failed")
        self.assertEqual(0,request_count,"request count reset failed")
