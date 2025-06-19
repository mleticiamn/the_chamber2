import pygame
import sys
import random
import textwrap

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("THE CHAMBER - A Social Experiment Game")
font_large = pygame.font.SysFont("courier", 50)
font = pygame.font.SysFont("courier", 22)
small_font = pygame.font.SysFont("courier", 16)
clock = pygame.time.Clock()

# --- Game Configuration ---
MIN_PLAYERS = 3
MAX_PLAYERS = 7
MAX_ROUNDS = 6
COLOR_PRIMARY = (0, 200, 255)
COLOR_SECONDARY = (200, 255, 255)
COLOR_BG = (5, 5, 15)
COLOR_DANGER = (255, 50, 50)
COLOR_TRUST = (50, 255, 150)

# --- Histórias (Todos Inocentes) ---
STORY_POOL = [
    ("Eu era paramédico. Numa noite caótica, usei um atalho para chegar a uma vítima de acidente, mas bati a ambulância. O atraso foi de poucos minutos, mas a pessoa não resistiu. Fui investigado e absolvido, pois a condição dela já era fatal, mas a dúvida de que aqueles minutos poderiam ter feito a diferença me assombra.", 
     "Por minha causa, a ajuda atrasou... e a pessoa não sobreviveu.", False),

    ("No meu antigo emprego, descobri que meu gerente, um bom homem em apuros financeiros, estava desviando pequenas quantias. Em vez de denunciá-lo e arruinar sua família, eu o confrontei em particular. Ele prometeu devolver tudo e o fez. Guardei o segredo, mas sempre temi ser visto como cúmplice.", 
     "Eu sabia do roubo o tempo todo... e acobertei o responsável.", False),

    ("Minha irmã mais nova estava num relacionamento abusivo. Uma noite, ela me ligou chorando. O namorado dela havia pegado seu passaporte para impedi-la de viajar. Fui até lá e, enquanto ele estava no banho, entrei no quarto e peguei o passaporte de volta. Ele nunca soube que fui eu, achou que tinha perdido, e minha irmã conseguiu sair da cidade em segurança.", 
     "Eu invadi a casa... e roubei um documento importante de lá.", False),

    ("Na faculdade, eu fazia parte de um grupo de ativismo. Numa manifestação que deveria ser pacífica, um membro se exaltou e quebrou a vitrine de uma loja. Em meio ao caos e sirenes, todos nós corremos. Nunca contei a ninguém que eu estava lá e vi quem foi o culpado, por medo de ser associado ao ato.", 
     "Eu estava na cena do crime quando tudo aconteceu... e fugi com os outros.", False),

    ("Enquanto voltava para casa, encontrei uma carteira no chão com uma grande quantidade de dinheiro e todos os documentos. Por um momento, a tentação de ficar com o dinheiro foi enorme, pois eu estava cheio de dívidas. Hesitei por quase uma hora, mas no fim minha consciência pesou e eu devolvi a carteira intacta ao dono.", 
     "Eu estava com uma fortuna que não era minha em mãos... e um mar de dívidas para pagar.", False),
    
    ("Eu trabalhava como pesquisador em um laboratório. Estávamos perto de uma descoberta, mas um lote crucial de amostras foi contaminado por um erro meu no manuseio. Em vez de admitir e atrasar o projeto em meses, joguei as amostras fora e culpei uma 'falha no equipamento de refrigeração'. A pesquisa foi refeita e eventualmente funcionou, mas foi baseada numa mentira minha.",
     "Eu destruí evidências cruciais... e falsifiquei um relatório para encobrir.", False),

    ("Meu melhor amigo ia me fazer uma visita surpresa, mas eu vi uma mensagem sem querer e descobri. Fingi surpresa total quando ele chegou, com direito a gritos e espanto. A alegria dele em me surpreender foi tão genuína que nunca tive coragem de contar que eu já sabia de tudo. Sinto que nossa amizade tem um pequeno pilar falso.",
     "Toda a alegria dele foi baseada em uma encenação... eu menti na cara dele.", False),

    ("Eu vendi meu carro antigo para um jovem comprador. Durante a negociação, 'esqueci' de mencionar um problema intermitente na caixa de câmbio que só aparecia em viagens longas. Omiti a informação para conseguir um preço melhor. Não é ilegal, mas sei que não foi honesto.",
     "Eu omiti uma informação deliberadamente... para enganar o comprador e lucrar mais.", False),
    
    ("Durante uma prova importante na universidade, vi o aluno mais inteligente da turma colar descaradamente. O professor não percebeu. Fiquei em um dilema: se eu o denunciasse, ele seria expulso; se eu ficasse quieto, seria injusto com todos os outros. Optei por não dizer nada e conviver com isso.",
     "Eu tinha conhecimento de uma fraude... e me recusei a cooperar com a verdade.", False),

    ("Meu vizinho viajou e me pediu para cuidar de seu gato. Sem querer, deixei a porta aberta e o gato fugiu. Passei a noite procurando, sem sucesso. No dia seguinte, comprei um gato idêntico numa pet shop e o coloquei na casa dele. O vizinho voltou e nunca notou a troca. Sinto um peso enorme por ter 'substituído' seu animal de estimação.",
     "Houve um desaparecimento sob minha vigilância... então eu encobri e forjei a identidade do substituto.", False),

    ("Recebi um depósito por engano na minha conta bancária, uma quantia considerável. A regra do banco é clara: eu deveria informar imediatamente. Mas eu estava passando por um aperto financeiro. Esperei duas semanas para ver se alguém notaria. Ninguém notou. Só então, com a consciência pesada, liguei para o banco e relatei o erro. O dinheiro foi estornado.",
     "Uma grande quantia em dinheiro apareceu na minha conta... e eu a mantive em segredo por semanas.", False),

    ("Eu estava responsável por regar a planta rara e caríssima de um amigo durante sua viagem. Esqueci por vários dias e a planta morreu. Em pânico, fui a uma floricultura especializada, gastei uma fortuna e comprei uma planta idêntica para colocar no lugar. Meu amigo elogiou como a planta estava 'ainda mais bonita'.",
     "O original morreu em minhas mãos... então eu o substituí por uma cópia.", False),

    ("Numa entrevista de emprego, menti sobre ser fluente em espanhol, pois era um requisito. Consegui o emprego. Na primeira semana, descobri que teria uma videoconferência com um cliente do Chile. Passei três noites em claro, usando aplicativos e fazendo aulas intensivas, só para conseguir me virar na reunião. Foi um sufoco, mas ninguém desconfiou.",
     "Eu falsifiquei uma qualificação essencial... e enganei a todos.", False),

    ("Eu gerenciava as redes sociais de um pequeno negócio. Para aumentar os números rapidamente, comprei um pacote de seguidores falsos (bots). As métricas inflaram, o dono ficou feliz com o 'crescimento', mas eu sei que o engajamento é uma farsa e a qualquer momento a plataforma pode remover todos os fakes.",
     "Os números que eu apresentei eram uma fraude... eu comprei o resultado.", False),

    ("Eu peguei emprestado um livro raro da biblioteca da faculdade. Em casa, derramei café nele, manchando várias páginas. Em vez de pagar a multa altíssima, usei um secador e um pouco de maquiagem para disfarçar a mancha. Devolvi o livro e o bibliotecário não notou nada. Alguém um dia vai descobrir.",
     "Eu danifiquei propriedade alheia... e adulterei a cena para esconder as provas.", False)
]

