# The Chamber - Plataforma para Experimento de Julgamento Moral

`The Chamber` é uma plataforma de coleta de dados desenvolvida em **Pygame**, projetada para servir como ferramenta em experimentos de psicologia e ciências comportamentais. O foco do projeto é investigar como o julgamento moral e a tomada de decisão são influenciados pela divulgação gradual de informações.

## O Experimento

### Hipótese / Questão Central
O objetivo do estudo é analisar como os indivíduos formam e potencialmente alteram seus julgamentos sobre uma situação eticamente complexa à medida que novos fragmentos de evidência são apresentados. A pesquisa busca responder a perguntas como:

* Com que rapidez as pessoas formam um julgamento inicial?
* Quão suscetíveis são esses julgamentos a mudanças quando confrontados com novas informações que podem contradizer ou contextualizar as anteriores?
* Existem variáveis demográficas (idade, gênero) ou de experiência que se correlacionam com a flexibilidade ou rigidez do julgamento?

### Metodologia e Coleta de Dados
O fluxo do jogo foi desenhado para isolar e registrar as variáveis de interesse de forma sistemática.

1.  **Dados Demográficos:** Ao iniciar, a plataforma coleta dados básicos do participante: idade, gênero e nível de familiaridade auto-declarado com jogos de dilema moral. Cada sessão de jogo recebe um ID único (`ID_Sessao`).

2.  **Apresentação do Caso:** Um caso (história com um suspeito) é selecionado aleatoriamente do banco de casos (`CASE_POOL`), garantindo que os participantes enfrentem cenários diferentes.

3.  **Julgamento Incremental (6 Rodadas):** A história não é revelada de uma só vez. Ela é dividida em **seis fragmentos**. O experimento ocorre em seis rodadas:
    * **Rodada 1:** O primeiro fragmento é apresentado. O participante vota em **"Culpado"** ou **"Inocente"**.
    * **Rodada 2:** O segundo fragmento é adicionado ao primeiro. O participante vota novamente, agora com mais contexto.
    * **... e assim por diante, até a Rodada 6**, onde todos os seis fragmentos estão visíveis.

4.  **Variáveis Coletadas por Rodada:** Para cada um dos seis votos, o sistema registra:
    * `Decisao_Final`: O voto do participante (0 para Inocente, 1 para Culpado).
    * `Tempo_de_Decisao_s`: O tempo em segundos que o participante levou para decidir.
    * `Mudanca_de_Voto`: Um indicador (1 para sim, 0 para não) se o voto da rodada atual é diferente do voto da rodada anterior.

5.  **Revelação Final:** Após a sexta e última votação, a plataforma revela a história completa e o desfecho real do caso, mostrando se o suspeito era, de fato, culpado ou inocente.

### Estrutura do Arquivo de Saída
Ao final de cada sessão completa (as 6 rodadas), os dados coletados são automaticamente salvos em um arquivo chamado `resultados_experimento.csv`. Se o arquivo não existir, ele será criado com um cabeçalho. Os dados de novas sessões são adicionados ao final do arquivo, permitindo a coleta contínua.

As colunas salvas no arquivo CSV são:

| Cabeçalho               | Descrição                                                          |
| :---------------------- | :----------------------------------------------------------------- |
| `ID_Sessao`             | Identificador único para a sessão de jogo.                         |
| `ID_Participante`       | Identificador do participante (fixado como P1 no código atual).    |
| `Num_Rodada`            | O número da rodada de votação (de 1 a 6).                          |
| `Idade`                 | Idade do participante.                                             |
| `Genero_Participante`   | Gênero declarado pelo participante.                                |
| `Experiencia_com_Jogos` | Nível de familiaridade com jogos morais (1-5).                     |
| `ID_Caso`               | Identificador do caso que foi jogado.                              |
| `Tipo_de_Historia`      | Se o caso é baseado em fatos reais ou fictício.                    |
| `Genero_Suspeito`       | Gênero do suspeito no caso.                                        |
| `Tempo_de_Decisao_s`    | Tempo de decisão do participante em segundos.                      |
| `Decisao_Final`         | Voto do participante (0 = Inocente, 1 = Culpado).                  |
| `Mudanca_de_Voto`       | Se o voto mudou em relação à rodada anterior (0 = Não, 1 = Sim).   |
| `Resultado_Real_Caso`   | O desfecho verdadeiro do caso (0 = Inocente, 1 = Culpado).         |
| `Num_Jogadores_Sessao`  | Número de jogadores (fixado em 1 no código atual).                 |

## Como Executar a Plataforma

Siga os passos abaixo para executar o experimento em sua máquina.

#### Pré-requisitos
* Python 3.x instalado.

### Instalação

1.  Clone este repositório para a sua máquina local:
    ```bash
    git clone [https://github.com/laysearaujo/the_chamber.git](https://github.com/laysearaujo/the_chamber.git)
    cd the_chamber
    ```

2.  (Recomendado) Crie e ative um ambiente virtual para isolar as dependências do projeto:
    * No macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * No Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  Instale a biblioteca Pygame. Crie um arquivo chamado `requirements.txt` na pasta do projeto, adicione o conteúdo abaixo a ele, e depois execute o comando de instalação.

    Conteúdo para `requirements.txt`:
    ```
    pygame
    ```

    Comando para instalar:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Com o ambiente virtual ativado e as dependências instaladas, execute o arquivo principal:

```bash
python the_chamber.py