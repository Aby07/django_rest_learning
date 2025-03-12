#from django.shortcuts import render
#from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from students.models import Students
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .paginations import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


@api_view(['GET', 'POST'])
def studentsView(request): 
    if request.method == 'GET': # return all student data
        students = Students.objects.all()
        serilizers = StudentSerializer(students, many=True)
        return Response(serilizers.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST': # create a new student
        serilizers = StudentSerializer(data=request.data)
        if serilizers.is_valid(): 
            serilizers.save()
            return Response(serilizers.data, status=status.HTTP_201_CREATED)
        return Response(serilizers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk):
    try:
        student=Students.objects.get(pk=pk)
    except Students.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': # get a single student data
        serilizer = StudentSerializer(student)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT': # update a single student data
        serilizer = StudentSerializer(student, data=request.data)
        if serilizer.is_valid(): 
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_200_OK)
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE': # delete a student detail
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#class based view

class Employees(APIView): # class based view
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request): #creating a employee
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
           return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self, request, pk): #get a single employee details
        emp = self.get_object(pk)
        serializer = EmployeeSerializer(emp)
        return Response(serializer.data, status=status.HTTP_200_OK)      
    
    def put(self, request, pk):
        emp = self.get_object(pk)
        serilizer = EmployeeSerializer(emp, data=request.data)
        if serilizer.is_valid(): 
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_200_OK)
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        emp = self.get_object(pk)
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# mixins

class MixinEmployees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
    
class MixinEmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)
    
# Generics

# class GenericEmployee(generics.ListAPIView, generics.CreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

class GenericEmployee(generics.ListCreateAPIView): #using combiation of list and create
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    
# class GenericEmployeeDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = 'pk'
    
class GenericEmployeeDetail(generics.RetrieveUpdateDestroyAPIView): #combination of retrive update and delete using pk
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'

#Viewsets

class ViewSetEmployeeView(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def retrieve(self, request, pk):
        queryset = Employee.objects.all()
        emp = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(emp)
        return Response(serializer.data)
    
    def update(self, request, pk):
        emp = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(emp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        emp = get_object_or_404(Employee, pk=pk)
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ModelViewSetEmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    #filterset_fields = ['designatiion']
    filterset_class = EmployeeFilter


#used in nested serializer
class BlogViews(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter]
    search_fields = ['blog_title']

class CommentsViews(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class BlogDetailViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentsDetailViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

