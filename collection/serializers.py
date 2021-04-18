from rest_framework import serializers
from collection.models import Collection,Movie

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('title', 'description', 'uuid')

class DeatiledCollectionSerializer(serializers.ModelSerializer):

    movies = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('title', 'description', 'movies')

    def get_movies(self,obj):
        movies = Movie.objects.filter(collection=obj)
        data=[]
        [data.append({'title':movie.title,'description':movie.description,'uuid':movie.uuid,'genres':movie.genres}) for movie in movies]
        return data