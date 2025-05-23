# Generated by Django 4.2.9 on 2025-05-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0003_alter_investmenttype_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialInstitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nome')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Slug')),
                ('institution_type', models.CharField(choices=[('bank', 'Banco'), ('brokerage', 'Corretora'), ('other', 'Outro')], default='bank', max_length=20, verbose_name='Tipo de Instituição')),
                ('code', models.CharField(blank=True, help_text='Ex: código usado no sistema externo', max_length=50, null=True, verbose_name='Código interno')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('website', models.URLField(blank=True, verbose_name='Site')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail de contato')),
                ('phone_number', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('address', models.TextField(blank=True, verbose_name='Endereço completo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Instituição Financeira',
                'verbose_name_plural': 'Instituições Financeiras',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='investmenttype',
            name='descricao',
            field=models.TextField(blank=True, help_text='Detalhes adicionais sobre este tipo.', null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='investmenttype',
            name='nome',
            field=models.CharField(help_text='Ex: CDB, Ações, Criptomoedas etc.', max_length=100, unique=True, verbose_name='Nome'),
        ),
    ]
