# Generated by Django 3.2 on 2024-01-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paragraphsearch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]