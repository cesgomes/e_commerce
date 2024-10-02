# Generated by Django 5.1 on 2024-10-02 03:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(max_length=1000),
        ),
    ]
