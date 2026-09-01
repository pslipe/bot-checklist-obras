import sqlite3

def conectar():
    conexao = sqlite3.connect("checklist.db")

    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS pendencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT, status TEXT, local TEXT, prazo TEXT, prioridade TEXT, foto_file_id TEXT)""")
    conexao.commit()
    conexao.close()

def verificar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT name FROM sqlite_master
        WHERE type='table'""")
    tabelas = cursor.fetchall()
    print(tabelas)
    conexao.close()

def criar_pendencia(descricao, local, prioridade, prazo, foto_file_id, grupo_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""INSERT INTO pendencias (descricao, status, local, prioridade, prazo, foto_file_id, grupo_id) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (descricao, "Pendente", local, prioridade, prazo, foto_file_id, grupo_id))
    id_pendencia = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return id_pendencia

def buscar_pendencias(grupo_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            descricao,
            status,
            local,
            prioridade,
            prazo,
            foto_file_id
        FROM pendencias
        WHERE status = ?
        AND grupo_id = ?
    """, ("Pendente",grupo_id))

    pendencias = cursor.fetchall()
    conexao.close()

    return pendencias

def atualizar_pendencia_concluida(id_pendencia, grupo_id):
    conexao = conectar()
    cursor = conexao.cursor() 
    cursor.execute("""UPDATE pendencias 
        SET status = ?
        WHERE id = ?
        AND grupo_id = ?""", ("Concluido", id_pendencia, grupo_id))
    linhas_alteradas = cursor.rowcount
    conexao.commit()
    conexao.close()
    return linhas_alteradas

def verifica_coluna():
    conexao = conectar()
    cursor = conexao.cursor() 
    cursor.execute("""PRAGMA table_info(pendencias)""")
    colunas = cursor.fetchall()
    nomes_colunas = [coluna[1] for coluna in colunas]
    if "local" not in nomes_colunas:
        cursor.execute("""ALTER TABLE pendencias ADD COLUMN local TEXT""")
    else:
        print("Coluna ja existe")
    if "prazo" not in nomes_colunas:
            cursor.execute("""ALTER TABLE pendencias ADD COLUMN prazo TEXT""")
    else:
        print("Coluna ja existe")
    if "prioridade" not in nomes_colunas:
            cursor.execute("""ALTER TABLE pendencias ADD COLUMN prioridade TEXT""")
    else:
        print("Coluna ja existe")
    if "foto_file_id" not in nomes_colunas:
            cursor.execute("""ALTER TABLE pendencias ADD COLUMN foto_file_id TEXT""")
    else:
        print("Coluna ja existe")
    if "grupo_id" not in nomes_colunas:
        cursor.execute("""
        ALTER TABLE pendencias
        ADD COLUMN grupo_id INTEGER
        """)
    else:
        print("Coluna grupo_id já existe")

    conexao.commit()
    conexao.close()
    print(nomes_colunas)



criar_tabela()

verifica_coluna()
