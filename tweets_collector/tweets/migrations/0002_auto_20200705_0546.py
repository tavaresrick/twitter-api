# Generated by Django 3.0.8 on 2020-07-05 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='country',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='language',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
