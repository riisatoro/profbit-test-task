# Generated by Django 4.0.3 on 2022-03-29 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_created_at_category_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_at',)},
        ),
    ]
