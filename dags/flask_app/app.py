from faker import Faker
import random
from flask import Flask, jsonify


fake = Faker('pt_BR')

def tabela(qtd):
    dicionario_funcionario = {"matricula": [], "nome_funcionario": [], "cargo": [], "nivel_hierarquico": [], "regiao": [], "email": [], "telefone": []}
    dicionario_veiculo = {"matricula": [], "nome_funcionario": [], "placa_veiculo": [], "modelo_veiculo": [], "cor": []}

    matriculas_geradas = set()

    def gerar_matricula():
        matricula_numero = []
        rand = random.choice(range(2, 6))
        for i in range(rand):
            escolha = random.choice(range(0, 10))
            matricula_numero.append(str(escolha))  # Converti para string

        if matricula_numero[0] == '0':
            matricula_numero[0] = str(random.choice(range(1, 8)))
        matricula_gerada = ''.join(matricula_numero)
        
        # Garantir que a matrícula gerada seja única
        while matricula_gerada in matriculas_geradas:
            matricula_numero = []
            rand = random.choice(range(2, 6))
            for i in range(rand):
                escolha = random.choice(range(0, 10))
                matricula_numero.append(str(escolha))
            if matricula_numero[0] == '0':
                matricula_numero[0] = str(random.choice(range(1, 8)))
            matricula_gerada = ''.join(matricula_numero)
        
        matriculas_geradas.add(matricula_gerada)
        dicionario_funcionario['matricula'].append(int(matricula_gerada))
        dicionario_veiculo['matricula'].append(int(matricula_gerada))

    def gerar_nome():
        nome_completo = fake.name()
        dicionario_funcionario['nome_funcionario'].append(nome_completo)
        dicionario_veiculo['nome_funcionario'].append(nome_completo)

    def gerar_cargo_e_nivel_hierarquico():
        cargos = ["Aderecista I", "Aderecista II", "Aderecista III", "Advogado I", "Advogado II", "Advogado III", "Ase I", "Ase II", "Ase III", "Ajustador", "Almoxarife I", "Almoxarife II", "Almoxarife III", "Analista Finaneiro JR", "Analista Finaneiro PL", "Analista Financeiro SR", "Analista Administrativo I", "Analista Administrativo II", "Analista Administrativo III", "Analista de Banco de dados I", "Analista de Banco de dados II", "Analista de Banco de dados III", "Aprendiz - Auxiliar Admnistrativo", "Apresentador Artistico", "Apresentador Especial I", "Apresentador Especial II", "Apresentador Especial III", "Apresentador I", "Apresentador II", "Apresentador III", "Arquiteto", "Assesor", "Assistente Administrativo Financeiro", "Assistente Administrativo Juridico", "Assistente Executivo", "Executivo I", "Executivo II", "Executivo III", "Carpinteiro", "Cenografo", "Ch Producao", "Ch Rede", "Ch Redacao", "Ch Reportagem", "Coordenador", "Coordenador Empresarial", "Coordenador Financeiro", "Coordenador Fiscal", "Coordenador Figurino", "Coordenador Contratos", "Coordenador Defesa", "Cientista de Dados I", "Cientista de Dados II", "Cientista de Dados III", "Designer Ux", "Designer I", "Designer II", "Designer III", "Desenvolvedor I", "Desenvolvedor II", "Desenvolvedor III", "Dir Imagens I", "Dir Imagens II", "Dir Imagens III", "Dir Seguranca", "Dir Financeiro", "Dir Tecnologia", "Dir Programa", "Dir Compliance", "Dir Plataforma", "Dir Comunicacao", "Dir Telefonia", "Dir Pesquisa", "Dir Planejamento", "Dir Genero", "Dir Geral", "Editor I", "Editor II", "Editor III", "Editor Chefe", "Editor Imagem I", "Editor Imagem II", "Editor Imagem III", "Eletricista", "Encarregado"]
        nivel_hierarquico = ["Diretor", "Equipe", "Equipe Técnico Operacional", "Gerente", "Gerente Sr", "Supervisor", "Especialista"]
        cargo_escolhido = random.choice(cargos)
        dicionario_funcionario['cargo'].append(cargo_escolhido)
        if "Dir" in cargo_escolhido[0:3]:
            dicionario_funcionario['nivel_hierarquico'].append("Diretor")
        elif "Ch" in cargo_escolhido[0:2]:
            dicionario_funcionario['nivel_hierarquico'].append("Supervisor")
        elif "Executivo" in cargo_escolhido or "Advogado" in cargo_escolhido:
            dicionario_funcionario['nivel_hierarquico'].append("Gerente Sr")
        elif "Coordenador" in cargo_escolhido or "Analista" in cargo_escolhido:
            dicionario_funcionario['nivel_hierarquico'].append("Gerente")
        elif "Apresentador" in cargo_escolhido:
            dicionario_funcionario['nivel_hierarquico'].append("Equipe")
        else:
            dicionario_funcionario['nivel_hierarquico'].append("Equipe Técnico Operacional")

    def gerar_regiao():
        ufs_brasil = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        dicionario_funcionario['regiao'].append(random.choice(ufs_brasil))

    def gerar_email():
        email = fake.email()
        dicionario_funcionario['email'].append(email)

    def gerar_telefone():
        numero_telefone = fake.phone_number()
        dicionario_funcionario['telefone'].append(numero_telefone)

    placa_geradas = set()  # Inicializando a variável placa_geradas como um conjunto vazio
    def gerar_modelo():
        modelo = []
        chevrolet = ['Chevrolet Onix', 'Chevrolet Tracker', 'Chevrolet S10', 'Chevrolet Cruze', 'Chevrolet Prisma', 'Chevrolet Onix Plus', 'Chevrolet Spin', 'Chevrolet Classic']
        fiat = ['Fiat Strada', 'Fiat Mobi', 'Fiat Toro', 'Fiat Argo', 'Fiat Cronos', 'Fiat Pulse', 'Fiat Palio']
        honda = ['Honda Accord', 'Honda City', 'Honda Civic', 'Honda CR-V', 'Honda Fit', 'Honda HR-V']
        nissan = ['Nissan Frontier', 'Nissan GT-R', 'Nissan Kicks', 'Nissan March','Nissan Sentra', 'Nissan Versa']
        hyundai = ['Hyundai Creta', 'Hyundai HB20', 'Hyundai HB20S', 'Hyundai HR']
        volkswagen = ['Volkswagen Amarok', 'Volkswagen Fox', 'Volkswagen Gol', 'Volkswagen Golf', 'Volkswagen Jetta', 'Volkswagen Nivus', 'Volkswagen Polo']
        kia = ['Kia Cerato', 'Kia Soul', 'Kia Sportage', 'Kia Sorento', 'Kia Picanto', 'Kia Optima', 'Kia Rio','Kia Carnival']
        bmw = ['BMW X1', 'BMW X6','BMW X3', 'BMW X4', 'BMW X5', 'BMW X2']
        audi = ['Audi Q3', 'Audi A3', 'Audi A3 Sedan', 'Audi A4', 'Audi A5', 'Audi Q5', 'Audi R8', 'Audi Q7']
        rand_rover = ['Range Rover Sport', 'Range Rover Velar', 'Range Rover Evoque', 'Land Rover Discovery', 'Land Rover DISCOVERY Sport', 'Land Rover Defender']
        carro_modelo = [chevrolet, fiat, honda, nissan, hyundai, volkswagen, kia, bmw, audi, rand_rover]

        categoria = carro_modelo[random.randint(0, len(carro_modelo)-1)]
        escolha = categoria[random.randint(0, len(categoria)-1)]
        modelo.append(escolha)
        modelo_f = modelo[0]
        dicionario_veiculo['modelo_veiculo'].append(modelo_f)

    def gerar_placa():
        placa = [] # lista das letras e numeros gerados pela função random.choice
        letra = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z']
        numero = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        letra_numero = []

        for i in letra:
            letra_numero.append(i)
        for i in numero:
            letra_numero.append(i)

        while True:
            placa.clear() # Limpa a lista da placa para gerar uma nova
            for i in range(3):
                choose = random.choice(letra)
                placa.append(choose)
            for i in range(5):
                choose1 = random.choice(numero)
                placa.append(choose1)
            placa[5] = random.choice(letra_numero)
            placa[3] = '-'
            placa_final = ''.join(placa)
            if placa_final not in placa_geradas:
                placa_geradas.add(placa_final)
                dicionario_veiculo['placa_veiculo'].append(placa_final)
                break

    def gerar_cor():
        coress = ['Preto', 'Marrom', 'Vermelho', 'Laranja', 'Amarelo', 'Verde', 'Azul Claro', 'Azu  l Escuro', 'Branco', 'Rosa', 'Roxo', 'Cinza', 'Bege', 'Dourado', 'Prateado', 'Turquesa']
        escolha_cor = random.choice(coress)
        dicionario_veiculo['cor'].append(escolha_cor)

    for quantidade in range(1, qtd + 1):
        gerar_matricula()
        gerar_nome()
        gerar_cargo_e_nivel_hierarquico()
        gerar_regiao()
        gerar_email()
        gerar_telefone()
        gerar_placa()
        gerar_modelo()
        gerar_cor()

    dic = {"tabela_funcionario": dicionario_funcionario, "tabela_veiculo": dicionario_veiculo}
    return dic


