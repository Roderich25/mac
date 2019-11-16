from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(estatus='publicado')


class Post(models.Model):
    STATUS_CHOICES = (('boceto', 'Boceto'), ('publicado', 'Publicado'))
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publicado')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    contenido = models.TextField()
    publicado = models.DateField(default=timezone.now)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)
    estatus = models.CharField(max_length=10, choices=STATUS_CHOICES, default='boceto')
    objectos = models.Manager()
    publicados = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publicado',)
        db_table = 'blog_posts'

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publicado.year,
                                                 self.publicado.month,
                                                 self.publicado.day,
                                                 self.slug])


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.CharField(max_length=80)
    email = models.EmailField()
    comentario = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('creado',)

    def __str__(self):
        return f'Comentario de {self.nombre} en "{self.post}"'
