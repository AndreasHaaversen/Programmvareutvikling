from django.db import models
import os


def get_image_path(instance, filename):
    return os.path.join('dish_img', str(instance.id), filename)


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to=get_image_path, height_field=None,
                              width_field=None, max_length=None)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.CharField(max_length=25)

    def __str__(self):
        return self.name
