# Generated by Django 5.1.6 on 2025-02-21 20:12

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_nft_owner_alter_nft_uploaded_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nft_buys', to=settings.AUTH_USER_MODEL)),
                ('nft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.nft')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nft_sales', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
