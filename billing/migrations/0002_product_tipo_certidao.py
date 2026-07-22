from decimal import Decimal

from django.db import migrations, models
from django.db.models import Q


TIPOS_CERTIDAO = [
    ('inteiro-teor', 'Certidão Inteiro Teor'),
    ('inteiro-teor-livro-03', 'Certidão Inteiro Teor - Livro 03'),
    ('onus-reais', 'Certidão de Busca CPF/CNPJ'),
    ('vintenaria', 'Certidão de Filiação de Domínio'),
    ('atualizada', 'Certidão Atualizada + Ônus Reais + Ações'),
]


def criar_produtos_por_tipo(apps, schema_editor):
    Product = apps.get_model('billing', 'Product')

    produto_base = (
        Product.objects
        .filter(ativo=True, tipo_certidao='', stripe_price_id__gt='')
        .order_by('id')
        .first()
    )

    if produto_base and not Product.objects.filter(tipo_certidao='inteiro-teor').exists():
        produto_base.tipo_certidao = 'inteiro-teor'
        produto_base.save(update_fields=['tipo_certidao'])

    for tipo, nome in TIPOS_CERTIDAO:
        if Product.objects.filter(tipo_certidao=tipo).exists():
            continue
        Product.objects.create(
            nome=nome,
            descricao='Preencha o Stripe Price ID deste tipo de certidão.',
            tipo_certidao=tipo,
            stripe_product_id='',
            stripe_price_id='',
            preco=Decimal('0.00'),
            ativo=False,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tipo_certidao',
            field=models.CharField(
                blank=True,
                choices=TIPOS_CERTIDAO,
                default='',
                help_text='Tipo de certidão que usará este Price ID no checkout.',
                max_length=50,
            ),
        ),
        migrations.RunPython(criar_produtos_por_tipo, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(
                fields=('tipo_certidao',),
                condition=Q(ativo=True) & ~Q(tipo_certidao=''),
                name='unique_active_product_per_certidao',
            ),
        ),
    ]
