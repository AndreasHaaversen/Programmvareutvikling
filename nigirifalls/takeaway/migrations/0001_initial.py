# Generated by Django 2.1.5 on 2019-02-13 11:24

from django.db import migrations, models
import takeaway.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=takeaway.models.get_image_path)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dish_type', models.CharField(max_length=25)),
            ],
        ),
    ]
