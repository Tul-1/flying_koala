# Generated by Django 3.2.7 on 2022-06-14 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0004_alter_userrecipedata_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecipedata',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]