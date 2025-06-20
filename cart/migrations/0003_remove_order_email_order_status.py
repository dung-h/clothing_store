# Generated by Django 5.1.5 on 2025-06-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_order_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="email",
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Chờ xử lý"),
                    ("processing", "Đang xử lý"),
                    ("shipped", "Đã giao"),
                    ("cancelled", "Đã hủy"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
