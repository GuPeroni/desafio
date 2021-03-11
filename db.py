import psycopg2


class Banco:

    # Construtor da classe

    def __init__(self):       

        vHost = '127.0.0.1'
        vUser = 'postgres'
        vPass = '102225'
        vDb = 'usuarios'
        self.conn = psycopg2.connect(dbname=vDb, user=vUser, password=vPass, host=vHost)

    #Distrutor da classe(Fecha a conexão com o banco)

    def __del__(self):
        self.conn.close()

    #Retorna as consultas do banco

    def retorna_consulta(self, pComando):
        c = self.conn.cursor()
        c.execute(pComando)
        ret = c.fetchall()
        c.close()
        return ret
    
    #Executa uma query

    def executa_comando(self, pComando):
        if pComando:
            ex = self.conn.cursor()
            ex.execute(pComando)
            self.conn.commit()        

