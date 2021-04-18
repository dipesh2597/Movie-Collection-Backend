from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from collection.models import Collection,Movie,RequestCounter
from collection.serializers import CollectionSerializer, DeatiledCollectionSerializer
import os
import requests
from requests.auth import HTTPBasicAuth
from django.contrib.sites.shortcuts import get_current_site
from collections import Counter

# Create your views here.
class MoviesViews(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        # Making a get request
        try:
            page = request.GET['page']
        except:
            page = None
        if not page:
            page=1
        username = os.environ['username']
        password = os.environ['password']
        response = requests.get(f'https://demo.credy.in/api/v1/maya/movies/?page={page}',auth = HTTPBasicAuth(username, password))
        if response.status_code == 200:
            response = response.json()
            count = response['count']
            
            next_page_link = F"{get_current_site(request)}{request.path}?page={int(page)+1}"
            if int(page)>1:
                previous_page_link = F"{get_current_site(request)}{request.path}?page={int(page)-1}"
            else:
                previous_page_link = None
            data = {'count':count,'next':next_page_link,'previous':previous_page_link,'data':response['results']}
            return Response(data,status=HTTP_200_OK)
        else:
            data = {"message":"Error while fetching data. Try again!!"}
            return Response(data,status=HTTP_400_BAD_REQUEST)

class CollectionView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,collection_uuid=None):
        if collection_uuid:
            '''if uuid available then give details of that particular collection only'''
            collection = Collection.objects.get(uuid=collection_uuid)
            return Response(DeatiledCollectionSerializer(collection).data,status=HTTP_200_OK)
        try:
            collections = Collection.objects.filter(user=request.user)
            # checking if there is atleast 1 collection available for the user
            collections[0]
            is_success = True
        except Exception as e:
            is_success = False
        if is_success:
            data={}
            data['collection']=CollectionSerializer(collections,many=True).data
            genres = Movie.objects.filter(collection__in=collections).values_list('genres',flat=True)
            genres_list=[]
            for genre in genres:
                '''Creating genre list based on movie added'''
                [genres_list.append(single_genre) for single_genre in genre.split(",") if single_genre!='']
            genres_counter=Counter(genres_list)
            top_three_genre = genres_counter.most_common(3)
            try:
                favourite_genres = f"{top_three_genre[0][0]},{top_three_genre[1][0]},{top_three_genre[2][0]}"
            except:
                favourite_genres = ""
            data['favourite_genres']=favourite_genres
            response={'is_success':is_success,'data':data}
            return Response(response,status=HTTP_200_OK)
        else:
            response={'is_success':is_success,'data':{}}
            return Response(response,status=HTTP_400_BAD_REQUEST)

    def post(self,request):
        title = request.data.get('title')
        description = request.data.get('description')
        collection = Collection.objects.create(title=title,description=description,user=request.user)
        movies = request.data.get('movies')
        for movie in movies:
            movie = Movie.objects.create(title=movie['title'],description=movie['description'],genres=movie['genres'],collection=collection)
        
        return Response({"collection_uuid":collection.uuid},status=HTTP_201_CREATED)
    
    def put(self,request,collection_uuid):
        collection = Collection.objects.get(uuid=collection_uuid)
        title = request.data.get('title')
        description = request.data.get('description')
        movies = request.data.get('movies')
        if title:
            collection.title=title
        if description:
            collection.description=description
        if movies:
            for movie in movies:
                movie = Movie.objects.create(title=movie['title'],description=movie['description'],genres=movie['genres'],collection=collection)
        return Response(DeatiledCollectionSerializer(collection).data,status=HTTP_200_OK)

    def delete(self,request,collection_uuid):
        collection = Collection.objects.get(uuid=collection_uuid)
        collection.delete()
        return Response({"message":f"{collection.title} deleted successfully."},status=HTTP_200_OK)  

class RequestCounterView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        request_count = RequestCounter.objects.all()[0].count
        return Response({"requests":request_count},status=HTTP_200_OK)

    def post(self,request):
        request_count = RequestCounter.objects.all()[0]
        request_count.count = 0
        request_count.save()
        return Response({"message": "request count reset successfully"},status=HTTP_200_OK)