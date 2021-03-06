# Generated by Django 3.2.9 on 2022-03-29 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sams', '0011_auto_20220329_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('transaction_type', models.CharField(blank=True, choices=[('debit', 'debit'), ('credit', 'credit')], max_length=100, null=True)),
            ],
        ),
    ]
