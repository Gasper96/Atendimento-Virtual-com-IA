# Sistema de Agendamento Médico com integração de IA

Um assistente inteligente de agendamentos médicos que entende **linguagem natural** e agenda consultas automaticamente!  
O projeto utiliza a **API da OpenAI** para interpretar comandos do usuário, como por exemplo:

> "Gostaria de marcar uma consulta para João amanhã às 10h."

Ele identifica **nome, data e horário**, verifica **disponibilidade**, e registra o agendamento em um arquivo JSON.

## Descrição do Projeto
O sistema é uma aplicação em Python para gerenciamento de consultas médicas.  
Seu diferencial é a **interpretação automática** de pedidos em linguagem natural, utilizando o modelo **GPT-4o-mini** da OpenAI.  

Principais recursos:
- Interpretação de linguagem natural para marcar consultas.
-  Armazenamento automático das consultas em `consultas.json`.
-  Verificação de conflitos de horário e horário de funcionamento (08h–18h).
-  Cancelamento e listagem de consultas existentes.
-  Persistência de dados local via JSON.

## Como Executar Localmente
- Instale as dependências:
    Dependências Necessárias:
      Python 3.8+
      Bibliotecas:
                json (nativo do Python)
                datetime (nativo do Python)
                os (nativo do Python)
                openai: bash{
                              pip install openai }

- Configure a variável de ambiente com sua chave da OpenAI No Windows (cmd/prompt):
    bash{
          setx chave_openai "sua_chave_aqui" }

- Passo a Passo para Testes:
  I) Execute o script com python agendamento_saudeviva.py.
  II) Escolha a opção 1 para agendar uma consulta.
  III) Digite algo como:
                      Quero agendar uma consulta para Maria segunda-feira às 09:30.
  IV) Verifique se o sistema:
                      Cria ou atualiza o arquivo consultas.json.
                      Retorna a mensagem de confirmação com nome, data e hora.
  V) Use a opção 2 para listar consultas.
  VI) Use a opção 3 e insira o ID para cancelar uma consulta.
  VII) Repita o teste variando frases, horários e nomes.