# --- Helper Functions & Classes ---
def draw_background():
    screen.fill(COLOR_BG)
    for x in range(0, 1000, 20): pygame.draw.line(screen, (15, 25, 40), (x, 0), (x, 700), 1)
    for y in range(0, 700, 20): pygame.draw.line(screen, (15, 25, 40), (0, y), (1000, y), 1)

def wrap_text_pixel(text, font, max_pixel_width):
    words, lines, current_line = text.split(' '), [], ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_pixel_width: current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

class Player:
    def __init__(self, player_id, story, fragment):
        self.id, self.story, self.fragment = player_id, story, fragment
        self.is_eliminated, self.votes = False, 0

class Button:
    def __init__(self, rect, text, text_color=COLOR_PRIMARY, border_color=COLOR_PRIMARY, hover_color=COLOR_SECONDARY):
        self.rect, self.original_y = pygame.Rect(rect), rect[1]
        self.text, self.text_color = text, text_color
        self.border_color, self.hover_color, self.is_hovered = border_color, hover_color, False

    def draw(self, surface, y_offset=0):
        self.rect.y = self.original_y + y_offset
        color = self.hover_color if self.is_hovered else self.border_color
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=5)
        label = font.render(self.text, True, color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def check_hover(self, pos): self.is_hovered = self.rect.collidepoint(pos)
    def is_clicked(self, pos): return self.rect.collidepoint(pos)

# --- Game Screens ---
def intro_screen():
    running, title = True, font_large.render("THE CHAMBER", True, COLOR_PRIMARY)
    dilemma_lines = ["VOCÊ E DESCONHECIDOS ESTÃO PRESOS EM UM JOGO.", "A CADA RODADA, SUAS HISTÓRIAS SERÃO REVELADAS EM PEDAÇOS.", "VOTEM PARA ELIMINAR AQUELE EM QUEM MENOS CONFIAM.", "Até onde você iria para sobreviver?"]
    start_button = Button((400, 550, 200, 50), "INICIAR JOGO")
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); start_button.check_hover(mouse_pos)
        screen.blit(title, title.get_rect(centerx=500, y=100))
        for i, line in enumerate(dilemma_lines):
            line_surf = small_font.render(line, True, COLOR_SECONDARY)
            screen.blit(line_surf, line_surf.get_rect(centerx=500, y=250 + i * 35))
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
        pass_text, player_text = font.render("Passe o dispositivo para o", True, COLOR_SECONDARY), font_large.render(f"JOGADOR {next_player_id}", True, COLOR_PRIMARY)
        instruction_text = small_font.render("Os outros não devem olhar.", True, (150,150,150))
        screen.blit(pass_text, pass_text.get_rect(centerx=500, y=250)); screen.blit(player_text, player_text.get_rect(centerx=500, y=300)); screen.blit(instruction_text, instruction_text.get_rect(centerx=500, y=360))
        ready_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def show_full_story(player):
    ok_button, story_lines = Button((400, 600, 200, 50), "MEMORIZEI"), wrap_text_pixel(player.story, small_font, 900)
    running = True
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); ok_button.check_hover(mouse_pos)
        title = font.render(f"Jogador {player.id}, esta é a sua verdade:", True, COLOR_PRIMARY)
        screen.blit(title, (50, 50))
        for i, line in enumerate(story_lines):
            screen.blit(small_font.render(line, True, COLOR_SECONDARY), (50, 120 + i * 25))
        ok_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def round_transition_screen(round_num):
    running, start_button = True, Button((380, 400, 240, 50), "COMEÇAR RODADA")
    title_text, sub_text = (f"FASE DE HISTÓRIAS CONCLUÍDA", f"A Rodada {round_num} de discussão vai começar.") if round_num == 1 else (f"RODADA {round_num - 1} FINALIZADA", f"Preparem-se para a Rodada {round_num}.")
    title_surf, sub_surf = font_large.render(title_text, True, COLOR_PRIMARY), font.render(sub_text, True, COLOR_SECONDARY)
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); start_button.check_hover(mouse_pos)
        screen.blit(title_surf, title_surf.get_rect(centerx=500, y=250)); screen.blit(sub_surf, sub_surf.get_rect(centerx=500, y=320))
        start_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def discussion_screen(players, round_num):
    running, start_voting_button = True, Button((380, 630, 240, 50), "INICIAR VOTAÇÃO")
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); start_voting_button.check_hover(mouse_pos)
        title, instr = font_large.render(f"RODADA {round_num} - DISCUSSÃO", True, COLOR_PRIMARY), font.render("Discutam os fragmentos. Façam suas acusações e defesas.", True, COLOR_SECONDARY)
        screen.blit(title, title.get_rect(centerx=500, y=30)); screen.blit(instr, instr.get_rect(centerx=500, y=80))
        for i, p in enumerate(players):
            col, row = i % 4, i // 4; x, y = 50 + col * 240, 120 + row * 260
            box_rect = pygame.Rect(x, y, 220, 170)
            box_color, text_color = ((30,30,30), (100,100,100)) if p.is_eliminated else (COLOR_PRIMARY, COLOR_SECONDARY)
            pygame.draw.rect(screen, box_color, box_rect, 2, border_radius=5)
            screen.blit(font.render(f"Jogador {p.id}", True, box_color), (x + 10, y + 10))
            if p.is_eliminated:
                screen.blit(font_large.render("ELIMINADO", True, COLOR_DANGER), font_large.render("ELIMINADO", True, COLOR_DANGER).get_rect(center=box_rect.center))
            else:
                for j, line in enumerate(wrap_text_pixel(p.fragment, small_font, box_rect.width - 20)):
                    screen.blit(small_font.render(line, True, text_color), (x + 10, y + 40 + j * 20))
        start_voting_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_voting_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def voter_transition_screen(next_voter_id):
    running, ready_button = True, Button((350, 400, 300, 50), "ESTOU PRONTO PARA VOTAR")
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); ready_button.check_hover(mouse_pos)
        title_text, pass_text = font.render("VOTO REGISTRADO.", True, COLOR_SECONDARY), font.render("Passe o dispositivo para o", True, COLOR_SECONDARY)
        player_text = font_large.render(f"JOGADOR {next_voter_id}", True, COLOR_PRIMARY)
        screen.blit(title_text, title_text.get_rect(centerx=500, y=200)); screen.blit(pass_text, pass_text.get_rect(centerx=500, y=280)); screen.blit(player_text, player_text.get_rect(centerx=500, y=320))
        ready_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def vote_tally_screen(players, eliminated_player):
    running = True
    title_text, title_color = (f"JOGADOR {eliminated_player.id} FOI ELIMINADO", COLOR_DANGER) if eliminated_player else ("NINGUÉM FOI ELIMINADO (EMPATE)", COLOR_PRIMARY)
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        y_offset = 60
        for i, line in enumerate(wrap_text_pixel(title_text, font_large, 900)):
            title_surf = font_large.render(line, True, title_color)
            screen.blit(title_surf, title_surf.get_rect(centerx=500, y=y_offset)); y_offset += 50
        
        # NOVO: Revela que o jogador eliminado era inocente
        if eliminated_player:
            innocent_text = font.render(f"Jogador {eliminated_player.id} era inocente.", True, COLOR_DANGER)
            screen.blit(innocent_text, innocent_text.get_rect(centerx=500, y=y_offset + 10)); y_offset += 40
        
        votes_y, vote_title = y_offset + 40, font.render("Votos da rodada:", True, COLOR_PRIMARY)
        screen.blit(vote_title, vote_title.get_rect(centerx=500, y=y_offset))
        votes_y += 40
        for p in sorted(players, key=lambda p: p.id):
            if p.votes > 0:
                screen.blit(font.render(f"Jogador {p.id} recebeu {p.votes} voto(s)", True, COLOR_SECONDARY), font.render(f"Jogador {p.id} recebeu {p.votes} voto(s)", True, COLOR_SECONDARY).get_rect(centerx=500, y=votes_y)); votes_y += 40
        
        button_to_show = Button((400, 600, 200, 50), "CONTINUAR")
        button_to_show.check_hover(mouse_pos); button_to_show.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_to_show.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def round_screen(players, round_num, max_rounds):
    active_players, votes = [p for p in players if not p.is_eliminated], {}
    vote_buttons = {}
    for i, p in enumerate(players):
        col, row = i % 4, i // 4; x, y = 50 + col * 240, 120 + row * 280
        rect = (x + (220 - 200) // 2, y + 185, 200, 40)
        vote_buttons[p.id] = Button(rect, f"Votar Jogador {p.id}")
    peace_button = Button((350, 630, 300, 50), "NÃO HÁ CULPADOS", text_color=COLOR_PRIMARY, border_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY)
    current_voter_index = 0
    while len(votes) < len(active_players):
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        voter = active_players[current_voter_index]
        title, instr = font.render(f"RODADA {round_num} - Vez do Jogador {voter.id}", True, COLOR_PRIMARY), font.render("Vote em quem você acredita ser o culpado.", True, COLOR_SECONDARY)
        screen.blit(title, title.get_rect(centerx=500, y=30)); screen.blit(instr, instr.get_rect(centerx=500, y=65))
        for i, p in enumerate(players):
            col, row = i % 4, i // 4; x, y = 50 + col * 240, 120 + row * 280
            box_rect = pygame.Rect(x, y, 220, 170)
            box_color, text_color = ((30,30,30), (100,100,100)) if p.is_eliminated else (COLOR_PRIMARY, COLOR_SECONDARY)
            pygame.draw.rect(screen, box_color, box_rect, 2, border_radius=5)
            screen.blit(font.render(f"Jogador {p.id}", True, box_color), (x + 10, y + 10))
            if p.is_eliminated:
                screen.blit(font_large.render("ELIMINADO", True, COLOR_DANGER), font_large.render("ELIMINADO", True, COLOR_DANGER).get_rect(center=box_rect.center))
            else:
                for j, line in enumerate(wrap_text_pixel(p.fragment, small_font, box_rect.width - 20)):
                    screen.blit(small_font.render(line, True, text_color), (x + 10, y + 40 + j * 20))
                vote_buttons[p.id].check_hover(mouse_pos); vote_buttons[p.id].draw(screen)
        peace_button.check_hover(mouse_pos); peace_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                action_taken = False
                if peace_button.is_clicked(event.pos):
                    votes[voter.id] = 'peace'; action_taken = True
                else:
                    for player_id, button in vote_buttons.items():
                        if button.is_clicked(event.pos):
                            if any(p.id == player_id for p in active_players):
                                votes[voter.id] = player_id; action_taken = True; break
                if action_taken:
                    current_voter_index += 1
                    if len(votes) < len(active_players):
                        voter_transition_screen(active_players[current_voter_index].id)
        pygame.display.flip(); clock.tick(30)
    if all(vote == 'peace' for vote in votes.values()):
        return 'secret_pact', None
    for p in players: p.votes = 0 
    for voted_id in [v for v in votes.values() if isinstance(v, int)]:
        for p in players:
            if p.id == voted_id: p.votes += 1
    max_votes, eliminated_player, is_tie = 0, None, False
    for p in active_players:
        if p.votes > max_votes: max_votes, eliminated_player, is_tie = p.votes, p, False
        elif p.votes == max_votes and max_votes > 0: is_tie = True
    if is_tie: eliminated_player = None 
    return 'voted', eliminated_player

def end_game_screen(players, reason):
    quit_button = Button((400, 630, 200, 50), "SAIR DO JOGO")
    scroll_y, content_height = 0, 0
    title_text, sub_text, revelation_text = "", "", "A verdade é: não havia um criminoso. Todos eram inocentes, cada um com seus próprios segredos."
    title_color = COLOR_PRIMARY
    if reason == "secret_pact":
        title_text, sub_text, title_color = "O PACTO SILENCIOSO", "Sem saberem as escolhas uns dos outros, todos optaram pela confiança. Vocês quebraram o ciclo e venceram juntos.", COLOR_TRUST
    elif reason == "max_rounds" or reason == "survivors":
        title_text, sub_text, title_color = "O CICLO DE DESCONFIANÇA VENCEU", "O jogo terminou, deixando um rastro de acusações. Os sobreviventes... apenas sobreviveram.", COLOR_DANGER
    all_surfaces = []
    y_offset = 40
    for line in wrap_text_pixel(title_text, font_large, 900):
        all_surfaces.append((font_large.render(line, True, title_color), font_large.render(line, True, title_color).get_rect(centerx=500, top=y_offset))); y_offset += 50
    y_offset += 20
    for line in wrap_text_pixel(sub_text, font, 900):
        all_surfaces.append((font.render(line, True, COLOR_SECONDARY), font.render(line, True, COLOR_SECONDARY).get_rect(centerx=500, top=y_offset))); y_offset += 30
    y_offset += 20
    line_surf, line_surf2 = pygame.Surface((800, 1)), pygame.Surface((800, 1)); line_surf.fill(COLOR_PRIMARY); line_surf2.fill(COLOR_PRIMARY)
    all_surfaces.append((line_surf, line_surf.get_rect(centerx=500, top=y_offset))); y_offset += 20
    for line in wrap_text_pixel(revelation_text, font, 900):
        all_surfaces.append((font.render(line, True, (255, 255, 100)), font.render(line, True, (255, 255, 100)).get_rect(centerx=500, top=y_offset))); y_offset += 30
    y_offset += 20
    all_surfaces.append((line_surf2, line_surf2.get_rect(centerx=500, top=y_offset))); y_offset += 30
    content_height = y_offset
    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and content_height > 700: scroll_y = min(scroll_y + 30, 0)
                if event.button == 5 and content_height > 700: scroll_y = max(scroll_y - 30, 700 - content_height)
                # O botão de sair não tem offset, então checamos a posição original do mouse
                if quit_button.rect.collidepoint(mouse_pos): pygame.quit(), sys.exit()
        
        for surf, rect in all_surfaces:
            screen.blit(surf, (rect.x, rect.y + scroll_y))

        quit_button_original_pos = quit_button.rect.copy()
        quit_button_original_pos.y = quit_button.original_y
        
        pygame.draw.rect(screen, COLOR_BG, quit_button_original_pos)
        quit_button.check_hover(mouse_pos)
        quit_button.draw(screen)
        
        pygame.display.flip(); clock.tick(30)

# ====== MAIN GAME LOGIC ======
def main():
    intro_screen()
    num_players = choose_players_screen()
    final_stories = random.sample(STORY_POOL, num_players if num_players <= len(STORY_POOL) else len(STORY_POOL))
    players = []
    for i, (story, fragment, _) in enumerate(final_stories):
        p = Player(i + 1, story, fragment)
        players.append(p)
    for p in sorted(players, key=lambda p: p.id):
        transition_screen(p.id)
        show_full_story(p)
    round_num = 1
    while round_num <= MAX_ROUNDS:
        round_transition_screen(round_num)

        if len([p for p in players if not p.is_eliminated]) <= 2:
            end_game_screen(players, "survivors")
            break
            
        discussion_screen(players, round_num)
        
        vote_result, eliminated_player = round_screen(players, round_num, MAX_ROUNDS)
        if vote_result == 'secret_pact':
            end_game_screen(players, "secret_pact")
            break
        
        if eliminated_player:
            eliminated_player.is_eliminated = True
        
        vote_tally_screen(players, eliminated_player)
        
        round_num += 1
    else: 
        end_game_screen(players, "max_rounds")

if __name__ == "__main__":
    main()