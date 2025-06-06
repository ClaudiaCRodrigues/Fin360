# Generated by Django 4.2.9 on 2025-05-21 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0002_category_investmenttype_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmenttype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='investment_types', to='investments.category', verbose_name='Categoria'),
        ),
    ]
