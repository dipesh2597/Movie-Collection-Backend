from collection.models import RequestCounter

class RequestCounterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Whenever a request hits the server this method would be called once
        try:
            '''If a recorded is created then we will increase it by 1 We will make sure rather than this there is no place from where extra records are getting created only one record would be available all time in this table'''
            request_counter=RequestCounter.objects.all()[0]
            request_counter.count+=1
            request_counter.save()
        except:
            '''for first request we will create a record'''
            RequestCounter.objects.create(count=1)
        response = self.get_response(request)
        return response
