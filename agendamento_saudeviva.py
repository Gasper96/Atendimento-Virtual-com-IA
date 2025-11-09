import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

# Carregar chave de API da variável de ambiente
client = OpenAI(api_key=os.getenv("chave_openai"))

# Caminho do arquivo de dados
ARQUIVO_DADOS = "consultas.json"

#data atual
hoje = datetime.now().strftime("%Y-%m-%d")

# Funções auxiliares
def carregar_consultas():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_consultas(consultas):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(consultas, f, indent=4, ensure_ascii=False)

def horario_disponivel(data, hora, consultas):
    """Verifica se há conflito de horário"""
    nova_data = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
    fim_nova = nova_data + timedelta(minutes=30)
    for c in consultas:
        c_data = datetime.strptime(f"{c['data']} {c['hora']}", "%Y-%m-%d %H:%M")
        fim_c = c_data + timedelta(minutes=30)
        if (c_data <= nova_data < fim_c) or (nova_data <= c_data < fim_nova):
            return False
    return True

def dentro_do_horario_funcionamento(hora):
    h = datetime.strptime(hora, "%H:%M").time()
    inicio = datetime.strptime("08:00", "%H:%M").time()
    fim = datetime.strptime("18:00", "%H:%M").time()
    return inicio <= h < fim

def gerar_id(consultas):
    return len(consultas) + 1

# Função principal que interage com o ChatGPT
def interpretar_comando_linguagem_natural(texto):
    prompt = f"""
    Você é um assistente que interpreta pedidos de agendamento médico.
    a data de hoje é {hoje}. Use ESSA data como referência absoluta para calcular expressões como "amanhã", "depois de amanhã" etc.
    Não invente o ano. Use exatamente o ano indicado em {hoje}.
    Extraia as seguintes informações do texto abaixo e retorne somente o JSON puro no formato abaixo sem explicações extras:
    {{
        "nome": "Nome do paciente", 
        "data": "AAAA-MM-DD",
        "hora": "HH:MM"
    }}
    Texto: "{texto}"
    """
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"a data de hoje é {hoje} e Você é um assistente de agendamento médico, restrinja o assunto para apenas realizar o agendamento de exames."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )
    conteudo = resposta.choices[0].message.content
    try:
        dados = json.loads(conteudo)
        return dados
    except:
        print("❌ Erro ao interpretar a resposta do modelo:")
        print(conteudo)
        return None

# Função para agendar uma consulta
def agendar_consulta(texto):
    consultas = carregar_consultas()
    dados = interpretar_comando_linguagem_natural(texto)
    
    if not dados:
        return "Não consegui entender o pedido. Tente reformular."

    nome = dados["nome"]
    data = dados["data"]
    hora = dados["hora"]

    # Validações
    dia_semana = datetime.strptime(data, "%Y-%m-%d").weekday()
    if dia_semana > 4:
        return "A clínica só funciona de segunda a sexta-feira."

    if not dentro_do_horario_funcionamento(hora):
        return "O horário deve estar entre 08:00 e 18:00."

    if not horario_disponivel(data, hora, consultas):
        return f"Já existe uma consulta marcada para {hora} neste dia."

    # Registrar consulta
    nova_consulta = {
        "id": gerar_id(consultas),
        "nome": nome,
        "data": data,
        "hora": hora,
        "duracao_min": 30,
        "status": "marcada",
        "medico": "Dr. Carlos — Clínico Geral"
    }

    consultas.append(nova_consulta)
    salvar_consultas(consultas)

    mensagem_confirmacao = (
        f"✅ Consulta marcada com sucesso!\n"
        f"Paciente: {nome}\n"
        f"Data: {data}\n"
        f"Hora: {hora}\n"
        f"Médico: Dr. Carlos — Clínico Geral"
    )
    return mensagem_confirmacao

# Função para listar consultas
def listar_consultas():
    consultas = carregar_consultas()
    if not consultas:
        return "Nenhuma consulta registrada."
    resultado = "📅 Consultas agendadas:\n"
    for c in consultas:
        resultado += (f"ID: {c['id']} | {c['nome']} | {c['data']} {c['hora']} | "
                      f"Status: {c['status']}\n")
    return resultado

# Função para cancelar consulta
def cancelar_consulta(id_consulta):
    consultas = carregar_consultas()
    for c in consultas:
        if c["id"] == id_consulta:

            
            c["status"] = "cancelada"
            salvar_consultas(consultas)
            return f"Consulta ID {id_consulta} foi cancelada com sucesso."
    return "Consulta não encontrada."

# Interface simples via terminal
def menu():
    while True:
        print("\n=== Sistema de Agendamento SaúdeViva ===")
        print("1. Agendar consulta (linguagem natural)")
        print("2. Listar consultas")
        print("3. Cancelar consulta")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            texto = input("Descreva o pedido (ex: Quero marcar consulta para João amanhã às 10h): ")
            resposta = agendar_consulta(texto)
            print(resposta)
        elif opcao == "2":
            print(listar_consultas())
        elif opcao == "3":
            id_consulta = int(input("Digite o ID da consulta: "))
            print(cancelar_consulta(id_consulta))
        elif opcao == "4":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
