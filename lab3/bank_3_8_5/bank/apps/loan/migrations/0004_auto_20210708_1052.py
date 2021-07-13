# Generated by Django 3.2.4 on 2021-07-08 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_user_haha'),
        ('subbank', '0002_auto_20210707_0829'),
        ('loan', '0003_remove_loan_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='Manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Loan_managed_by_Employee', to='subbank.employee'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='Subbank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Loan_issued_by_Subbank', to='subbank.subbank'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='User',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Loan_owned_by_User', to='user.user'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='Loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Payment_pays_for_Loan', to='loan.loan'),
        ),
    ]
