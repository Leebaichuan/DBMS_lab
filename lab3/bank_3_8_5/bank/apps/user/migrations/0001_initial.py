# Generated by Django 3.2.4 on 2021-07-07 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('PhoneNum', models.CharField(max_length=20)),
                ('Address', models.CharField(max_length=255)),
                ('Contact_Name', models.CharField(max_length=255)),
                ('Contact_PhoneNum', models.CharField(max_length=20)),
                ('Contact_Email', models.EmailField(max_length=254)),
            ],
        ),
    ]
