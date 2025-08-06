import pygame
import sys
import random
import textwrap
import time
import csv
import os

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("The Chamber - Experimento Individual")
font_large = pygame.font.SysFont("courier", 50)
font = pygame.font.SysFont("courier", 22)
small_font = pygame.font.SysFont("courier", 16)
clock = pygame.time.Clock()

# --- Configurações do Experimento ---
MAX_ROUNDS = 6 # Conforme o GDD
COLOR_PRIMARY = (0, 200, 255)
COLOR_SECONDARY = (200, 255, 255)
COLOR_BG = (5, 5, 15)
COLOR_DANGER = (255, 50, 50)
COLOR_SUCCESS = (50, 255, 150)
COLOR_SCROLLBAR = (0, 150, 200)


# --- Banco de Casos com Múltiplos Fragmentos ---
CASE_POOL = [
    {
        "id": 1, "type": "Real", "suspect_gender": "Feminino",
        "fragments": [
            "Uma médica é vista saindo apressada de uma sala de cirurgia.",
            "Minutos depois, um alarme soa. Um paciente na mesma sala teve uma parada cardíaca e faleceu.",
            "Uma enfermeira alega ter ouvido a médica discutir com o paciente momentos antes do alarme.",
            "A investigação revela que a médica estava em um plantão de 36 horas.",
            "É descoberto que a médica havia solicitado equipamento de emergência que não foi fornecido pelo hospital.",
            "A autópsia confirma que a condição do paciente era pré-existente e gravíssima, tornando a sobrevivência improvável."
        ],
        "full_story": "A médica, exausta e trabalhando com recursos inadequados, teve uma discussão com o paciente tentando convencê-lo da necessidade de um procedimento arriscado. Ela saiu para buscar equipamento em outra sala, mas o paciente faleceu antes de sua volta. Foi absolvida por não haver negligência.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 2, "type": "Fictícia", "suspect_gender": "Masculino",
        "fragments": [
            "Um programador é demitido de uma startup de tecnologia.",
            "Na mesma noite, o servidor principal da empresa contendo todo o código-fonte é completamente apagado.",
            "Registros de acesso mostram que o login do programador demitido foi usado para apagar os arquivos.",
            "O programador tem um álibi: estava em um bar com amigos, longe do escritório.",
            "Ele alega que sua senha era fraca e conhecida por vários colegas.",
            "Um colega de equipe, que estava no escritório naquela noite, recentemente teve uma grande discussão com a diretoria por não receber crédito pelo projeto."
        ],
        "full_story": "O colega de equipe, sentindo-se injustiçado e sabendo a senha do programador demitido, usou o acesso dele para apagar o servidor, como vingança contra a empresa e para incriminar o ex-colega. O programador era inocente.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 3, "type": "Fictícia", "suspect_gender": "Masculino",
        "fragments": [
            "Um restaurador de arte é contratado para limpar uma pintura famosa em um museu.",
            "Após a devolução, um especialista alega que a pintura é uma falsificação quase perfeita.",
            "O restaurador foi o último a ter acesso exclusivo à obra de arte.",
            "Uma investigação financeira revela que o restaurador possui grandes dívidas de jogo não declaradas.",
            "Partículas de um pigmento moderno, inexistente na época do pintor original, são encontradas no ateliê do restaurador.",
            "Registros bancários mostram um grande depósito anônimo na conta do restaurador uma semana após a devolução da pintura."
        ],
        "full_story": "O restaurador, pressionado por dívidas, criou uma cópia meticulosa da obra. Durante o processo de 'restauração', ele trocou a original pela falsa e vendeu a pintura verdadeira no mercado negro para pagar suas dívidas. Ele foi considerado culpado.",
        "real_outcome": 1 # Culpado
    },
    {
        "id": 4, "type": "Real", "suspect_gender": "Feminino",
        "fragments": [
            "A fórmula secreta de um novo produto farmacêutico é vazada para uma empresa concorrente.",
            "Uma cientista sênior do projeto tinha acesso irrestrito à fórmula.",
            "Registros mostram que a cientista transferiu o arquivo da fórmula para um pen drive pessoal dias antes do vazamento.",
            "A cientista alega que fez o backup para trabalhar em uma apresentação em casa e perdeu o pen drive.",
            "Um assistente de laboratório júnior foi visto usando o computador da cientista fora do horário de expediente.",
            "O histórico de e-mails do assistente revela contato com um executivo da empresa concorrente."
        ],
        "full_story": "O assistente de laboratório, ambicioso e mal-intencionado, roubou o pen drive da cientista e vazou a fórmula para a concorrência em troca de uma oferta de emprego. A cientista foi usada como bode expiatório, mas acabou sendo inocentada.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 5, "type": "Fictícia", "suspect_gender": "Masculino",
        "fragments": [
            "Um pedestre é morto em um atropelamento e fuga durante a noite.",
            "Uma testemunha ocular descreve um carro sedan escuro, modelo que corresponde ao do suspeito.",
            "O carro do suspeito é encontrado em sua garagem com danos na parte dianteira, coberto por uma lona.",
            "O suspeito afirma que seu carro foi roubado na noite do acidente e que ele só percebeu na manhã seguinte.",
            "A perícia encontra apenas as impressões digitais do suspeito no volante e no interior do carro.",
            "Os dados de localização do celular do suspeito o colocam na rua exata do acidente no momento em que ocorreu."
        ],
        "full_story": "O suspeito estava dirigindo, distraiu-se e atingiu o pedestre. Em pânico, ele fugiu do local e inventou a história do roubo para tentar escapar da responsabilidade. As provas digitais e forenses provaram sua culpa.",
        "real_outcome": 1 # Culpado
    },
    {
        "id": 6, "type": "Fictícia", "suspect_gender": "Feminino",
        "fragments": [
            "Uma professora é acusada de vazar as respostas de uma prova nacional.",
            "Um aluno foi pego com uma cópia idêntica à prova oficial antes do exame.",
            "O arquivo da prova foi acessado no computador da professora na véspera.",
            "A professora nega envolvimento e afirma que deixou o computador desbloqueado na sala dos professores.",
            "Câmeras mostram outro docente mexendo no computador enquanto ela estava fora.",
            "Esse docente confessa ter copiado o arquivo e vendido as respostas a vários alunos."
        ],
        "full_story": "A professora foi vítima de negligência ao deixar o computador desbloqueado, mas não participou do vazamento. O verdadeiro culpado era outro professor, que confessou o crime.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 7, "type": "Fictícia", "suspect_gender": "Feminino",
        "fragments": [
            "Uma influenciadora digital é acusada de fraude em uma campanha de arrecadação para vítimas de enchente.",
            "Mais de R$ 500 mil foram arrecadados através das redes sociais dela.",
            "As vítimas afirmam não ter recebido qualquer ajuda proveniente da campanha.",
            "Extratos mostram transferências da conta da campanha para a conta pessoal da influenciadora.",
            "Ela alega que fez os saques para agilizar as compras de doações.",
            "Perícia comprova que parte significativa do dinheiro foi gasta em itens de luxo."
        ],
        "full_story": "A influenciadora usou a tragédia para enriquecer, desviando a maior parte dos recursos para gastos pessoais. Foi condenada por estelionato e apropriação indébita.",
        "real_outcome": 1
    },
    {
        "id": 8, "type": "Real", "suspect_gender": "Masculino",
        "fragments": [
            "Um motorista de ônibus é acusado de provocar um acidente fatal.",
            "Testemunhas dizem que ele dirigia acima da velocidade permitida.",
            "O tacógrafo indica velocidade 20% superior ao limite no momento do impacto.",
            "O motorista afirma que o sistema de freios apresentou falha repentina.",
            "A perícia confirma desgaste excessivo nos freios, incompatível com manutenção recente.",
            "A empresa responsável admite que ignorou pedidos de revisão feitos pelo motorista."
        ],
        "full_story": "O motorista não teve culpa direta; o acidente foi resultado de negligência da empresa que não realizou a manutenção. Ele foi inocentado.",
        "real_outcome": 0
    },
    {
        "id": 9, "type": "Fictícia", "suspect_gender": "Masculino",
        "fragments": [
            "Um cientista é acusado de manipular dados em uma pesquisa sobre vacinas.",
            "O artigo publicado apresenta resultados surpreendentes e altamente positivos.",
            "Colegas notam inconsistências nas planilhas originais e denunciam à instituição.",
            "O cientista argumenta que as discrepâncias ocorreram por erro de digitação.",
            "Um backup dos arquivos originais revela dados muito diferentes dos publicados.",
            "Descobre-se que ele alterou os resultados para garantir financiamento milionário."
        ],
        "full_story": "O cientista cometeu fraude deliberada para manter investimentos no projeto. Foi descredenciado e processado por má conduta científica.",
        "real_outcome": 1
    },
    {
        "id": 10, "type": "Real", "suspect_gender": "Feminino",
        "fragments": [
            "Uma prefeita é acusada de desviar verbas para festas da cidade.",
            "Populares afirmam que ela gastava mais com eventos do que com saúde.",
            "Investigações apontam contratos superfaturados em eventos culturais.",
            "Ela alega que os contratos foram assinados por um secretário, sem seu conhecimento.",
            "Testemunhas dizem que ela insistia em festas luxuosas para 'manter popularidade'.",
            "Perícia contábil prova que as assinaturas nos contratos foram dela."
        ],
        "full_story": "A prefeita usou recursos públicos para autopromoção por meio de festas grandiosas. Foi condenada por improbidade administrativa.",
        "real_outcome": 1
    }
]


