from django.db import models

# Create your models here.

from django.db import models


class OrderImovel(models.Model):

    TIPOS_CERTIDAO = [
        ('inteiro-teor', 'Certidão Inteiro Teor'),
        ('onus-reais', 'Certidão de Ônus Reais'),
        ('vintenaria', 'Certidão Vintenária'),
        ('atualizada', 'Certidão Atualizada + Ônus Reais + Ações'),
    ]

    FORMATO_CERTIDAO = [
        ('atualizada', 'Certidão Atualizada + Ônus Reais + Ações'),
        ('inteiro-teor', 'Certidão Inteiro Teor'),
        ('onus', 'Certidão de Ônus Reais'),
        ('vintenaria', 'Certidão Vintenária'),
    ]

    TIPO_IDENTIFICACAO = [
        ('matricula', 'Matrícula'),
        ('transcricao', 'Transcrição'),
    ]

    TIPO_BUSCA = [
        ('matricula', 'Tenho matrícula/transcrição'),
        ('endereco', 'Tenho endereço do imóvel'),
    ]

    # =========================
    # STEP 1 — Tipo Certidão
    # =========================
    tipo_certidao = models.CharField(
        max_length=50,
        choices=TIPOS_CERTIDAO
    )

    # =========================
    # STEP 2 — Cartório
    # =========================
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cartorio = models.CharField(max_length=255)

    # =========================
    # STEP 3 — Solicitante
    # =========================
    nome_solicitante = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    # =========================
    # Dados da Certidão
    # =========================
    formato_certidao = models.CharField(
        max_length=50,
        choices=FORMATO_CERTIDAO
    )

    tipo_busca = models.CharField(
        max_length=20,
        choices=TIPO_BUSCA
    )

    tipo_identificacao = models.CharField(
        max_length=20,
        choices=TIPO_IDENTIFICACAO,
        blank=True,
        null=True
    )

    matriculas = models.TextField(
        blank=True,
        null=True,
        help_text="Separar múltiplas matrículas por vírgula"
    )

    # =========================
    # Endereço do imóvel
    # =========================
    cep_imovel = models.CharField(
        max_length=9,
        blank=True,
        null=True
    )

    numero_imovel = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    rua_imovel = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    bairro_imovel = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    complemento_imovel = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    destino_utilizacao = models.TextField()

    # =========================
    # STEP 4 — Cadastro
    # =========================
    pais = models.CharField(
        max_length=100,
        default='Brasil'
    )

    cep = models.CharField(max_length=9)
    bairro = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)

    complemento = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # =========================
    # Controle
    # =========================
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    # =========================
    # Pagamento
    # =========================

    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.nome_solicitante} - {self.tipo_certidao}'
    
