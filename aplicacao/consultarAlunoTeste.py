import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox

def consultar_aluno_nome(parent):
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    nome = simpledialog.askstring("Consultar Aluno", "Digite o nome do aluno a ser consultado:", parent=parent).strip().title()
    nomes = cursor.execute("""SELECT 
                           a.nome_aluno,
                           a.idade_aluno,
                           a.matricula,
                           a.nivel_poder, 
                           a.status,
                           a.habilidade_aluno,
                           e.nome
                           FROM tb_Aluno a
                           INNER JOIN tb_equipe e
                           ON a.idEquipe =  e.id_equipe
                           WHERE nome_aluno = ?""",(nome,)).fetchall()
    
    if nomes:
        info = f"\n\nNome do Aluno: {nomes[0][0]}\n"
        info += f"Idade: {nomes[0][1]}\n"
        info += f"Matrícula do Aluno: {nomes[0][2]}\n"
        info += f"Nivel de Poder: {nomes[0][3]}\n"
        info += f"Status de Matrícula: {nomes[0][4]}\n"
        info += f"Habilidade do Aluno: {nomes[0][5]}\n"
        info += f"Equipe do Aluno: {nomes[0][-1]}\n"
        messagebox.showinfo("Informações do Aluno", info)
    else:
        messagebox.showwarning("Aviso", "Aluno não encontrado")

    conn.close()

def consultar_aluno_equipe(parent):
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()
    
    linhas = cursor.execute("""SELECT DISTINCT
                            e.nome 
                            FROM tb_Aluno a
                            INNER JOIN tb_equipe e
                            ON a.idEquipe = e.id_equipe
                            """).fetchall()
    
    equipes = [i[0].title() for i in linhas]
    
    equipe = simpledialog.askstring("Consultar Aluno", "As equipes disponíveis são:\n" + ", ".join(equipes) + "\nDigite o nome da equipe:", parent=parent).strip().title()
    if equipe in equipes:
        nomes = cursor.execute("""SELECT a.nome_aluno FROM tb_Aluno a INNER JOIN tb_equipe e ON a.idEquipe = e.id_equipe WHERE e.nome = ?""",(equipe,)).fetchall()
        
        resultado = "\nNome da equipe: " + equipe + "\n\nAlunos da Equipe:\n"
        for i in nomes: 
            resultado += "\t - " + i[0] + "\n"
        
        messagebox.showinfo("Alunos da Equipe", resultado)
    else:
        messagebox.showwarning("Aviso", "Nome de equipe inválido")

    conn.close()
