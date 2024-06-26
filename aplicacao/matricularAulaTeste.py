import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

# Função para matricular aluno em aula utilizando tkinter
def matricular_aula():
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    # Solicitar o nome do aluno usando um diálogo de entrada
    nome = simpledialog.askstring("Matricular Aluno", "Digite o nome do Aluno:")

    if not nome:
        conn.close()
        return
    
    nome = nome.title()

    # Verificar se o aluno está cadastrado
    ids = cursor.execute("""SELECT id_aluno FROM tb_Aluno WHERE nome_aluno = ?""", (nome,)).fetchall()
    if not ids:
        messagebox.showerror("Erro", "Este aluno não está cadastrado. Cadastre-o e depois matricule-o em uma aula.")
        conn.close()
        return None 
    
    id_aluno = ids[0][0]

    # Obter todas as aulas disponíveis
    aulas = cursor.execute("""SELECT descricao FROM tb_aulas_treinos """).fetchall()

    # Mostrar as aulas disponíveis em um diálogo de escolha
    aula_escolhida = simpledialog.askstring("Matricular Aluno", "Escolha a aula para matricular o aluno:", 
                                            initialvalue=aulas[0][0] if aulas else "")

    if not aula_escolhida:
        conn.close()
        return
    
    while aula_escolhida not in [aula[0] for aula in aulas]:
        messagebox.showerror("Erro", "Nome da aula inválido! Tente novamente.")
        aula_escolhida = simpledialog.askstring("Matricular Aluno", "Escolha a aula para matricular o aluno:", 
                                                initialvalue=aulas[0][0] if aulas else "")
        if not aula_escolhida:
            conn.close()
            return

    id_aula = cursor.execute("""SELECT idAula FROM tb_aulas_treinos WHERE descricao = ?""", (aula_escolhida,)).fetchone()[0]
    
    # Inserir a matrícula do aluno na tabela rel_aula_aluno
    cursor.execute("""INSERT INTO rel_aula_aluno (aluno_id, aula_id)
                      VALUES (?, ?) """, (id_aluno, id_aula))
    
    # Atualizar vagas disponíveis na tabela tb_aulas_treinos
    cursor.execute("""
        UPDATE tb_aulas_treinos
        SET vagas_disponiveis = max_vagas - (
            SELECT COUNT(r.aluno_id)
            FROM rel_aula_aluno r
            WHERE r.aula_id = tb_aulas_treinos.idAula
        )
        WHERE idAula = ?
    """, (id_aula,))

    messagebox.showinfo("Sucesso", "Aluno matriculado com sucesso!")
    conn.commit()
    conn.close()