server = Flask(__name__)


"""
Este aplicativo Flask gera informações aleatórias sobre funcionários e veículos brasileiros
usando a biblioteca Faker. Ele disponibiliza três endpoints via API REST para acessar essas informações:

1. /funcionarios/<int:qtd>:
   Endpoint que retorna um JSON com dados fictícios de funcionários brasileiros.
   Parâmetro 'qtd' especifica a quantidade de registros de funcionários a serem gerados.

2. /veiculos/<int:qtd>:
   Endpoint que retorna um JSON com dados fictícios de veículos brasileiros.
   Parâmetro 'qtd' especifica a quantidade de registros de veículos a serem gerados.

3. /dados-funcionarios_veiculo/<int:qtd>:
   Endpoint que retorna um JSON com dados fictícios de funcionários e seus respectivos veículos.
   Parâmetro 'qtd' especifica a quantidade de registros de funcionários e veículos a serem gerados.

As informações geradas incluem matrícula, nome do funcionário, cargo, nível hierárquico,
região (UF), e-mail, telefone para funcionários, além de placa do veículo, modelo e cor para veículos.

Os dados são gerados aleatoriamente a cada requisição, garantindo matrículas e placas únicas
e associando corretamente os veículos aos funcionários. O aplicativo é iniciado no host '0.0.0.0'
e na porta 5000 quando executado diretamente.

Exemplo de uso:
- Para obter 5 registros de funcionários: GET /funcionarios/5
- Para obter 3 registros de veículos: GET /veiculos/3
- Para obter 2 registros de funcionários com seus veículos correspondentes: GET /dados-funcionarios_veiculo/2
"""


@server.get('/funcionarios/<int:qtd>')
def obter_funcionarios(qtd):
    tabela_completa = tabela(qtd)
    return jsonify(tabela_completa['tabela_funcionario'])

# Endpoint para obter dados dos veículos
@server.get('/veiculos/<int:qtd>')
def obter_veiculos(qtd):
    tabela_completa = tabela(qtd)
    return jsonify(tabela_completa['tabela_veiculo'])

@server.get('/dados-funcionarios_veiculo/<int:qtd>')
def obter_info(qtd):
    tabela_completa = tabela(qtd)
    return jsonify(tabela_completa)

if __name__ == '__main__':
   server.run(host='0.0.0.0', port=5000)