# --- Classes Auxiliares ---
class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.age = ""
        self.gender = ""
        self.experience = 0

class Button:
    def __init__(self, rect, text, text_color=COLOR_PRIMARY, border_color=COLOR_PRIMARY, hover_color=COLOR_SECONDARY):
        self.rect, self.text, self.text_color = pygame.Rect(rect), text, text_color
        self.border_color, self.hover_color, self.is_hovered = border_color, hover_color, False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.border_color
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=5)
        label = font.render(self.text, True, color)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def check_hover(self, pos): self.is_hovered = self.rect.collidepoint(pos)
    def is_clicked(self, pos): return self.rect.collidepoint(pos)

# --- Telas do Jogo ---
def draw_background():
    screen.fill(COLOR_BG)
    for x in range(0, 1000, 20): pygame.draw.line(screen, (15, 25, 40), (x, 0), (x, 700), 1)
    for y in range(0, 700, 20): pygame.draw.line(screen, (15, 25, 40), (0, y), (1000, y), 1)

def wrap_text_pixel(text, font, max_pixel_width):
    words, lines, current_line = text.split(' '), [], ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_pixel_width: current_line = test_line
        else: lines.append(current_line); current_line = word + " "
    lines.append(current_line)
    return lines

def intro_screen():
    running = True
    title = font_large.render("THE CHAMBER", True, COLOR_PRIMARY)
    start_button = Button((350, 600, 300, 50), "INICIAR EXPERIMENTO")

    intro_text = (
        "Bem-vindo. Você está prestes a participar de um experimento social sobre "
        "tomada de decisão e julgamento sob incerteza.\n\n"
        "A cada rodada, um novo fragmento de informação sobre um caso será revelado. "
        "Seu papel é julgar o suspeito com base nas evidências apresentadas.\n\n"
        "Suas decisões são anônimas e essenciais para a pesquisa. Obrigado por participar."
    )

    all_wrapped_lines = []
    for paragraph in intro_text.split('\n'):
        wrapped_lines = wrap_text_pixel(paragraph, font, 750)
        all_wrapped_lines.extend(wrapped_lines)

    while running:
        draw_background()
        mouse_pos = pygame.mouse.get_pos()
        start_button.check_hover(mouse_pos)

        screen.blit(title, title.get_rect(centerx=500, y=100))

        y_offset = 250
        for line in all_wrapped_lines:
            line_surface = font.render(line, True, COLOR_SECONDARY)
            screen.blit(line_surface, line_surface.get_rect(centerx=500, y=y_offset))
            y_offset += 30

        start_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos):
                    running = False

        pygame.display.flip()
        clock.tick(30)

