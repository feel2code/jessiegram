# Generated by Django 2.2.16 on 2022-03-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20220328_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=25),
        ),
    ]
