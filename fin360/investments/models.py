from django.db import models

class InvestmentType(models.Model):
    nome = models.CharField(
        verbose_name="Nome",
        max_length=100,
        unique=True,
        help_text="Ex: Renda Fixa, Ações, Criptomoedas etc."
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        blank=True,
        null=True,
        help_text="Detalhes adicionais sobre este tipo de investimento."
    )

    class Meta:
        verbose_name = "Tipo de Investimento"
        verbose_name_plural = "Tipos de Investimento"
        ordering = ['nome']

    def __str__(self):
        return self.nome
