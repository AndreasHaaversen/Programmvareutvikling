from django.db import models
import os


def get_image_path(instance, filename):
    return os.path.join('dish_img', str(instance.id), filename)


class Allergen(models.Model):

    ALLERGEN_CHOICES = (
        ('none', ' '),
        ('gluten', 'G'),
        ('shellfish', 'Sh'),
        ('egg', 'E'),
        ('fish', 'F'),
        ('peanuts', 'P'),
        ('soy', 'So'),
        ('milk', 'Mi'),
        ('nuts', 'N'),
        ('celery', 'C'),
        ('mustard', 'Mu'),
        ('sesame', 'Se'),
        ('sulphites', 'Su'),
        ('lupin', 'L'),
        ('molluscs', 'Mo'),
    )
    name = models.CharField(max_length=20, choices=ALLERGEN_CHOICES)

    def __str__(self):
        return self.name


class Dish(models.Model):

    DISH_TYPE_CHOICES = (
        ('maki', 'Maki'),
        ('nigiri', 'Nigiri'),
        ('sashimi', 'Sashimi'),
        ('menu', 'Menu'),
    )

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to=get_image_path, height_field=None,
                              width_field=None, max_length=None)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.CharField(max_length=7, choices=DISH_TYPE_CHOICES,
                                 default='maki')
    allergy_info = models.ManyToManyField(Allergen, default='none')

    class Meta:
        verbose_name_plural = "Dishes"

    def __str__(self):
        return self.name


class OrderInfo(models.Model):

    ORDER_STATUS_CHOICES = (
        ('accepted', 'Accepted'),
        ('prod', 'In production'),
        ('ready', 'Ready'),
        ('collected', 'Collected'),
        ('cancelled', 'Cancelled'),
    )

    name_of_customer = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.IntegerField()
    pickup_time = models.DateTimeField()
    comment = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES,
                              default='accepted')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_order_total(self):
        return sum(dish.price * dish.quantity for dish in self.dishes.all())


class OrderItem(models.Model):
    order = models.ForeignKey(OrderInfo,
                              related_name='dishes',
                              on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,
                             related_name='order_items',
                             on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
