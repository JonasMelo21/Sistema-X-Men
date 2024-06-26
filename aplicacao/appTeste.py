import tkinter as tk
from gerenciarEquipeTeste import buscarEquipeNome, buscarEquipeInstrutor, cadastrarEquipe
from cadastrarAlunoTeste import cadastrar_aluno
from consultarAlunoTeste import consultar_aluno_equipe, consultar_aluno_nome
from gerenciarMissaoTeste import buscarMissaoEquipe, buscarMissaoObjetivo, cadastrarMissao, comparar_datas
from matricularAulaTeste import matricular_aula  # Importe a função de matrícula de aulas

# Funções para os botões
def gerenciar_missoes():
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Gerenciamento de Missões")
    label = tk.Label(nova_janela, text="Escolha uma opção de Gerenciamento de Missões", font=("Arial", 14))
    label.pack(pady=10)

    botao_cadastrar_missao = tk.Button(nova_janela, text="Cadastrar Nova Missão", command=lambda: cadastrarMissao(nova_janela))
    botao_cadastrar_missao.pack(pady=5)

    botao_buscar_objetivo = tk.Button(nova_janela, text="Buscar Missão por Objetivo", command=lambda: buscarMissaoObjetivo(nova_janela))
    botao_buscar_objetivo.pack(pady=5)

    botao_buscar_equipe = tk.Button(nova_janela, text="Buscar Missão por Equipe", command=lambda: buscarMissaoEquipe(nova_janela))
    botao_buscar_equipe.pack(pady=5)

def gerenciar_equipes():
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Gerenciamento de Equipes")
    label = tk.Label(nova_janela, text="Escolha uma opção de Gerenciamento de Equipes", font=("Arial", 14))
    label.pack(pady=10)
    
    botao_buscar_nome = tk.Button(nova_janela, text="A) Buscar Equipe Pelo Nome da Equipe", command=lambda: buscarEquipeNome(nova_janela))
    botao_buscar_nome.pack(pady=5)
    
    botao_buscar_instrutor = tk.Button(nova_janela, text="B) Buscar Equipe Pelo Nome do Instrutor", command=lambda: buscarEquipeInstrutor(nova_janela))
    botao_buscar_instrutor.pack(pady=5)
    
    botao_cadastrar = tk.Button(nova_janela, text="C) Cadastrar Uma Nova Equipe", command=lambda: cadastrarEquipe(nova_janela))
    botao_cadastrar.pack(pady=5)

def gerenciar_alunos():
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Gerenciamento de Alunos")
    label = tk.Label(nova_janela, text="Escolha uma opção de Gerenciamento de Alunos", font=("Arial", 14))
    label.pack(pady=10)
    
    botao_cadastrar_aluno = tk.Button(nova_janela, text="Cadastrar Aluno", command=lambda: cadastrar_aluno(nova_janela))
    botao_cadastrar_aluno.pack(pady=5)
    
    botao_consultar_aluno_nome = tk.Button(nova_janela, text="Consultar Aluno por Nome", command=lambda: consultar_aluno_nome(nova_janela))
    botao_consultar_aluno_nome.pack(pady=5)
    
    botao_consultar_aluno_equipe = tk.Button(nova_janela, text="Consultar Aluno por Equipe", command=lambda: consultar_aluno_equipe(nova_janela))
    botao_consultar_aluno_equipe.pack(pady=5)

def gerenciar_aulas():
    nova_janela = tk.Toplevel()
    nova_janela.title("Gerenciamento de Aulas")

    # Adicionar label explicativa
    label = tk.Label(nova_janela, text="Bem-vindo ao Gerenciamento de Aulas", font=("Arial", 14))
    label.pack(pady=10)
    
    # Adicionar botão para matricular aluno
    botao_matricular_aula = tk.Button(nova_janela, text="Matricular em Aula", command=matricular_aula)
    botao_matricular_aula.pack(pady=5)

# Criação da janela principal
janela = tk.Tk()
janela.title("Sistema de Gerenciamento da Escola para Jovens Superdotados do Professor Xavier")

# Adicionando a frase
frase = tk.Label(janela, text="Salve, Mutante! Digite a Opção Desejada", font=("Arial", 14))
frase.pack(pady=10)

# Adicionando os botões
botao_missoes = tk.Button(janela, text="A) Gerenciamento de Missões", command=gerenciar_missoes)
botao_missoes.pack(pady=5)

botao_equipes = tk.Button(janela, text="B) Gerenciamento de Equipes", command=gerenciar_equipes)
botao_equipes.pack(pady=5)

botao_alunos = tk.Button(janela, text="C) Gerenciamento de Alunos", command=gerenciar_alunos)
botao_alunos.pack(pady=5)

botao_aulas = tk.Button(janela, text="D) Gerenciamento de Aulas", command=gerenciar_aulas)
botao_aulas.pack(pady=5)

# Iniciando o loop da interface
janela.mainloop()