def demographics_screen(player_id):
    player = Player(player_id)
    active_field = "age"
    age_input_rect = pygame.Rect(350, 180, 300, 50)
    gender_buttons = {
        "Mulher cis": Button((150, 300, 200, 50), "Mulher cis"), "Homem cis": Button((370, 300, 200, 50), "Homem cis"),
        "Não binário": Button((590, 300, 200, 50), "Não binário"), "Mulher trans": Button((150, 360, 200, 50), "Mulher trans"),
        "Homem trans": Button((370, 360, 200, 50), "Homem trans"), "Outro": Button((590, 360, 200, 50), "Outro"),
    }
    exp_buttons = {i: Button((200 + (i-1)*130, 500, 100, 50), str(i)) for i in range(1, 6)}
    confirm_button = Button((400, 610, 200, 50), "CONFIRMAR")

    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        title = font_large.render("DADOS DO PARTICIPANTE", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=50))
        screen.blit(font.render("Qual sua idade?", True, COLOR_SECONDARY), (350, 150))
        pygame.draw.rect(screen, COLOR_PRIMARY if active_field == "age" else COLOR_SECONDARY, age_input_rect, 2)
        screen.blit(font.render(player.age, True, COLOR_SECONDARY), (age_input_rect.x + 10, age_input_rect.y + 10))
        screen.blit(font.render("Você é:", True, COLOR_SECONDARY), (150, 270))
        for gender, btn in gender_buttons.items():
            if player.gender == gender: btn.border_color, btn.text_color = COLOR_SUCCESS, COLOR_SUCCESS
            else: btn.border_color, btn.text_color = COLOR_PRIMARY, COLOR_PRIMARY
            btn.check_hover(mouse_pos); btn.draw(screen)
        screen.blit(font.render("Qual seu nível de familiaridade com jogos morais? (1-5)", True, COLOR_SECONDARY), (200, 470))
        for exp, btn in exp_buttons.items():
            if player.experience == exp: btn.border_color, btn.text_color = COLOR_SUCCESS, COLOR_SUCCESS
            else: btn.border_color, btn.text_color = COLOR_PRIMARY, COLOR_PRIMARY
            btn.check_hover(mouse_pos); btn.draw(screen)
        if player.age and player.gender and player.experience:
            confirm_button.check_hover(mouse_pos); confirm_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if age_input_rect.collidepoint(mouse_pos): active_field = "age"
                else: active_field = ""
                for gender, btn in gender_buttons.items():
                    if btn.is_clicked(mouse_pos): player.gender = gender
                for exp, btn in exp_buttons.items():
                    if btn.is_clicked(mouse_pos): player.experience = exp
                if confirm_button.is_clicked(mouse_pos) and player.age and player.gender and player.experience:
                    return player
            if event.type == pygame.KEYDOWN and active_field == "age":
                if event.key == pygame.K_BACKSPACE: player.age = player.age[:-1]
                elif event.unicode.isdigit(): player.age += event.unicode
        pygame.display.flip(); clock.tick(30)

