from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .manager import IAuthorManager

class IAuthor(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user/')
    bio = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = IAuthorManager()
    def __str__(self):
        return self.name


class IBlog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(IAuthor, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(upload_to='blog/')
    createdAt = models.DateField(auto_now_add=True)
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title
