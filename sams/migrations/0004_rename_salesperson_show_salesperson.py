# Generated by Django 3.2.9 on 2022-03-26 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sams', '0003_auto_20220326_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='Salesperson',
            new_name='salesperson',
        ),
    ]