def voting_screen(player, case, round_num):
    culpado_button = Button((225, 600, 250, 80), "CULPADO (1)", text_color=COLOR_DANGER, border_color=COLOR_DANGER)
    inocente_button = Button((525, 600, 250, 80), "INOCENTE (0)", text_color=COLOR_SUCCESS, border_color=COLOR_SUCCESS)
    start_time = time.time()

    scroll_y = 0
    scroll_speed = 30
    padding = 20
    line_spacing = 28
    paragraph_spacing = 10

    fragment_box = pygame.Rect(100, 120, 800, 450)

    all_text_lines = []
    for i in range(round_num):
        fragment_text = f"Info {i+1}: {case['fragments'][i]}"
        wrapped_lines = wrap_text_pixel(fragment_text, font, fragment_box.width - (padding * 2))
        all_text_lines.extend(wrapped_lines)
        if i < round_num - 1:
            all_text_lines.append("")

    total_text_height = (len(all_text_lines) - (round_num -1)) * line_spacing + (round_num -1) * (line_spacing + paragraph_spacing)

    while True:
        draw_background()
        mouse_pos = pygame.mouse.get_pos()
        culpado_button.check_hover(mouse_pos)
        inocente_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                decision_time = round(time.time() - start_time, 2)
                if culpado_button.is_clicked(mouse_pos): return 1, decision_time
                if inocente_button.is_clicked(mouse_pos): return 0, decision_time

            if event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * scroll_speed
                max_scroll = max(0, total_text_height - fragment_box.height + (padding * 2))
                scroll_y = max(0, min(scroll_y, max_scroll))

        title = font.render(f"RODADA {round_num} DE {MAX_ROUNDS}", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=30))

        case_info = f"Caso #{case['id']} | Gênero do Suspeito: {case['suspect_gender']} | Tipo: {case['type']}"
        case_info_surf = small_font.render(case_info, True, COLOR_SECONDARY)
        screen.blit(case_info_surf, case_info_surf.get_rect(centerx=500, y=80))

        pygame.draw.rect(screen, COLOR_PRIMARY, fragment_box, 2, border_radius=10)

        screen.set_clip(fragment_box.inflate(-4, -4))

        y_offset = fragment_box.y + padding - scroll_y
        for i in range(round_num):
            fragment_text = f"Info {i+1}: {case['fragments'][i]}"
            for line in wrap_text_pixel(fragment_text, font, fragment_box.width - (padding * 2)):
                line_surf = font.render(line, True, COLOR_SECONDARY)
                screen.blit(line_surf, (fragment_box.x + padding, y_offset))
                y_offset += line_spacing
            y_offset += paragraph_spacing

        screen.set_clip(None)

        content_is_scrollable = total_text_height > fragment_box.height - (padding * 2)
        if content_is_scrollable:
            max_scroll = total_text_height - fragment_box.height + (padding * 2)
            scrollbar_height = max(20, fragment_box.height * (fragment_box.height / total_text_height))
            scrollbar_y_ratio = scroll_y / max_scroll
            scrollbar_y = fragment_box.y + (scrollbar_y_ratio * (fragment_box.height - scrollbar_height))

            scrollbar_rect = pygame.Rect(fragment_box.right - 12, scrollbar_y, 8, scrollbar_height)
            pygame.draw.rect(screen, COLOR_SCROLLBAR, scrollbar_rect, 0, border_radius=4)

        culpado_button.draw(screen)
        inocente_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def final_revelation_screen(case):
    quit_button = Button((400, 630, 200, 50), "FIM DO CASO")
    outcome_text = "CULPADO" if case['real_outcome'] == 1 else "INOCENTE"
    outcome_color = COLOR_DANGER if case['real_outcome'] == 1 else COLOR_SUCCESS

    while True:
        draw_background()
        mouse_pos = pygame.mouse.get_pos()
        quit_button.check_hover(mouse_pos)

        title = font_large.render("REVELAÇÃO FINAL", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=50))

        screen.blit(font.render(f"A verdade sobre o Caso #{case['id']}:", True, COLOR_SECONDARY), (100, 150))
        y_offset = 190
        for line in wrap_text_pixel(case['full_story'], font, 800):
            screen.blit(font.render(line, True, COLOR_SECONDARY), (100, y_offset)); y_offset += 30

        y_offset += 30
        veredict_text = font_large.render(f"O suspeito era: {outcome_text}", True, outcome_color)
        screen.blit(veredict_text, veredict_text.get_rect(centerx=500, y=y_offset))

        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_clicked(mouse_pos): return

        pygame.display.flip()
        clock.tick(30)

