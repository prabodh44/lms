# Generated by Django 3.0 on 2021-01-18 08:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20210101_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_fullname',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]