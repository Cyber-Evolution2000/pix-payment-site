import sqlite3
import os
import json

class Database:
    def __init__(self, db_name="certificados.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Inicializa o banco de dados e cria a tabela se não existir"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                curso TEXT NOT NULL,
                data_emissao TEXT NOT NULL,
                validade TEXT NOT NULL,
                link_certificado TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("BANCO DE DADOS INICIALIZADO!")
    
    def cadastrar_aluno(self, nome, cpf, curso, data_emissao, validade, link_certificado):
        """Cadastra um novo aluno no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO alunos (nome, cpf, curso, data_emissao, validade, link_certificado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, curso, data_emissao, validade, link_certificado))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False  # CPF já existe
        except Exception as e:
            conn.close()
            print(f"ERRO AO CADASTRAR: {e}")
            return False
    
    def listar_alunos(self):
        """Retorna todos os alunos cadastrados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM alunos ORDER BY nome')
        alunos = cursor.fetchall()
        
        conn.close()
        return alunos
    
    def buscar_por_cpf(self, cpf):
        """Busca um aluno pelo CPF"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM alunos WHERE cpf = ?', (cpf,))
        aluno = cursor.fetchone()
        
        conn.close()
        
        if aluno:
            return {
                'id': aluno[0],
                'nome': aluno[1],
                'cpf': aluno[2],
                'curso': aluno[3],
                'data_emissao': aluno[4],
                'validade': aluno[5],
                'link': aluno[6]
            }
        return None
    
    def buscar_por_id(self, id_aluno):
        """Busca um aluno pelo ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM alunos WHERE id = ?', (id_aluno,))
        aluno = cursor.fetchone()
        
        conn.close()
        
        if aluno:
            return {
                'id': aluno[0],
                'nome': aluno[1],
                'cpf': aluno[2],
                'curso': aluno[3],
                'data_emissao': aluno[4],
                'validade': aluno[5],
                'link': aluno[6]
            }
        return None
    
    def editar_aluno(self, id_aluno, nome, curso, data_emissao, validade, link_certificado):
        """Edita os dados de um aluno"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE alunos 
                SET nome = ?, curso = ?, data_emissao = ?, validade = ?, link_certificado = ?
                WHERE id = ?
            ''', (nome, curso, data_emissao, validade, link_certificado, id_aluno))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"ERRO AO EDITAR: {e}")
            return False
    
    def excluir_aluno(self, id_aluno):
        """Exclui um aluno do banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM alunos WHERE id = ?', (id_aluno,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"ERRO AO EXCLUIR: {e}")
            return False
    
    def exportar_para_json(self):
        """Exporta os dados para JSON (para o HTML usar)"""
        alunos = self.listar_alunos()
        dados = []
        
        for aluno in alunos:
            dados.append({
                'nome': aluno[1],
                'cpf': aluno[2],
                'curso': aluno[3],
                'data_emissao': aluno[4],
                'validade': aluno[5],
                'link': aluno[6]
            })
        
        # Salvar em arquivo JSON
        with open('certificados.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        # Gerar arquivo JavaScript
        with open('certificados.js', 'w', encoding='utf-8') as f:
            f.write('const certificadosCadastrados = ')
            json.dump(dados, f, ensure_ascii=False, indent=2)
            f.write(';')
        
        print(f"DADOS EXPORTADOS: {len(dados)} ALUNO(S) NO BANCO DE DADOS")
        return len(dados)

def cadastrar_aluno_interativo():
    """Função para cadastrar um novo aluno"""
    print("\n" + "="*50)
    print("           CADASTRO DE ALUNO")
    print("="*50)
    
    # Solicitar dados do aluno
    nome = input("NOME COMPLETO: ").strip()
    while not nome:
        print("NOME E OBRIGATORIO!")
        nome = input("NOME COMPLETO: ").strip()
    
    cpf = input("CPF (APENAS NUMEROS): ").strip()
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        print("CPF DEVE TER 11 DIGITOS!")
        return
    
    curso = input("CURSO: ").strip()
    while not curso:
        print("CURSO E OBRIGATORIO!")
        curso = input("CURSO: ").strip()
    
    data_emissao = input("DATA DE EMISSAO (DD/MM/AAAA): ").strip()
    while not data_emissao:
        print("DATA DE EMISSAO E OBRIGATORIA!")
        data_emissao = input("DATA DE EMISSAO (DD/MM/AAAA): ").strip()
    
    validade = input("DATA DE VALIDADE (DD/MM/AAAA): ").strip()
    while not validade:
        print("DATA DE VALIDADE E OBRIGATORIA!")
        validade = input("DATA DE VALIDADE (DD/MM/AAAA): ").strip()
    
    link_certificado = input("LINK DO CERTIFICADO: ").strip()
    while not link_certificado:
        print("LINK DO CERTIFICADO E OBRIGATORIO!")
        link_certificado = input("LINK DO CERTIFICADO: ").strip()
    
    # Cadastrar no banco de dados
    db = Database()
    sucesso = db.cadastrar_aluno(nome, cpf, curso, data_emissao, validade, link_certificado)
    
    if sucesso:
        print(f"\nALUNO CADASTRADO COM SUCESSO!")
        print(f"NOME: {nome}")
        print(f"CPF: {cpf}")
        print(f"CURSO: {curso}")
        print(f"VALIDADE: {validade}")
        
        # Exportar automaticamente para JSON/JS
        db.exportar_para_json()
        
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
    else:
        print("ERRO: CPF JA CADASTRADO NO SISTEMA!")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")

def listar_alunos_interativo():
    """Lista todos os alunos cadastrados"""
    db = Database()
    alunos = db.listar_alunos()
    
    print("\n" + "="*50)
    print("           ALUNOS CADASTRADOS")
    print("="*50)
    
    if not alunos:
        print("NENHUM ALUNO CADASTRADO.")
    else:
        print(f"TOTAL DE {len(alunos)} ALUNO(S) CADASTRADO(S):\n")
        
        for i, aluno in enumerate(alunos, 1):
            print(f"{i}. {aluno[1]}")
            print(f"   ID: {aluno[0]}")
            print(f"   CPF: {aluno[2]}")
            print(f"   CURSO: {aluno[3]}")
            print(f"   EMISSAO: {aluno[4]} | VALIDADE: {aluno[5]}")
            print(f"   LINK: {aluno[6]}")
            print("-" * 40)
    
    input("\nPRESSIONE ENTER PARA CONTINUAR...")

def editar_aluno_interativo():
    """Função para editar um aluno existente"""
    print("\n" + "="*50)
    print("           EDITAR ALUNO")
    print("="*50)
    
    db = Database()
    
    # Listar alunos primeiro
    alunos = db.listar_alunos()
    if not alunos:
        print("NENHUM ALUNO CADASTRADO PARA EDITAR.")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
        return
    
    print("ALUNOS CADASTRADOS:\n")
    for aluno in alunos:
        print(f"ID: {aluno[0]} | {aluno[1]} | CPF: {aluno[2]}")
    
    try:
        id_aluno = int(input("\nDIGITE O ID DO ALUNO QUE DESEJA EDITAR: "))
    except ValueError:
        print("ID INVALIDO!")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
        return
    
    # Buscar aluno
    aluno = db.buscar_por_id(id_aluno)
    if not aluno:
        print("ALUNO NAO ENCONTRADO!")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
        return
    
    print(f"\nEDITANDO ALUNO: {aluno['nome']}")
    print("DEIXE EM BRANCO PARA MANTER O VALOR ATUAL\n")
    
    # Solicitar novos dados
    nome = input(f"NOME COMPLETO [{aluno['nome']}]: ").strip()
    if not nome:
        nome = aluno['nome']
    
    curso = input(f"CURSO [{aluno['curso']}]: ").strip()
    if not curso:
        curso = aluno['curso']
    
    data_emissao = input(f"DATA DE EMISSAO [{aluno['data_emissao']}]: ").strip()
    if not data_emissao:
        data_emissao = aluno['data_emissao']
    
    validade = input(f"DATA DE VALIDADE [{aluno['validade']}]: ").strip()
    if not validade:
        validade = aluno['validade']
    
    link_certificado = input(f"LINK DO CERTIFICADO [{aluno['link']}]: ").strip()
    if not link_certificado:
        link_certificado = aluno['link']
    
    # Confirmar edição
    confirmar = input(f"\nCONFIRMAR EDICAO DO ALUNO {aluno['nome']}? (S/N): ").strip().upper()
    
    if confirmar == 'S':
        sucesso = db.editar_aluno(id_aluno, nome, curso, data_emissao, validade, link_certificado)
        if sucesso:
            print("ALUNO EDITADO COM SUCESSO!")
            # Exportar automaticamente
            db.exportar_para_json()
        else:
            print("ERRO AO EDITAR ALUNO!")
    else:
        print("EDICAO CANCELADA!")
    
    input("\nPRESSIONE ENTER PARA CONTINUAR...")

def excluir_aluno_interativo():
    """Função para excluir um aluno"""
    print("\n" + "="*50)
    print("           EXCLUIR ALUNO")
    print("="*50)
    
    db = Database()
    
    # Listar alunos primeiro
    alunos = db.listar_alunos()
    if not alunos:
        print("NENHUM ALUNO CADASTRADO PARA EXCLUIR.")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
        return
    
    print("ALUNOS CADASTRADOS:\n")
    for aluno in alunos:
        print(f"ID: {aluno[0]} | {aluno[1]} | CPF: {aluno[2]}")
    
    try:
        id_aluno = int(input("\nDIGITE O ID DO ALUNO QUE DESEJA EXCLUIR: "))
    except ValueError:
        print("ID INVALIDO!")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
        return
    
    # Buscar aluno
    aluno = db.buscar_por_id(id_aluno)
    if not aluno:
        print("ALUNO NAO ENCONTRADO!")
        input("\nPRESSIONE ENTER PARA CONTINUAR...")
        return
    
    # Confirmar exclusão
    print(f"\nVOCE VAI EXCLUIR O ALUNO:")
    print(f"NOME: {aluno['nome']}")
    print(f"CPF: {aluno['cpf']}")
    print(f"CURSO: {aluno['curso']}")
    
    confirmar = input(f"\nCONFIRMAR EXCLUSAO? ESTA ACAO NAO PODE SER DESFEITA! (S/N): ").strip().upper()
    
    if confirmar == 'S':
        sucesso = db.excluir_aluno(id_aluno)
        if sucesso:
            print("ALUNO EXCLUIDO COM SUCESSO!")
            # Exportar automaticamente
            db.exportar_para_json()
        else:
            print("ERRO AO EXCLUIR ALUNO!")
    else:
        print("EXCLUSAO CANCELADA!")
    
    input("\nPRESSIONE ENTER PARA CONTINUAR...")

def menu_principal():
    """Menu principal do sistema"""
    # Inicializar banco
    db = Database()
    
    while True:
        print("\n" + "="*50)
        print("           SISTEMA DE CADASTRO DE ALUNOS")
        print("="*50)
        print("1. CADASTRAR NOVO ALUNO")
        print("2. LISTAR ALUNOS CADASTRADOS")
        print("3. EDITAR ALUNO")
        print("4. EXCLUIR ALUNO")
        print("5. SAIR DO SISTEMA")
        
        opcao = input("\nDIGITE SUA OPCAO (1-5): ").strip()
        
        if opcao == "1":
            cadastrar_aluno_interativo()
        elif opcao == "2":
            listar_alunos_interativo()
        elif opcao == "3":
            editar_aluno_interativo()
        elif opcao == "4":
            excluir_aluno_interativo()
        elif opcao == "5":
            print("\nSAINDO DO SISTEMA... ATE LOGO!")
            break
        else:
            print("OPCAO INVALIDA! DIGITE 1, 2, 3, 4 OU 5.")
            input("PRESSIONE ENTER PARA TENTAR NOVAMENTE...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPROGRAMA INTERROMPIDO PELO USUARIO. ATE LOGO!")
    except Exception as e:
        print(f"\nERRO INESPERADO: {e}")
        input("PRESSIONE ENTER PARA SAIR...")