def main():
    intro_screen()

    player = demographics_screen(1)

    # Escolhe um caso aleatório do pool expandido
    current_case = random.choice(CASE_POOL)
    collected_data = []
    session_id = f"SESSAO_{int(time.time())}"
    player_votes_history = []

    for round_num in range(1, MAX_ROUNDS + 1):
        decision, decision_time = voting_screen(player, current_case, round_num)

        mudanca_voto = 0
        if round_num > 1 and decision != player_votes_history[-1]:
            mudanca_voto = 1
        player_votes_history.append(decision)

        data_row = {
            "ID_Sessao": session_id, "ID_Participante": f"P{player.id}", "Num_Rodada": round_num,
            "Idade": player.age, "Genero_Participante": player.gender, "Experiencia_com_Jogos": player.experience,
            "ID_Caso": current_case['id'], "Tipo_de_Historia": current_case['type'], "Genero_Suspeito": current_case['suspect_gender'],
            "Tempo_de_Decisao_s": decision_time, "Decisao_Final": decision, "Mudanca_de_Voto": mudanca_voto,
            "Resultado_Real_Caso": current_case['real_outcome'], "Num_Jogadores_Sessao": 1
        }
        collected_data.append(data_row)

    final_revelation_screen(current_case)

    output_filename = "resultados_experimento.csv"
    file_exists = os.path.isfile(output_filename)

    try:
        with open(output_filename, 'a', newline='', encoding='utf-8') as csvfile:
            if collected_data:
                writer = csv.DictWriter(csvfile, fieldnames=collected_data[0].keys())
                # Escreve o cabeçalho apenas se o arquivo for novo ou estiver vazio
                if not file_exists or os.path.getsize(output_filename) == 0:
                    writer.writeheader()
                writer.writerows(collected_data)
            print(f"\n--- DADOS DA SESSÃO SALVOS COM SUCESSO EM '{output_filename}' ---")
    except Exception as e:
        print(f"\n--- ERRO AO SALVAR OS DADOS: {e} ---")
        if collected_data:
            headers = collected_data[0].keys()
            print("\t".join(headers))
            for row in collected_data:
                print("\t".join(str(v) for v in row.values()))

if __name__ == "__main__":
    main()
