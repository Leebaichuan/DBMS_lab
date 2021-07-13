# Generated by Django 3.2.4 on 2021-07-07 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('Type', models.CharField(max_length=20)),
                ('Leader_ID', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subbank',
            fields=[
                ('Name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('City', models.CharField(max_length=255)),
                ('Asset', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=255)),
                ('PhoneNum', models.CharField(max_length=20)),
                ('Address', models.CharField(max_length=255)),
                ('StartDate', models.DateTimeField(auto_now_add=True)),
                ('Depart_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works_for', to='subbank.department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='Subbank_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to', to='subbank.subbank'),
        ),
    ]
