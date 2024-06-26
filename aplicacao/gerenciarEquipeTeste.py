import tkinter as tk
from tkinter import simpledialog, messagebox

def buscarEquipeNome(parent):
    # Conectando ao banco de dados
    import sqlite3
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    # Mostrando as equipes disponíveis para busca
    equipes_no_banco = cursor.execute("""SELECT nome FROM tb_equipe""").fetchall()
    equipe_names = [i[0] for i in equipes_no_banco]
    
    if not equipe_names:
        messagebox.showinfo("Informação", "Não há equipes disponíveis para busca.")
        return
    
    messagebox.showinfo("Equipes Disponíveis", "As equipes disponíveis para busca são: \n" + "\n".join(equipe_names))
    
    # Solicitando o nome da equipe
    nome_equipe = simpledialog.askstring("Buscar Equipe", "Digite o nome da equipe da qual deseja ver as informações:", parent=parent)
    
    if not nome_equipe:
        return
    
    nome_equipe = nome_equipe.title()
    equipe = cursor.execute("""SELECT 
                            e.nome,
                            i.nome_instrutor,
                            a.nome_aluno FROM
                            tb_equipe e 
                            INNER JOIN tb_instrutor i ON e.idInstrutor = i.id_instrutor
                            INNER JOIN tb_Aluno a ON e.id_equipe = a.idEquipe 
                            WHERE e.nome = ?""", (nome_equipe,)).fetchall()
    
    if not equipe:
        messagebox.showinfo("Informação", "Nenhuma equipe encontrada com o nome fornecido.")
        return

    # Exibindo informações da equipe
    info = f"\nNome da Equipe: {nome_equipe}\nInstrutor Responsável: {equipe[0][1]}\nAlunos:"
    for i in equipe:
        info += f"\n\t - {i[2]}"
    
    messagebox.showinfo("Informação da Equipe", info)
    conn.close()

def buscarEquipeInstrutor(parent):
    # Conectando ao banco de dados
    import sqlite3
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    # Mostrando os instrutores com equipes associadas
    instrutores = cursor.execute("""SELECT i.nome_instrutor FROM tb_instrutor i INNER JOIN tb_equipe e ON e.idInstrutor = i.id_instrutor""").fetchall()
    instrutor_names = [i[0] for i in instrutores]
    
    if not instrutor_names:
        messagebox.showinfo("Informação", "Não há instrutores responsáveis por equipes.")
        return
    
    messagebox.showinfo("Instrutores Disponíveis", "Os instrutores responsáveis por equipes são: \n" + "\n".join(instrutor_names))
    
    # Solicitando o nome do instrutor
    nome_instrutor = simpledialog.askstring("Buscar Equipe por Instrutor", "Digite o nome do instrutor do qual deseja buscar suas equipes:", parent=parent)
    
    if not nome_instrutor:
        return
    
    nome_instrutor = nome_instrutor.title()
    result = cursor.execute("""SELECT 
                      i.nome_instrutor,
                      e.nome,
                      a.nome_aluno
                      FROM tb_instrutor i 
                      INNER JOIN tb_equipe e ON e.idInstrutor = i.id_instrutor
                      INNER JOIN tb_Aluno a ON a.idEquipe = e.id_equipe
                      WHERE i.nome_instrutor = ?""", (nome_instrutor,)).fetchall()
    
    if not result:
        messagebox.showinfo("Informação", "Nenhuma equipe encontrada para o instrutor fornecido.")
        return

    # Exibindo informações do instrutor e suas equipes
    info = f"\nInstrutor: {result[0][0]}\nEquipe: {result[0][1]}\nAlunos:"
    for i in result:
        info += f"\n\t - {i[2]}"
    
    messagebox.showinfo("Informação da Equipe do Instrutor", info)
    conn.close()

def cadastrarEquipe(parent):
    # Biblioteca de expressões regulares para validar o nome da equipe
    import re 

    # Conectando ao banco de dados
    import sqlite3 
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    # Recebendo e validando o nome da equipe
    while True:
        nome = simpledialog.askstring("Cadastrar Equipe", "Digite o nome da Equipe:", parent=parent)
        if not nome:
            return
        nome = nome.title()
        if re.match(r'^[A-Za-z\s]+$', nome):
            break
        else:
            messagebox.showwarning("Aviso", "O nome da equipe deve conter apenas letras e espaços em branco")

    # Mostrando os instrutores disponíveis
    linhas = cursor.execute("""SELECT nome_instrutor from tb_instrutor """).fetchall()
    instrutores = [i[0] for i in linhas]
    
    if not instrutores:
        messagebox.showinfo("Informação", "Não há instrutores disponíveis.")
        return

    messagebox.showinfo("Instrutores Disponíveis", "Estes são os instrutores disponíveis: \n" + "\n".join(instrutores))
    
    # Recebendo do usuário e validando o nome do instrutor
    while True:
        instrutor = simpledialog.askstring("Cadastrar Equipe", "Digite o nome do instrutor da equipe:", parent=parent)
        if not instrutor:
            return
        instrutor = instrutor.title()
        if instrutor in instrutores:
            break
        else:
            messagebox.showwarning("Aviso", "Instrutor inválido. Por favor, escolha um instrutor disponível.")
    
    # Selecionando o id do instrutor do banco de dados
    result = cursor.execute("""SELECT id_instrutor from tb_instrutor WHERE nome_instrutor = ? """, (instrutor,)).fetchall()
    
    if not result:
        messagebox.showwarning("Aviso", "Instrutor inválido.")
        return

    id = result[0][0] # Result é uma lista de tuplas aninhadas, então vou selecionar o id que é o primeiro elemento da 1a tupla

    # Inserindo a equipe no banco de dados
    cursor.execute("""
                        INSERT INTO tb_equipe(nome,idInstrutor)
                        VALUES
                        (?,?)
                        """, (nome, id))
    
    # Salvando as alterações e fechando a conexão com o banco de dados
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Equipe cadastrada com sucesso!")
