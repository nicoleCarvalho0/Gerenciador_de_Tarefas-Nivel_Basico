import os
import sqlite3

conexão = sqlite3.connect('tarefas.db')
cursor = conexão.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS tarefas (
                id INTeger PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                concluido BOOLEAN DEFAULT 0
                )
               """)

conexão.commit()

def cores(cores):
    '''Exibir mensagens com cores diferentes.'''
    if cores.startswith ("Nenhuma") or cores.startswith("Opção") or cores.startswith("Ocorreu"):
         print(f"\033[31m{cores}\033[m") #Vermelho
    else:
        print(f"\033[32m{cores}\033[m") #Verde
    
def voltar_menu():
    '''Função para voltar ao menu principal.'''
    input("Pressione Enter para voltar ao menu : ")
    limpar_terminal()

def submenu_lista(titulo):
    '''Exibir o título do submenu.'''
    print(f"\n{'='*20} {titulo} {'='*20}")

def sair_programa():
    '''Função para sair do programa.'''
    print("Saindo do programa...")
    exit()

def menu_lista():
    '''Exibir o menu principal.'''
    print("\n=== MENU ===")
    print("1 - Adicionar tarefa".ljust(20))
    print("2 - Ver tarefas".ljust(20))
    print("3 - Marcar como concluída".ljust(20))
    print("4 - Remover tarefa".ljust(20))
    print("0 - Sair".ljust(20))

def adicionar_tarefas():
        '''Função para adicionar uma nova tarefa.'''
        limpar_terminal()
        submenu_lista("Adicionar Tarefa")
        nome=input("Digite a tarefa: ")
        cursor.execute("INSERT INTO tarefas (nome) VALUES (?)",(nome,))
        conexão.commit()
        cores("Tarefa adicionada com sucesso!")
        voltar_menu()

def ver_tarefas():
    '''Função para visualizar as tarefas cadastradas.'''
    limpar_terminal()
    cursor.execute("SELECT id,nome,concluido FROM tarefas")
    tarefas=cursor.fetchall()
    
    if not tarefas:
      
      cores("Nenhuma tarefa cadastrada.")

    else:
      submenu_lista("Lista de Tarefas")
      for indice,tarefa in enumerate(tarefas):
        status="-Feito" if tarefa[2] else "-Pendente"
        print(f"{indice+1}-{tarefa[1]}:{status}")
        
def marcar_concluida():
    '''Função para marcar uma tarefa como concluída.'''
    limpar_terminal()
    cursor.execute("SELECT * FROM tarefas")
    tarefas=cursor.fetchall()

    if not tarefas:
        cores("Nenhuma tarefa para concluir.")
    else:
        ver_tarefas()
        try:
            submenu_lista("Marcar Tarefa como Concluída")
            numero_tarefa=int(input("Digite o número da tarefa que você concluiu:"))
            if 1<= numero_tarefa <= len(tarefas):
                id_tarefa=tarefas[numero_tarefa - 1][0]
                cursor.execute("UPDATE tarefas SET concluido = 1 WHERE id = ?", (id_tarefa,))
                conexão.commit()
                cores("Tarefa marcada como concluída!")
            else:
                print("Número de tarefa inválido.")
        except ValueError:
            print("Digite um número válido.")   

        voltar_menu() 

def remover_tarefa():
    '''Função para remover uma tarefa.'''
    limpar_terminal()
    cursor.execute("SELECT id,nome,concluido FROM tarefas")
    tarefas=cursor.fetchall()
    while True:
        if not tarefas:
            cores("Nenhuma tarefa para remover.")
        else:
            try:
                submenu_lista("Remover Tarefa")
                ver_tarefas()
                numero_tarefa=int(input("Digite o número da tarefa que deseja remover:"))
                if 1 <= numero_tarefa <= len(tarefas):
                    id_tarefa=tarefas[numero_tarefa - 1][0]
                    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
                    conexão.commit()
                    cores(f"Tarefa removida com sucesso!")
                else:
                    print("Número de tarefa inválido.")
            except Exception as e:
                cores(f"Ocorreu um erro: {e}")
        continuar=input("Deseja remover outra tarefa? (s/n): ").strip().lower()
        if continuar != 's':
            break 
        limpar_terminal()

def limpar_terminal():
    '''Função para limpar o terminal.'''
    try:
        os.system('cls')  # Para Windows
    except Exception:
        print("Não foi possível limpar o terminal. Continuando...")

while True:
    '''Loop principal do programa.'''
    menu_lista()
    
    opção=input("Escolha uma opção: ")
    try:
        if opção == '1':
             adicionar_tarefas()
        elif opção == '2':
             ver_tarefas()
             voltar_menu()
        elif opção == '3':
            marcar_concluida()
        elif opção == '4':
             remover_tarefa()
        elif opção == '0':
            sair_programa()
        else:
            cores("Opção inválida. Tente novamente.")
    except Exception as e:
        cores(f"Ocorreu um erro: {e}")


