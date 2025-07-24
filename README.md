# The Chamber - Protótipo Experimental
Este repositório contém o código-fonte do "The Chamber", um jogo desenvolvido em Pygame que funciona como um protótipo para um experimento social sobre julgamento moral com informações parciais.

## O Experimento
O objetivo central do experimento é analisar como as pessoas julgam situações eticamente complexas e como suas percepções podem mudar conforme mais contexto é fornecido. O jogo foi projetado para coletar dados sobre as decisões dos jogadores, permitindo uma análise posterior sobre os fatores que influenciam o julgamento humano.

**Fluxo do Jogo e Coleta de Dados**
1. Coleta de Dados Demográficos: No início, cada jogador preenche um formulário com sua idade, gênero e nível de familiaridade com jogos de dilema moral.

2. Apresentação do Caso: Um caso (história) é sorteado aleatoriamente.

3. Julgamento em 3 Etapas: A história é revelada em três fragmentos. Após cada fragmento, cada jogador vota secretamente em "Culpado" (1) or "Inocente" (0).

4. Coleta de Dados: O jogo registra para cada voto:

* A decisão do jogador.

* O tempo levado para decidir.

* Se o jogador mudou de voto em relação à rodada anterior.

5. Revelação Final: Após a terceira votação, a história completa e o resultado real (se o suspeito era de fato culpado ou inocente) são revelados.

6. Exportação: Ao final do caso, todos os dados coletados na sessão são impressos no console (terminal) em um formato de tabela, pronto para ser copiado para uma planilha.

## Como Rodar o Jogo
Para executar o protótipo em sua máquina, siga os passos abaixo.

Pré-requisitos
* Python 3.x instalado em seu sistema.

### Instalação
1. Clone o repositório:

    ``` batch
    git clone https://github.com/laysearaujo/the_chamber.git
    cd the_chamber
    ```

2. Crie um ambiente virtual (Recomendado):

    ```batch
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ````

3. Instale as dependências:

    O único requisito para este jogo é a biblioteca Pygame. Instale-a usando o arquivo `requirements.txt` fornecido.

    ```batch
    pip install -r requirements.txt
    ```

### Execução
Após instalar as dependências, execute o arquivo principal do jogo:

```batch
python the_chamber.py
```

O jogo será iniciado em uma nova janela. Siga as instruções na tela para definir o número de jogadores, preencher os dados e jogar. Ao final da partida, verifique o console onde você executou o comando para ver a tabela de dados coletados.
