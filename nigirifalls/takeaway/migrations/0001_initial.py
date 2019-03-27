# Generated by Django 2.1.7 on 2019-03-26 14:38

from django.db import migrations, models
import django.db.models.deletion
import takeaway.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('none', ' '), ('gluten', 'G'), ('shellfish', 'Sh'), ('egg', 'E'), ('fish', 'F'), ('peanuts', 'P'), ('soy', 'So'), ('milk', 'Mi'), ('nuts', 'N'), ('celery', 'C'), ('mustard', 'Mu'), ('sesame', 'Se'), ('sulphites', 'Su'), ('lupin', 'L'), ('molluscs', 'Mo')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=takeaway.models.get_image_path)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dish_type', models.CharField(choices=[('maki', 'Maki'), ('nigiri', 'Nigiri'), ('sashimi', 'Sashimi'), ('menu', 'Menu')], default='maki', max_length=7)),
                ('allergy_info', models.ManyToManyField(default='none', to='takeaway.Allergen')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_customer', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
                ('pickup_time', models.DateTimeField()),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('prod', 'In production'), ('ready', 'Ready'), ('collected', 'Collected'), ('cancelled', 'Cancelled')], default='accepted', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='takeaway.Dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='takeaway.OrderInfo')),
            ],
        ),
    ]
