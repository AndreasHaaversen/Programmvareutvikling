# Generated by Django 2.1.5 on 2019-02-13 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takeaway', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='dish_type',
            new_name='dish_class',
        ),
    ]