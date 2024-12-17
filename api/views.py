from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from api.serializers import UserSerializers,TodoSerializer

from rest_framework import authentication,permissions

from task.models import Todo

from rest_framework import serializers

# Create your views here.

class UserCreationView(APIView):

    serializer_class=UserSerializers

    def post(self,request,*args,**kwargs):

        serializer_instance=self.serializer_class(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)
        
        return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
    

class TodoListCreateView(APIView):

    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    serializer_class=TodoSerializer

    def get(self,request,*args,**kwargs):

        #request.user


        qs=Todo.objects.filter(owner=request.user)

        #localhost:8000/api/todos?status=true (optional query parameter)

        #fetching query parameter

        #request.query_params={} (get dictionary)(status=key and true=value)

        if "status" in request.query_params:

            search_text=request.query_params.get("status")

            qs=qs.filter(status=search_text)


        serializer_insatance=self.serializer_class(qs,many=True)

        return Response(data=serializer_insatance.data)
    
    def post(self,request,*args,**kwargs):

        serializer_instance=self.serializer_class(data=request.data) #deserialization

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        
        return Response(data=serializer_instance.errors)
    
class TodoRetrieveUpdateDestroyView(APIView):

    serializer_class=TodoSerializer

    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=get_object_or_404(Todo,pk=id)

        serializer_instance=self.serializer_class(qs)

        return Response(data=serializer_instance.data)
    
    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        todo_obj=get_object_or_404(Todo,id=id)

        if request.user != todo_obj.owner:

            raise serializers.ValidationError("Access Denied")

        todo_obj.delete()

        return Response(data={"message":"deleted"})
    
    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        todo_obj=get_object_or_404(Todo,id=id)

        if request.user != todo_obj.owner:

            raise serializers.ValidationError("Access Denied")

        serializer_instance=self.serializer_class(data=request.data,instance=todo_obj)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        return Response(data=serializer_instance.errors)    
