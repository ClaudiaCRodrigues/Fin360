from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class FinancialInstitution(models.Model):
    BANK = 'bank'
    BROKERAGE = 'brokerage'
    OTHER = 'other'
    INSTITUTION_TYPES = [
        (BANK, 'Banco'),
        (BROKERAGE, 'Corretora'),
        (OTHER, 'Outro'),
    ]

    name = models.CharField('Nome', max_length=200, unique=True)
    slug = models.SlugField('Slug', max_length=200, unique=True)
    institution_type = models.CharField(
        'Tipo de Instituição', max_length=20, choices=INSTITUTION_TYPES, default=BANK
    )
    code = models.CharField('Código interno', max_length=50, blank=True, null=True)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    website = models.URLField('Site', blank=True)
    email = models.EmailField('E-mail de contato', blank=True)
    phone_number = models.CharField('Telefone', max_length=30, blank=True)
    address = models.TextField('Endereço completo', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Instituição Financeira'
        verbose_name_plural = 'Instituições Financeiras'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('institution_detail', kwargs={'slug': self.slug})

class Category(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True)
    description = models.TextField('Descrição', blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class InvestmentType(models.Model):
    nome = models.CharField('Nome', max_length=100, unique=True,
                            help_text='Ex: CDB, Ações, Criptomoedas etc.')
    category = models.ForeignKey(
        Category, verbose_name='Categoria', on_delete=models.PROTECT,
        related_name='investment_types', null=True, blank=True
    )
    descricao = models.TextField('Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de Investimento'
        verbose_name_plural = 'Tipos de Investimento'
        ordering = ['nome']

    def __str__(self):
        cat = self.category.name if self.category else 'Sem categoria'
        return f"{self.nome} ({cat})"

class Investment(models.Model):
    category = models.ForeignKey(
        Category, related_name='investments', on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        InvestmentType, related_name='investments', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    name = models.CharField('Nome do Ativo', max_length=200)
    ticker = models.CharField('Ticker', max_length=20, blank=True)
    initial_value = models.DecimalField('Valor Investido', max_digits=14, decimal_places=2)
    current_value = models.DecimalField('Valor Atual', max_digits=14, decimal_places=2)
    acquired_date = models.DateField('Data de Aquisição', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Investimento'
        verbose_name_plural = 'Investimentos'

    def __str__(self):
        return f"{self.name} ({self.ticker})"

    @property
    def return_percent(self):
        if self.initial_value:
            return (self.current_value / self.initial_value - 1) * 100
        return 0