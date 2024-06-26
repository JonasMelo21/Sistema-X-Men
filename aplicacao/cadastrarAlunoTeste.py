import random
import re
import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox

def cadastrar_aluno(parent):
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    aluno = []

    # Recebe o nome do aluno e valida
    while True:
        nome = simpledialog.askstring("Cadastrar Aluno", "Digite o nome do aluno:", parent=parent).strip()
        if re.match(r'^[A-Za-z\s]+$', nome):
            break
        else:
            messagebox.showwarning("Aviso", "O nome deve conter apenas letras e espaços em branco")

    # Verificar se o aluno já não está cadastrado
    linhas = cursor.execute("""SELECT nome_aluno FROM tb_Aluno WHERE nome_aluno = ?""", (nome,)).fetchall()
    if linhas == []:
        aluno.append(nome.title())
    else:
        messagebox.showinfo("Informação", "Aluno(a) já cadastrado")
        return

    # Recebe a idade do aluno e valida
    while True:
        try:
            idade = int(simpledialog.askstring("Cadastrar Aluno", "Digite a idade do aluno:", parent=parent))
            if idade > 0:
                break
            else:
                messagebox.showwarning("Aviso", "A idade deve ser um número maior que 0")
        except ValueError:
            messagebox.showwarning("Aviso", "A idade deve ser um número")

    aluno.append(idade)

    # Gera número de matrícula único
    matricula = str(random.randint(100000, 10000000))
    linhas = cursor.execute("""SELECT matricula FROM tb_Aluno""").fetchall()
    matriculas = [i[0] for i in linhas]

    while matricula in matriculas:
        matricula = str(random.randint(100000, 10000000))

    aluno.append(matricula)

    # Receber e validar o nível de poder
    niveis_poder = ["Omega", "Alfa", "Beta", "Gama", "Delta", "Epsilon"]
    while True:
        poder = simpledialog.askstring("Cadastrar Aluno", "Digite o nível de poder:\n- Omega\n- Alfa\n- Beta\n- Gama\n- Delta\n- Epsilon", parent=parent).strip()
        if poder in niveis_poder:
            break
        else:
            messagebox.showwarning("Aviso", "O nível de poder deve ser uma das opções fornecidas")

    aluno.append(poder.title())

    # Receber e validar o status de matrícula
    status_opcoes = ['Ativo', 'Inativo', 'Transferido', 'Graduado', 'Suspenso', 'Expulso']
    while True:
        status = simpledialog.askstring("Cadastrar Aluno", "Digite o status de matrícula do aluno:\n- Ativo\n- Inativo\n- Transferido\n- Graduado\n- Suspenso\n- Expulso", parent=parent).strip()
        if status in status_opcoes:
            break
        else:
            messagebox.showwarning("Aviso", "O status de matrícula deve ser uma das opções fornecidas")

    aluno.append(status)

    # Receber e validar a habilidade do aluno
    while True:
        habilidade = simpledialog.askstring("Cadastrar Aluno", "Digite a habilidade do aluno:", parent=parent).strip()
        if len(habilidade) <= 45 and re.match(r'^[A-Za-z\s]+$', habilidade):
            break
        else:
            messagebox.showwarning("Aviso", "A habilidade deve ter até 45 caracteres e conter apenas letras e espaços em branco")

    aluno.append(habilidade.title())

    # Selecionando e montando uma lista das equipes disponíveis
    linhas = cursor.execute("""SELECT nome FROM tb_equipe""").fetchall()
    equipes = [i[0] for i in linhas]

    # Recebendo e validando a equipe do aluno
    while True:
        equipe = simpledialog.askstring("Cadastrar Aluno", "As equipes disponíveis são: " + ", ".join(equipes) + "\nDigite o nome da equipe que o aluno faz parte, se aplicável, senão, digite 0:", parent=parent)
        if equipe == "0":
            aluno.append(0)
            break
        elif equipe in equipes:
            idEquipe = cursor.execute("""SELECT id_equipe FROM tb_equipe WHERE nome = ?""", (equipe,)).fetchall()
            aluno.append(idEquipe[0][0])
            break
        else:
            messagebox.showwarning("Aviso", "Equipe inválida. Escolha uma das opções fornecidas ou digite 0.")

    cursor.execute("""INSERT INTO tb_Aluno(nome_aluno, idade_aluno, matricula, nivel_poder, status, habilidade_aluno, idEquipe) VALUES(?, ?, ?, ?, ?, ?, ?)""", tuple(aluno))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
