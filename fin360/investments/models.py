from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name        = models.CharField("Nome",      max_length=100, unique=True)
    slug        = models.SlugField("Slug",      max_length=100, unique=True, blank=True)
    description = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class InvestmentType(models.Model):
    nome      = models.CharField(
        "Nome",
        max_length=100,
        unique=True,
        help_text="Ex: CDB, Ações, Criptomoedas etc."
    )
    category  = models.ForeignKey(
        Category,
        verbose_name="Categoria",
        on_delete=models.PROTECT,
        related_name="investment_types",
        null=True,
        blank=True,
    )
    descricao = models.TextField(
        "Descrição",
        blank=True, null=True,
        help_text="Detalhes adicionais sobre este tipo."
    )

    class Meta:
        verbose_name = "Tipo de Investimento"
        verbose_name_plural = "Tipos de Investimento"
        ordering = ["nome"]

    def __str__(self):
        # usa o campo correto (self.nome) e trata category nula
        cat = self.category.name if self.category else "Sem categoria"
        return f"{self.nome} ({cat})"
