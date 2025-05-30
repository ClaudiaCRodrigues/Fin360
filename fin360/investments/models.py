from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db.models import JSONField


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
        'Tipo de Instituição', max_length=20,
        choices=INSTITUTION_TYPES,
        default=BANK
    )
    code = models.CharField('Código interno', max_length=50, blank=True, null=True)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    website = models.URLField('Site', blank=True)
    email = models.EmailField('E-mail de contato', blank=True)
    phone_number = models.CharField('Telefone', max_length=30, blank=True)
    address = models.TextField('Endereço completo', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    # ← Novos campos para reconhecimento dinâmico
    signature_patterns = ArrayField(
        base_field=models.CharField(max_length=200),
        blank=True,
        default=list,
        help_text="Strings que aparecem no PDF para identificar esta instituição"
    )
    parser_class = models.CharField(
        'Classe de Parser',
        max_length=200,
        blank=True,
        help_text="Import path da classe de parser, ex: 'investments.parsers.XPParser'"
    )
    
    parsing_rules = JSONField(
        'Regras de Parsing',
        default=dict,
        blank=True,
        help_text="Defina um JSON com regex para cada campo, ex: "
                  r'{"data_operacao": "Data de\\s*Cotização\\s*(\\d{2}/\\d{2}/\\d{4})", '
                  r'"valor": "Valor Solicitado\\s*R\\$\\s*([\\d\\.\\,]+)", '
                  r'"tipo": "Operação\\s*(Aplicação|Resgate)"}'
    )

    class Meta:
        verbose_name = 'Instituição Financeira'
        verbose_name_plural = 'Instituições Financeiras'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    nome = models.CharField(
        'Nome', max_length=100, unique=True,
        help_text='Ex: CDB, Ações, Criptomoedas etc.'
    )
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
    broker = models.ForeignKey(
        FinancialInstitution, on_delete=models.PROTECT
    )
    name = models.CharField('Nome', max_length=200)
    ticker = models.CharField('Ticker', max_length=20, blank=True)
    initial_value = models.DecimalField(
        'Valor Investido', max_digits=14, decimal_places=2
    )
    current_value = models.DecimalField(
        'Valor Atual', max_digits=14, decimal_places=2
    )
    quantidade = models.DecimalField(
        'Quantidade', max_digits=20, decimal_places=8, null=True, blank=True
    )
    preco_unitario = models.DecimalField(
        'Preço Unitário', max_digits=20, decimal_places=8, null=True, blank=True
    )
    valor_total = models.DecimalField(
        'Valor Total', max_digits=20, decimal_places=2, null=True, blank=True
    )
    acquired_date = models.DateField('Data de Aquisição', null=True, blank=True)
    data_operacao = models.DateField('Data de Operação', null=True, blank=True)
    tipo = models.CharField('Tipo Operação', max_length=50, null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

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


class InvestmentTransaction(models.Model):
    investment = models.ForeignKey(
        Investment,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    date = models.DateField('Data')
    transaction_type = models.CharField(
        'Tipo', max_length=10,
        choices=[('buy', 'Buy'), ('sell', 'Sell'), ('apply', 'Apply'), ('rescue', 'Rescue')]
    )
    quantity = models.DecimalField(
        'Quantidade', max_digits=20, decimal_places=8
    )
    price = models.DecimalField(
        'Preço', max_digits=20, decimal_places=8
    )
    fees = models.DecimalField(
        'Taxas', max_digits=20, decimal_places=2, default=0
    )
    description = models.TextField('Descrição', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date']

    def __str__(self):
        return f"{self.investment} – {self.transaction_type} em {self.date:%d/%m/%Y}"


class Index(models.Model):
    SELIC = 'selic'
    IPCA = 'ipca'
    CDI = 'cdi'
    OTHER = 'other'

    INDEX_CHOICES = [
        (SELIC, 'SELIC'),
        (IPCA, 'IPCA'),
        (CDI, 'CDI'),
        (OTHER, 'Outro'),
    ]

    name = models.CharField('Índice', max_length=20, choices=INDEX_CHOICES)
    value = models.DecimalField('Valor (%)', max_digits=6, decimal_places=2)
    date = models.DateField('Data de Referência')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Índice'
        verbose_name_plural = 'Índices'
        unique_together = ('name', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_name_display()} — {self.value}% em {self.date:%d/%m/%Y}"

    def get_absolute_url(self):
        return reverse('admin_index_list')
