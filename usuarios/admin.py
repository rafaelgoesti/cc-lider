from django.contrib import admin
from .models import Usuarios, Aula, Material, Aviso, EventoAcademico, EventoGeral, ContatoProfessor

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome')
    search_fields = ('matricula', 'nome')

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'professor', 'dia', 'hora_inicio', 'hora_fim', 'sala', 'cor_sala')
    list_filter = ('dia', 'professor', 'cor_sala')
    search_fields = ('disciplina', 'professor', 'sala')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'disciplina', 'aula', 'data_upload', 'is_novo')
    list_filter = ('tipo', 'disciplina', 'is_novo')
    search_fields = ('titulo', 'descricao', 'disciplina')

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'icone', 'destaque')
    list_filter = ('destaque', 'data_publicacao')
    search_fields = ('titulo', 'mensagem')

@admin.register(EventoAcademico)
class EventoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'tipo', 'data', 'horario', 'local')
    list_filter = ('tipo', 'disciplina', 'data')
    search_fields = ('disciplina', 'local')

@admin.register(EventoGeral)
class EventoGeralAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'data_inicio', 'data_fim', 'horario', 'local')
    list_filter = ('tipo', 'data_inicio')
    search_fields = ('titulo', 'local', 'descricao')

@admin.register(ContatoProfessor)
class ContatoProfessorAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'nome_professor', 'email', 'atendimento')
    list_filter = ('disciplina',)
    search_fields = ('nome_professor', 'email')
