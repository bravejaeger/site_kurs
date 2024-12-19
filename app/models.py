"""
Definition of models.
"""
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")

    description = models.TextField(verbose_name="Краткое содержание")

    content = models.TextField(verbose_name="Полное содержание")

    posted = models.DateTimeField(default = datetime.now, db_index=True, verbose_name="Опубликована")

    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")

    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке")

    # методы класса
    def get_absolute_url(self):  # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):  # метод возвращает название, используемое для представления отдельных записей в адм. разделе
        return self.title

    # метаданные - вложенный в класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts"  # имя таблицы для модели
        ordering = ["-posted"]  # порядок сортировки данных в модели ("-" означает убывание)
        verbose_name = "статья блога"  # имя, под которым модель будет отображаться в адм. разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога"  # тоже для всех статей блога

# Регистрация модели в админке
admin.site.register(Blog)

class Comment(models.Model):

    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name="Статья комментария")

    def __str__(self):

        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:

        db_table = "Comment"

        ordering = ["-date"]

        verbose_name = "Комментарий к статье блога"

        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)

class Works(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.CharField(max_length=200, verbose_name='Стоимость')
    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке.")
    posted = models.DateTimeField(default = datetime.now, db_index=True, verbose_name="Добавлено")

    def get_absolute_url(self):  
        return reverse("productpost", args=[str(self.id)])
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "Works"  
        ordering = ["posted"]  
        verbose_name = "Примеры работ"  
        verbose_name_plural = "Примеры работ" 

admin.site.register(Works)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина для {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    work = models.ForeignKey(Works, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.work.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")

    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание оплаты'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
        ('Deleted', 'Удален'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    work = models.ForeignKey(Works, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.work.title}"

    @property
    def total_price(self):
        return self.quantity * self.work.price

