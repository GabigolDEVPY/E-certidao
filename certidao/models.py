from django.db import models

from core.encrypted_fields import EncryptedCharField, EncryptedEmailField, EncryptedTextField
from core.privacy import mask_email, mask_phone


class OrderImovel(models.Model):
    TIPOS_CERTIDAO = [
        ('inteiro-teor', 'Certidão Inteiro Teor'),
        ('onus-reais', 'Certidão de Ônus Reais'),
        ('vintenaria', 'Certidão Vintenária'),
        ('atualizada', 'Certidão Atualizada + Ônus Reais + Ações'),
    ]

    STATUS_PEDIDO = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
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
    # Usuário
    # =========================
    usuario = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='pedidos',
        blank=True,
        null=True
    )

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
    nome_solicitante = EncryptedCharField(max_length=255)
    email = EncryptedEmailField(max_length=254)
    telefone = EncryptedCharField(max_length=20)

    # =========================
    # Dados da Certidão
    # =========================

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

    matriculas = EncryptedTextField(
        blank=True,
        null=True,
        help_text="Separar múltiplas matrículas por vírgula"
    )

    # =========================
    # Endereço do imóvel
    # =========================
    cep_imovel = EncryptedCharField(
        max_length=9,
        blank=True,
        null=True
    )

    numero_imovel = EncryptedCharField(
        max_length=20,
        blank=True,
        null=True
    )

    rua_imovel = EncryptedCharField(
        max_length=255,
        blank=True,
        null=True
    )

    bairro_imovel = EncryptedCharField(
        max_length=255,
        blank=True,
        null=True
    )

    complemento_imovel = EncryptedCharField(
        max_length=255,
        blank=True,
        null=True
    )

    destino_utilizacao = EncryptedTextField()

    # =========================
    # STEP 4 — Cadastro
    # =========================
    pais = models.CharField(
        max_length=100,
        default='Brasil',
        blank=True,
    )

    cep = EncryptedCharField(max_length=9, blank=True, null=True)
    bairro = EncryptedCharField(max_length=255, blank=True, null=True)
    rua = EncryptedCharField(max_length=255, blank=True, null=True)
    numero = EncryptedCharField(max_length=20, blank=True, null=True)

    complemento = EncryptedCharField(
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
    # Pagamento e Status
    # =========================

    is_paid = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_PEDIDO,
        default='pendente'
    )

    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )

    stripe_checkout_session_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='ID da sessão de checkout do Stripe',
    )

    @property
    def email_mascarado(self):
        return mask_email(self.email)

    @property
    def telefone_mascarado(self):
        return mask_phone(self.telefone)
    
    def __str__(self):
        return f'{self.nome_solicitante} - {self.tipo_certidao}'
    
