import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import re
from datetime import datetime

# Funções de Gerenciamento de Missões
def buscarMissaoObjetivo(janela):
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    # Mostrando os objetivos de diferentes missões
    linhas = cursor.execute("SELECT objetivo_missao FROM tb_missao").fetchall()
    missoes = [linha[0] for linha in linhas]

    if missoes:
        objetivos_texto = "\n".join(missoes)
        messagebox.showinfo("Objetivos das Missões", f"Objetivos disponíveis:\n\n{objetivos_texto}")
    else:
        messagebox.showinfo("Objetivos das Missões", "Nenhuma missão encontrada no banco de dados.")
        conn.close()
        return

    def mostrar_missao(objetivo):
        obj = cursor.execute("""
            SELECT m.objetivo_missao, m.dt_inicio, m.dt_fim, m.status_missao, e.nome 
            FROM tb_missao m
            INNER JOIN tb_equipe e ON e.id_equipe = m.id_Equipe
            WHERE m.objetivo_missao = ? 
        """, (objetivo,)).fetchall()

        if obj:
            info = f"Objetivo da Missão: {obj[0][0]}\nData de Início: {obj[0][1]}\nData de Fim: {obj[0][2]}\nStatus da Missão: {obj[0][3]}\nNome da Equipe: {obj[0][4]}"
            messagebox.showinfo("Informações da Missão", info)
        else:
            messagebox.showerror("Erro", "Missão inválida")

    objetivo = simpledialog.askstring("Buscar Missão", "Digite uma missão para visualizar suas informações:", parent=janela)
    if objetivo:
        mostrar_missao(objetivo.title())

    conn.close()

def buscarMissaoEquipe(janela):
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    # Buscar equipes disponíveis
    equipes = cursor.execute("""
        SELECT DISTINCT e.nome 
        FROM tb_equipe e 
        INNER JOIN tb_missao m ON e.id_equipe = m.id_Equipe
    """).fetchall()
    equipe_nomes = [equipe[0] for equipe in equipes]

    if equipe_nomes:
        equipes_texto = "\n".join(equipe_nomes)
        messagebox.showinfo("Equipes Disponíveis", f"Equipes disponíveis:\n\n{equipes_texto}")
    else:
        messagebox.showinfo("Equipes Disponíveis", "Nenhuma equipe encontrada no banco de dados.")
        conn.close()
        return

    def mostrar_missoes(equipe_desejada):
        equipe = cursor.execute("""
            SELECT e.nome, m.objetivo_missao, m.status_missao, m.dt_inicio, m.dt_fim
            FROM tb_equipe e
            INNER JOIN tb_missao m ON m.id_Equipe = e.id_equipe
            WHERE e.nome = ?
        """, (equipe_desejada,)).fetchall()

        if equipe:
            info = f"Nome da Equipe: {equipe[0][0]}\n"
            for missao in equipe:
                info += f"\nObjetivo da Missão: {missao[1]}\nStatus da Missão: {missao[2]}\nData de Início: {missao[3]}\nData de Fim: {missao[4]}\n"
            messagebox.showinfo("Informações da Equipe", info)
        else:
            messagebox.showerror("Erro", "Equipe inválida")

    equipe_desejada = simpledialog.askstring("Buscar Missão por Equipe", "Digite a equipe para visualizar suas missões:", parent=janela)
    if equipe_desejada:
        mostrar_missoes(equipe_desejada.title())

    conn.close()

def comparar_datas(data_inicio, data_fim):
    formato = '%Y-%m-%d'
    dt_inicio = datetime.strptime(data_inicio, formato)
    dt_fim = datetime.strptime(data_fim, formato)
    return dt_inicio < dt_fim

def cadastrarMissao(janela):
    conn = sqlite3.connect("XMen.db")
    cursor = conn.cursor()

    def validar_objetivo(objetivo):
        return re.match(r'^[A-Za-z\s]+$', objetivo) and not objetivo.isspace() and len(objetivo) <= 45

    def validar_data(data):
        return re.match(r'^\d{4}-\d{2}-\d{2}$', data)

    def validar_status(status):
        return status in ["Sucesso", "Falha", "Em Andamento"]

    objetivo = simpledialog.askstring("Cadastrar Missão", "Digite o objetivo da missão:", parent=janela).title()
    while not validar_objetivo(objetivo):
        messagebox.showerror("Erro", "O objetivo da missão deve conter apenas letras e espaços em branco e no máximo 45 caracteres")
        objetivo = simpledialog.askstring("Cadastrar Missão", "Digite o objetivo da missão:", parent=janela).title()

    data_inicio = simpledialog.askstring("Cadastrar Missão", "Digite a data de início da missão (AAAA-MM-DD):", parent=janela)
    while not validar_data(data_inicio):
        messagebox.showerror("Erro", "Digite a data no formato válido (AAAA-MM-DD)")
        data_inicio = simpledialog.askstring("Cadastrar Missão", "Digite a data de início da missão (AAAA-MM-DD):", parent=janela)

    data_fim = simpledialog.askstring("Cadastrar Missão", "Digite a data de fim da missão (AAAA-MM-DD):", parent=janela)
    while not validar_data(data_fim) or not comparar_datas(data_inicio, data_fim):
        messagebox.showerror("Erro", "A data de fim deve ser maior que a data de início e no formato válido (AAAA-MM-DD)")
        data_fim = simpledialog.askstring("Cadastrar Missão", "Digite a data de fim da missão (AAAA-MM-DD):", parent=janela)

    status = simpledialog.askstring("Cadastrar Missão", "Digite o status da missão (Sucesso, Falha, Em Andamento):", parent=janela).title()
    while not validar_status(status):
        messagebox.showerror("Erro", "Status inválido")
        status = simpledialog.askstring("Cadastrar Missão", "Digite o status da missão (Sucesso, Falha, Em Andamento):", parent=janela).title()

    equipes = cursor.execute("SELECT nome FROM tb_equipe").fetchall()
    equipe_nomes = [equipe[0] for equipe in equipes]

    equipe = simpledialog.askstring("Cadastrar Missão", "Digite o nome da equipe que receberá a missão:", parent=janela).title()
    while equipe not in equipe_nomes:
        messagebox.showerror("Erro", "Nome inválido")
        equipe = simpledialog.askstring("Cadastrar Missão", "Digite o nome da equipe que receberá a missão:", parent=janela).title()

    id_equipe = cursor.execute("SELECT id_equipe FROM tb_equipe WHERE nome = ?", (equipe,)).fetchone()[0]

    cursor.execute("""
        INSERT INTO tb_missao (objetivo_missao, dt_inicio, dt_fim, status_missao, id_Equipe) 
        VALUES (?, ?, ?, ?, ?)
    """, (objetivo, data_inicio, data_fim, status, id_equipe))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Missão cadastrada com sucesso!")
