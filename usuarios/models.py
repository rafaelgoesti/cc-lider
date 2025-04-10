from django.db import models

class Usuarios(models.Model):
    matricula = models.IntegerField()
    nome = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nome)

DIAS_SEMANA = [
    ('SEG', 'Segunda'),
    ('TER', 'Terça'),
    ('QUA', 'Quarta'),
    ('QUI', 'Quinta'),
    ('SEX', 'Sexta'),
]

class Aula(models.Model):
    dia = models.CharField(max_length=3, choices=DIAS_SEMANA)
    disciplina = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    sala = models.CharField(max_length=500)
    cor_sala = models.CharField(max_length=20, default='primary')

    def __str__(self):
        return f"{self.disciplina} - {self.dia} {self.hora_inicio.strftime('%H:%M')}"
    class Meta:
        ordering = ['dia', 'hora_inicio']

class Material(models.Model):
    TIPO_CHOICES = [
        ('PDF', 'Documento PDF'),
        ('PPT', 'Apresentação PowerPoint'),
        ('ZIP', 'Arquivo Compactado'),
        ('VID', 'Vídeo'),
        ('DOC', 'Documento'),
        ('LNK', 'Link Externo'),
    ]

    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='materiais', null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    arquivo = models.FileField(upload_to='materiais/')
    data_upload = models.DateTimeField(auto_now_add=True)
    is_novo = models.BooleanField(default=True)
    disciplina = models.CharField(max_length=100)  # Ou relacione com um modelo Disciplina

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

    class Meta:
        verbose_name_plural = "Materiais"
        ordering = ['-data_upload']

class Aviso(models.Model):
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    icone = models.CharField(max_length=50, default='fa-bullhorn')  # ex: fa-users, fa-book
    destaque = models.BooleanField(default=False)  # para mostrar o alerta especial no topo

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-data_publicacao']

class EventoAcademico(models.Model):
    TIPO_CHOICES = [
        ('PROVA', 'Prova'),
        ('TRABALHO', 'Trabalho'),
        ('PROJETO', 'Projeto'),
        ('APRESENTACAO', 'Apresentação'),
        # Adicione mais se necessário
    ]

    disciplina = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.disciplina} - {self.get_tipo_display()} em {self.data.strftime('%d/%m/%Y')}"

class EventoGeral(models.Model):
    TIPO_CHOICES = [
        ('EVENTO', 'Evento'),
        ('PALESTRA', 'Palestra'),
        ('COMPETICAO', 'Competição'),
        ('REUNIAO', 'Reunião'),
        ('OUTRO', 'Outro'),
    ]

    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='OUTRO')
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    horario = models.TimeField(null=True, blank=True)
    local = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

class ContatoProfessor(models.Model):
    disciplina = models.CharField(max_length=100)
    nome_professor = models.CharField(max_length=100)
    email = models.EmailField()
    atendimento = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.disciplina} - {self.nome_professor}"