from ast import Pass
from django.http import Http404, JsonResponse
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from . models import Movie,Guest,Reservation,Post
from rest_framework.decorators import api_view
from rest_framework import status
from .seriailzers import GuestSerializer,ReservationSerializer,MovieSerializer,PostSerializer
from rest_framework.views import APIView
from rest_framework import generics,mixins,viewsets,filters 
from rest_framework.authentication import BasicAuthentication ,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . permissions import IsAutherOrReedOnly

# Create your views here.

# List == GET
# Create == POST
# pk query == GET 
# Update == PUT
# Delete destroy == DELETE

def test(request):
    return HttpResponse(" i working ")


#1 without rest framework and no model query FBV (FUNCTION BASED VIEW)
def no_rest_no_model(request):
    guests=[
         {
             'id':1,
             'Name': 'Eslam',
            'phone':'01061601974',
         },
         {
              'id':2,
             'Name': 'Qadri',
            'phone':'01142279871',
         },
     ]
    return JsonResponse(guests,safe=False)

#2 no rest and from model 
def no_rest_with_model(request):

    data=Guest.objects.all()
    response=[{
        'guest':list(data.values('name','phone')),
    }
    ]
    return JsonResponse(response,safe=False)

#3 FBV (FUNCTION BASED VIEW)

#   3.1   GET and POST METHODS

@api_view(['GET','POST'] )#THE Pramters is the type of http request
def FBV_LIST(request):
    #the get method get me all clintes name  
    #search
    if request.method == 'GET':
        guests=Guest.objects.all()
        seriailzer=GuestSerializer(guests,many=True)
        return Response (seriailzer.data,status=status.HTTP_201_CREATED)
    #crate new object
    elif request.method == 'POST':
        seriailzer=GuestSerializer(data=request.data)
        if seriailzer.is_valid():
            seriailzer.save()
            return Response (seriailzer.data,status=status.HTTP_201_CREATED)
        
    return Response(seriailzer.data,status=status.HTTP_400_BAD_REQUEST)


#3.2   GET ,DELETE and PUT  METHODS
@api_view(['GET','PUT','DELETE'])
def FBV_BK(request,Pk):
    try:
        guest=Guest.objects.get(pk=Pk)
    except  Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        seriailzer=GuestSerializer(guest)
        return Response (seriailzer.data)
    elif request.method =="DELETE":
        guest.delete()
        return Response (status=status.HTTP_200_OK)
    elif request.method=='PUT':
        seriailzer=GuestSerializer(data=request.data)
        if seriailzer.is_valid():
            seriailzer.save()
            return Response (seriailzer.data,status=status.HTTP_200_OK)
    return Response(seriailzer.errors,status=status.HTTP_400_BAD_REQUEST)


# 4 CBV class based view  
    #inherte APIView from rest_framework.views import APIView
#4.1   GET and post methods
class CBV_LIST(APIView):
    def get(self, request):
        guests=Guest.objects.all()
        seriailzer=GuestSerializer(guests,many=True)
        return Response(seriailzer.data)
    def post(self, request):
        seriailzer=GuestSerializer(data=request.data)
        if seriailzer.is_valid():
            seriailzer.save()
            return Response(seriailzer.data,status=status.HTTP_201_CREATED)
        return Response(seriailzer.errors,status=status.HTTP_400_BAD_REQUEST)

#4.2 GET ,DELETE, PUT  methods
class CBV_BK(APIView):
    def get_object(self,PK):
        try:
            return Guest.objects.get(pk=PK)
        except Guest.DoesNotExist:
            raise Http404
    def get(self,request,PK):
        guest = self.get_object(PK)
        seriailzer=GuestSerializer(guest)
        return Response(seriailzer.data)
    def put(self,request,PK):
        guest = self.get_object(PK)
        seriailzer=GuestSerializer(guest,data=request.data)
        if seriailzer.is_valid():
            seriailzer.save()
            return Response(seriailzer.data,status=200)
        return Response(seriailzer.errors,status=400)
    def delete(self,request,PK):
        guest = self.get_object(PK)
        guest.delete()
        return Response(status=201)

#5 mixins to don't use huge line of code
# not allow to change the varibales name 
#5.1 Mixins list POST,GET Methods

class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

#5.2 mixins get put delete 
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

#6 Generics
#6.1 get and post 
class Generic_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated]

# 6.2 get and put and delete

class Generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer   
    # authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated]

#7 Viwe sets
class Viewset_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer 
class Viewset_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer  
    filter_backend=[filters.SearchFilter]
    search_fields=['movie']
class Viewset_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer  

#8 find move 
@api_view(['GET'])
def find_movie(request):
    movie=Movie.objects.filter(
        movie=request.data['movie'],
        hall=request.data['hall']
    )
    serializer=MovieSerializer(movie,many =True )
    return Response(serializer.data)
#9 create new Reservation
@api_view(['POST'])
def new_Reservation(request):
    movie=Movie.objects.get(
        movie=request.data['movie'],
        hall=request.data['hall']
        )
    guest =Guest()
    guest.name=request.data['name']
    guest.phone=request.data['phone']
    guest.save()

    reservation=Reservation()
    reservation.guest=guest
    reservation.movie=movie
    reservation.save()
    return Response (status=status.HTTP_201_CREATED)

#10 post auther editer 
#this test to coustom permission i created
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAutherOrReedOnly]
    queryset=Post.objects.all()
    serializer_class=PostSerializer
