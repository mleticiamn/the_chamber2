import pygame
import sys
import random
import textwrap
import time

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("The Chamber - Experimento")
font_large = pygame.font.SysFont("courier", 50)
font = pygame.font.SysFont("courier", 22)
small_font = pygame.font.SysFont("courier", 16)
clock = pygame.time.Clock()

# --- Configurações do Experimento ---
MIN_PLAYERS = 3
MAX_PLAYERS = 7
COLOR_PRIMARY = (0, 200, 255)
COLOR_SECONDARY = (200, 255, 255)
COLOR_BG = (5, 5, 15)
COLOR_DANGER = (255, 50, 50)
COLOR_SUCCESS = (50, 255, 150)

# --- Banco de Casos (Histórias) ---
CASE_POOL = [
    {
        "id": 1,
        "type": "Real",
        "suspect_gender": "Feminino",
        "fragments": [
            "Uma médica é acusada de negligência após um paciente falecer durante um procedimento de emergência.",
            "Descobre-se que a médica estava em um plantão de 36 horas e havia alertado o hospital sobre a falta de equipamento.",
            "A autópsia revela que a condição do paciente já era terminal e o procedimento, por si só, era um último recurso de alto risco."
        ],
        "full_story": "Apesar do esforço sobre-humano em um ambiente precário, a médica não conseguiu salvar o paciente, cuja condição já era irreversível. O conselho de medicina a absolveu de todas as acusações.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 2,
        "type": "Fictícia",
        "suspect_gender": "Masculino",
        "fragments": [
            "Um programador é demitido e, na mesma noite, o servidor principal da empresa é completamente apagado.",
            "Investigadores descobrem que o acesso que apagou os dados veio do computador do programador.",
            "O programador alega que sua senha havia sido roubada por um colega com quem teve uma discussão."
        ],
        "full_story": "Embora a evidência circunstancial fosse forte, o colega confessou ter roubado a senha e sabotado o servidor como vingança, incriminando o programador. O programador era inocente.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 3,
        "type": "Real",
        "suspect_gender": "Masculino",
        "fragments": [
            "Um homem é visto fugindo de uma joalheria logo após o alarme de roubo disparar.",
            "A polícia o prende a duas quadras de distância com uma bolsa cheia de joias.",
            "O homem alega que o verdadeiro ladrão o ameaçou com uma arma e o forçou a carregar a bolsa."
        ],
        "full_story": "Câmeras de segurança de uma loja próxima confirmaram a história do homem. Elas mostraram o assaltante armado entregando a bolsa e o mandando correr, segundos antes de fugir em outra direção. O homem era uma vítima usada como isca.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 4,
        "type": "Fictícia",
        "suspect_gender": "Feminino",
        "fragments": [
            "Uma cientista é acusada de falsificar dados em uma pesquisa sobre um novo medicamento.",
            "A empresa farmacêutica que financiou o estudo publicou os resultados positivos apressadamente.",
            "A cientista afirma que seus dados preliminares foram mal interpretados e publicados sem sua aprovação final."
        ],
        "full_story": "Uma auditoria interna revelou que a diretoria da farmacêutica pressionou pela publicação, ignorando as notas de rodapé da cientista que indicavam a necessidade de mais testes. Ela era inocente da fraude, mas foi usada como bode expiatório.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 5,
        "type": "Real",
        "suspect_gender": "Masculino",
        "fragments": [
            "Um jovem ativista ambiental é preso por invadir uma propriedade privada de uma madeireira.",
            "Ele estava com equipamento fotográfico e documentava o desmatamento ilegal na área.",
            "A madeireira alega que ele danificou equipamentos caros durante a invasão."
        ],
        "full_story": "As fotos do ativista provaram o desmatamento ilegal, levando a uma investigação federal contra a madeireira. A acusação de dano foi retirada por falta de provas, e o ativista foi liberado, sendo considerado um herói ambiental.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 6,
        "type": "Fictícia",
        "suspect_gender": "Outro",
        "fragments": [
            "Uma figura proeminente da alta sociedade é acusada de roubar uma obra de arte durante um leilão de caridade.",
            "Testemunhas afirmam ter visto a pessoa perto da obra pouco antes de seu desaparecimento.",
            "A pessoa acusada alega que estava apenas admirando a peça e que é vítima de um mal-entendido."
        ],
        "full_story": "A obra de arte foi encontrada mais tarde no depósito do evento; um funcionário a guardou por engano pensando que não havia sido vendida. A acusação era infundada e baseada em preconceito contra o estilo excêntrico da pessoa.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 7,
        "type": "Real",
        "suspect_gender": "Feminino",
        "fragments": [
            "Uma mãe é acusada de sequestrar o próprio filho após uma amarga disputa pela custódia.",
            "Ela foi encontrada com a criança em outra cidade, violando uma ordem judicial.",
            "A mãe alega que o ex-parceiro era abusivo e que ela fugiu para proteger a criança de perigo iminente."
        ],
        "full_story": "Investigações posteriores e testemunhos confirmaram as alegações de abuso. Embora tenha violado a ordem judicial, a justiça considerou suas ações como um esforço para proteger o filho, e a custódia foi reavaliada a seu favor. Ela foi considerada inocente da acusação de sequestro malicioso.",
        "real_outcome": 0 # Inocente
    },
    {
        "id": 8,
        "type": "Fictícia",
        "suspect_gender": "Masculino",
        "fragments": [
            "Um chef de cozinha famoso tem seu restaurante fechado por violações sanitárias graves.",
            "Um ex-funcionário demitido recentemente fez a denúncia anônima.",
            "O chef alega que a denúncia é uma sabotagem e que as 'violações' foram plantadas."
        ],
        "full_story": "Durante a investigação, foi descoberto que o ex-funcionário, de fato, sabotou a cozinha na noite anterior à inspeção para se vingar da demissão. O restaurante foi reaberto e o chef inocentado.",
        "real_outcome": 0 # Inocente
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
    running, title = True, font_large.render("THE CHAMBER", True, COLOR_PRIMARY)
    start_button = Button((400, 550, 200, 50), "INICIAR JOGO")
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); start_button.check_hover(mouse_pos)
        screen.blit(title, title.get_rect(centerx=500, y=100))
        # Adicionar mais texto aqui se necessário
        start_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def choose_players_screen():
    players_num = MIN_PLAYERS
    minus_btn, plus_btn, ok_btn = Button((400, 250, 50, 50), "-"), Button((550, 250, 50, 50), "+"), Button((450, 350, 100, 50), "OK")
    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        title = font.render("Escolha o número de jogadores:", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=150))
        num_text = font_large.render(str(players_num), True, COLOR_SECONDARY)
        screen.blit(num_text, num_text.get_rect(center=(500, 275)))
        for btn in [minus_btn, plus_btn, ok_btn]: btn.check_hover(mouse_pos); btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if minus_btn.is_clicked(mouse_pos) and players_num > MIN_PLAYERS: players_num -= 1
                elif plus_btn.is_clicked(mouse_pos) and players_num < MAX_PLAYERS: players_num += 1
                elif ok_btn.is_clicked(mouse_pos): return players_num
        pygame.display.flip(); clock.tick(30)

