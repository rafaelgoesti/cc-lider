from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Usuarios, Aula, Material, Aviso, EventoAcademico, EventoGeral, ContatoProfessor


def login(request):
    if request.method == "POST":
        matricula = request.POST.get('matricula')
        try:
            usuario = Usuarios.objects.get(matricula=matricula)
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nome'] = usuario.nome
            response = redirect('home')
            response.set_cookie('mostrar_boas_vindas', 'true', max_age=5)
            return response
        except Usuarios.DoesNotExist:
            return render(request, 'login.html', {'mensagem': "Matrícula não encontrada."})
    return render(request, 'login.html')

def get_contexto_geral(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    try:
        usuario = Usuarios.objects.get(id=request.session['usuario_id'])
    except Usuarios.DoesNotExist:
        request.session.flush()
        return redirect('login')

    DIAS_SEMANA = {
        'SEG': 'Segunda',
        'TER': 'Terça',
        'QUA': 'Quarta',
        'QUI': 'Quinta',
        'SEX': 'Sexta',
    }

    aulas = Aula.objects.order_by('dia', 'hora_inicio')
    aulas_por_dia = {dia: [] for dia in DIAS_SEMANA}
    for aula in aulas:
        if aula.dia in aulas_por_dia:
            aulas_por_dia[aula.dia].append(aula)

    materiais = Material.objects.all().order_by('-data_upload')
    materiais_por_disciplina = {}
    for material in materiais:
        if material.disciplina not in materiais_por_disciplina:
            materiais_por_disciplina[material.disciplina] = []
        materiais_por_disciplina[material.disciplina].append(material)

    avisos = Aviso.objects.all().order_by('-data_publicacao')
    aviso_destaque = avisos.filter(destaque=True).first()
    total_novos = avisos.count()

    eventos = EventoAcademico.objects.all().order_by('data', 'horario')
    
    eventos_gerais = EventoGeral.objects.order_by('data_inicio')[:5]

    contatos = ContatoProfessor.objects.all().order_by('disciplina')

    # Estatísticas
    total_disciplinas = Aula.objects.values('disciplina').distinct().count()
    total_alunos = Usuarios.objects.count()
    total_provas = EventoAcademico.objects.filter(tipo__iexact='Prova').count()
    total_tarefas = EventoAcademico.objects.filter(tipo__iexact='Trabalho').count()

    contexto = {
        'usuario': usuario,
        'dias_nomes': DIAS_SEMANA.items(),
        'aulas_por_dia': aulas_por_dia,
        'materiais': materiais,
        'materiais_por_disciplina': materiais_por_disciplina,
        'avisos': avisos,
        'aviso_destaque': aviso_destaque,
        'total_novos': total_novos,
        'eventos': eventos,
        'eventos_gerais': eventos_gerais,
        'contatos': contatos,

        'total_disciplinas': total_disciplinas,
        'total_alunos': total_alunos,
        'total_provas': total_provas,
        'total_tarefas': total_tarefas,
    }

    return contexto


def home(request):
    contexto = get_contexto_geral(request)
    if isinstance(contexto, HttpResponseRedirect):
        return contexto
    return render(request, 'index.html', contexto)


def todos_materiais(request):
    contexto = get_contexto_geral(request)
    if isinstance(contexto, HttpResponseRedirect):
        return contexto
    return render(request, 'index.html', contexto)


def todos_avisos(request):
    contexto = get_contexto_geral(request)
    if isinstance(contexto, HttpResponseRedirect):
        return contexto
    return render(request, 'index.html', contexto)


def logout(request):
    request.session.flush()
    return redirect('login')
