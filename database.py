import sqlite3
import os

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
            print(f"Erro ao cadastrar: {e}")
            return False
    
    def listar_alunos(self):
        """Retorna todos os alunos cadastrados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM alunos')
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
        import json
        with open('certificados.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        # Gerar arquivo JavaScript
        with open('certificados.js', 'w', encoding='utf-8') as f:
            f.write('const certificadosCadastrados = ')
            json.dump(dados, f, ensure_ascii=False, indent=2)
            f.write(';')
        
        print(f"✅ Dados exportados: {len(dados)} aluno(s) no banco de dados")

if __name__ == "__main__":
    db = Database()
    print("Banco de dados inicializado!")