def transition_screen(next_player_id):
    running, ready_button = True, Button((350, 400, 300, 50), "EU ESTOU PRONTO")
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); ready_button.check_hover(mouse_pos)
        pass_text = font.render("Passe o dispositivo para o", True, COLOR_SECONDARY)
        player_text = font_large.render(f"JOGADOR {next_player_id}", True, COLOR_PRIMARY)
        instruction_text = small_font.render("Os outros não devem olhar.", True, (150,150,150))
        screen.blit(pass_text, pass_text.get_rect(centerx=500, y=250))
        screen.blit(player_text, player_text.get_rect(centerx=500, y=300))
        screen.blit(instruction_text, instruction_text.get_rect(centerx=500, y=360))
        ready_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def demographics_screen(player_id):
    player = Player(player_id)
    active_field = "age"
    age_input_rect = pygame.Rect(350, 180, 300, 50)
    
    # ALTERADO: Mais opções de gênero e novo layout
    gender_buttons = {
        "Mulher cis": Button((150, 300, 200, 50), "Mulher cis"),
        "Homem cis": Button((370, 300, 200, 50), "Homem cis"),
        "Não binário": Button((590, 300, 200, 50), "Não binário"),
        "Mulher trans": Button((150, 360, 200, 50), "Mulher trans"),
        "Homem trans": Button((370, 360, 200, 50), "Homem trans"),
        "Outro": Button((590, 360, 200, 50), "Outro"),
    }
    
    exp_buttons = {i: Button((200 + (i-1)*130, 500, 100, 50), str(i)) for i in range(1, 6)}
    confirm_button = Button((400, 610, 200, 50), "CONFIRMAR")

    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        title = font_large.render(f"DADOS DO JOGADOR {player_id}", True, COLOR_PRIMARY)
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
    culpado_button = Button((225, 500, 250, 80), "CULPADO (1)", text_color=COLOR_DANGER, border_color=COLOR_DANGER)
    inocente_button = Button((525, 500, 250, 80), "INOCENTE (0)", text_color=COLOR_SUCCESS, border_color=COLOR_SUCCESS)
    start_time = time.time()
    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); culpado_button.check_hover(mouse_pos); inocente_button.check_hover(mouse_pos)
        title = font.render(f"JOGADOR {player.id} - RODADA {round_num}", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=50))
        case_info = f"Caso #{case['id']} | Gênero do Suspeito: {case['suspect_gender']} | Tipo: {case['type']}"
        screen.blit(small_font.render(case_info, True, COLOR_SECONDARY), small_font.render(case_info, True, COLOR_SECONDARY).get_rect(centerx=500, y=120))
        fragment_box = pygame.Rect(100, 180, 800, 250)
        pygame.draw.rect(screen, COLOR_PRIMARY, fragment_box, 2, border_radius=10)
        y_offset = fragment_box.y + 30
        for i in range(round_num):
            for line in wrap_text_pixel(f"Info {i+1}: {case['fragments'][i]}", font, fragment_box.width - 40):
                screen.blit(font.render(line, True, COLOR_SECONDARY), font.render(line, True, COLOR_SECONDARY).get_rect(centerx=fragment_box.centerx, y=y_offset)); y_offset += 30
            y_offset += 20
        culpado_button.draw(screen); inocente_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                decision_time = round(time.time() - start_time, 2)
                if culpado_button.is_clicked(mouse_pos): return 1, decision_time
                if inocente_button.is_clicked(mouse_pos): return 0, decision_time
        pygame.display.flip(); clock.tick(30)

