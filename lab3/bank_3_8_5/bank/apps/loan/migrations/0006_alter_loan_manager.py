# Generated by Django 3.2.4 on 2021-07-09 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subbank', '0002_auto_20210707_0829'),
        ('loan', '0005_auto_20210708_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='Manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Loan_managed_by_Employee', to='subbank.employee'),
        ),
    ]
