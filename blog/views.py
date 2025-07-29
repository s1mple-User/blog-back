from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import IBlog, IAuthor
from .serializers import RegistrationSerializer,IBlogSerializer,IAuthorSerializer,TokenObtainPairSerializer,IBlogSerializerAll
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView  

class BlogAll(ListAPIView):
    queryset = IBlog.objects.all()
    serializer_class = IBlogSerializer

class UserDetailAPIView():
    queryset = IAuthor.objects.all()
    serializer_class = IBlogSerializer
    lookup_field = 'id' 

class DeleteCard():
    queryset = IBlog.objects.all()
    serializer_class = IBlogSerializer
    lookup_field = 'id' 

class CreateUser(generics.ListCreateAPIView):
    queryset = IBlog.objects.all()
    serializer_class  = RegistrationSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class BlogListAPIView(generics.ListCreateAPIView):
    queryset = IBlog.objects.all().order_by('-createdAt')
    serializer_class = IBlogSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
     serializer.save(author=self.request.user)

class BlogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IBlog.objects.all()
    serializer_class = IBlogSerializer
    lookup_field = 'slug' 


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  
        self.perform_destroy(instance)
        return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    

    def perform_update(self, serializer):
     serializer.save(author=self.request.user)

    def patch(self, request, *args, **kwargs):
     instance = self.get_object()
     serializer = self.get_serializer(instance, data=request.data, partial=True)

     if serializer.is_valid():
        self.perform_update(serializer)
        return Response(serializer.data)
     else:
        return Response(serializer.errors, status=400)


        

class AuthorListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            author = IAuthor.objects.get(id=request.user.id)
            serializer = IAuthorSerializer(author)
            return Response(serializer.data)
        except IAuthor.DoesNotExist:
            return Response({'detail': 'Author not found'}, status=404)
        
class BlogsAPIView(APIView):
   def get(self, request):
    search_query = request.GET.get('search', '') 
    if search_query:
        blogs = IBlog.objects.filter(title__icontains=search_query) 
    else:
        blogs = {}

    serializer = IBlogSerializerAll(blogs, many=True)
    return Response(serializer.data)

class BlogsByAuthorAPIView(APIView):

    def get(self, request, author_id, format=None):
        author = get_object_or_404(IAuthor, id=author_id)
        blogs = author.blogs.all()
        serializer = IBlogSerializer(blogs, many=True)
        return Response(serializer.data)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message":"Token is blocked"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)