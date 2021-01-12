from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Posting
from .serializers import PostingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

#auth stuff
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PostingViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = PostingSerializer
    queryset = Posting.objects.all()

    """
    ViewSet Sample Code
    def list(self, request):
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PostingSerializer(data=request.data)
    #validate the serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Posting.objects.all()
        posting = get_object_or_404(queryset, pk=pk)
        serializer = PostingSerializer(posting)
        return Response(serializer.data)

    def update(self, request, pk=None):
        posting = Posting.objects.get(pk=pk)
        serializer = PostingSerializer(posting, data=request.data)

        #validate the serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        posting = Posting.objects.get(pk=pk)
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, 
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostingSerializer
    queryset = Posting.objects.all()

    lookup_field = 'id'

    #auth setup
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)
    
    def delete(self, request, id = None):
        return self.destroy(request, id)

class postingAPIVIew(APIView):

    def get(self, request):
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostingSerializer(data=request.data)
   
    #validate the serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #invalid serializer handler    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def postingList(request):
    
    if request.method == 'GET':
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostingSerializer(data=request.data)
    #validate the serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def postingDetail(request, pk):
    try:
        posting = Posting.objects.get(pk=pk)

    except Posting.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostingSerializer(posting)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostingSerializer(posting, data=request.data)

        #validate the serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostingDetailsAPIVIew(APIView):

    def getObject(self, id):
        try:
            return Posting.objects.get(id=id)
        except Posting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        posting = self.getObject(id)

        serializer = PostingSerializer(posting)
        return Response(serializer.data)
    
    def put(self, request, id):
        posting = self.getObject(id)
        serializer = PostingSerializer(posting, data=request.data)

        #validate the serializer before saving
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        posting = self.getObject(id)
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    