def final_revelation_screen(case):
    running, quit_button = True, Button((400, 630, 200, 50), "FIM DO CASO")
    outcome_text = "CULPADO" if case['real_outcome'] == 1 else "INOCENTE"
    outcome_color = COLOR_DANGER if case['real_outcome'] == 1 else COLOR_SUCCESS
    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); quit_button.check_hover(mouse_pos)
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
        pygame.display.flip(); clock.tick(30)

# ====== LÓGICA PRINCIPAL DO EXPERIMENTO ======
def main():
    intro_screen()
    num_players = choose_players_screen()
    
    players = []
    for i in range(1, num_players + 1):
        transition_screen(i)
        players.append(demographics_screen(i))
        
    current_case = random.choice(CASE_POOL)
    collected_data = []
    session_id = f"SESSAO_{int(time.time())}"
    player_votes_history = {p.id: [] for p in players}

    for round_num in range(1, 4):
        for player in players:
            transition_screen(player.id)
            decision, decision_time = voting_screen(player, current_case, round_num)
            mudanca_voto = 0
            if round_num > 1 and decision != player_votes_history[player.id][-1]:
                mudanca_voto = 1
            player_votes_history[player.id].append(decision)
            data_row = {
                "ID_Sessao": session_id, "ID_Participante": f"P{player.id}", "Num_Rodada": round_num,
                "Idade": player.age, "Genero_Participante": player.gender, "Experiencia_com_Jogos": player.experience,
                "ID_Caso": current_case['id'], "Tipo_de_Historia": current_case['type'], "Genero_Suspeito": current_case['suspect_gender'],
                "Tempo_de_Decisao_s": decision_time, "Decisao_Final": decision, "Mudanca_de_Voto": mudanca_voto,
                "Resultado_Real_Caso": current_case['real_outcome'], "Num_Jogadores_Sessao": num_players
            }
            collected_data.append(data_row)

    final_revelation_screen(current_case)

    print("\n--- DADOS COLETADOS NA SESSÃO ---")
    if collected_data:
        headers = collected_data[0].keys()
        print("\t".join(headers))
        for row in collected_data:
            print("\t".join(str(v) for v in row.values()))
    print("\n--- FIM DOS DADOS ---")

if __name__ == "__main__":
    main()
