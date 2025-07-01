import pygame
import sys
import random
import textwrap

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("THE CHAMBER - Leitura Mental")
font_large = pygame.font.SysFont("courier", 50)
font = pygame.font.SysFont("courier", 22)
small_font = pygame.font.SysFont("courier", 16)
clock = pygame.time.Clock()

# --- Game Configuration ---
MIN_PLAYERS = 3
MAX_PLAYERS = 7
MAX_ROUNDS = 1 # ALTERADO: O jogo agora tem apenas 1 rodada
COLOR_PRIMARY = (0, 200, 255)
COLOR_SECONDARY = (200, 255, 255)
COLOR_BG = (5, 5, 15)
COLOR_DANGER = (255, 50, 50)
COLOR_SUCCESS = (50, 255, 150)

# --- Baralho de Perguntas ---
QUESTION_POOL = [
    "Você contaria uma mentira para proteger um amigo de uma consequência grave?",
    "Você aceitaria 1 milhão de reais para nunca mais ver seu melhor amigo?",
    "Você denunciaria um colega de trabalho por roubar algo pequeno da empresa?",
    "Você sacrificaria a vida de um animal de estimação para salvar um estranho?",
    "Você leria o diário ou as mensagens privadas do seu parceiro(a) se tivesse a chance?",
    "Você voltaria no tempo para consertar seu maior erro, mesmo que isso mudasse quem você é hoje?",
    "Você preferiria ter uma vida extremamente feliz, mas curta, ou uma vida normal, mas longa?",
    "Você aceitaria um emprego que paga muito bem, mas que você considera eticamente questionável?",
    "Você perdoaria uma traição?",
    "Você revelaria um segredo de outra pessoa se isso significasse fazer justiça?",
    "Você escolheria saber a data exata da sua morte?",
    "Você preferiria ser amado por todos, mas não respeitado?",
    "Você desistiria de toda a sua privacidade em troca de segurança absoluta?",
    "Você prefere a verdade dolorosa ou uma mentira confortável?",
    "Você arriscaria sua vida para salvar um membro da sua família?",
    "Você usaria um 'bot' para vencer em um jogo online competitivo?",
    "Se você pudesse ser invisível por um dia, você faria algo ilegal?",
    "Você acredita em segundas chances para tudo?",
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
    def __init__(self, player_id):
        self.id, self.score = player_id, 0
        self.hand, self.chosen_question, self.secret_answer = [], None, None

class Button:
    def __init__(self, rect, text, text_color=COLOR_PRIMARY, border_color=COLOR_PRIMARY, hover_color=COLOR_SECONDARY):
        self.rect, self.original_y = pygame.Rect(rect), rect[1]
        self.text, self.text_color = text, text_color
        self.border_color, self.hover_color, self.is_hovered = border_color, hover_color, False

    def draw(self, surface):
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
    dilemma_lines = ["UM JOGO SOBRE LER AS PESSOAS.", "QUEM VOCÊ ACHA QUE CONHECE MELHOR?", "ESCOLHA UMA PERGUNTA. RESPONDA EM SECRETO.", "ADIVINHE AS RESPOSTAS DOS OUTROS PARA PONTUAR.", "Prepare-se para se surpreender."]
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

def market_draft_screen(current_player, market_cards, pick_number):
    running, selected_card_index = True, -1
    MAX_COLS, CARD_WIDTH, CARD_HEIGHT, GAP_X, GAP_Y = 4, 220, 160, 20, 20
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        title = font_large.render(f"VEZ DO JOGADOR {current_player.id}", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=50))
        instr = font.render(f"Escolha sua {pick_number}ª carta do mercado.", True, COLOR_SECONDARY)
        screen.blit(instr, instr.get_rect(centerx=500, y=120))
        card_rects = []
        for i, card_text in enumerate(market_cards):
            row, col = i // MAX_COLS, i % MAX_COLS
            x = (1000 - (MAX_COLS * CARD_WIDTH + (MAX_COLS - 1) * GAP_X)) // 2 + col * (CARD_WIDTH + GAP_X)
            y = 180 + row * (CARD_HEIGHT + GAP_Y)
            card_rects.append(pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT))
        for i, rect in enumerate(card_rects):
            color = COLOR_SUCCESS if i == selected_card_index else COLOR_PRIMARY
            pygame.draw.rect(screen, color, rect, 2, border_radius=10)
            for j, line in enumerate(wrap_text_pixel(market_cards[i], small_font, rect.width - 20)):
                screen.blit(small_font.render(line, True, COLOR_SECONDARY), small_font.render(line, True, COLOR_SECONDARY).get_rect(centerx=rect.centerx, y=rect.y + 20 + j * 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        chosen_card = market_cards.pop(i)
                        return chosen_card, market_cards
        pygame.display.flip(); clock.tick(30)

def choose_main_question_screen(player):
    running, selected_card_index = True, -1
    card_rects = [pygame.Rect(200, 250, 250, 150), pygame.Rect(550, 250, 250, 150)]
    confirm_button = Button((400, 500, 200, 50), "CONFIRMAR")
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        title = font_large.render(f"JOGADOR {player.id}", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=50))
        instr = font.render("Escolha qual das suas duas cartas será a principal.", True, COLOR_SECONDARY)
        screen.blit(instr, instr.get_rect(centerx=500, y=120))
        for i, rect in enumerate(card_rects):
            color = COLOR_SUCCESS if i == selected_card_index else COLOR_PRIMARY
            pygame.draw.rect(screen, color, rect, 2, border_radius=10)
            for j, line in enumerate(wrap_text_pixel(player.hand[i], small_font, rect.width - 20)):
                screen.blit(small_font.render(line, True, COLOR_SECONDARY), small_font.render(line, True, COLOR_SECONDARY).get_rect(centerx=rect.centerx, y=rect.y + 20 + j * 20))
        if selected_card_index != -1:
            confirm_button.check_hover(mouse_pos); confirm_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos): selected_card_index = i
                if selected_card_index != -1 and confirm_button.is_clicked(mouse_pos):
                    player.chosen_question = player.hand[selected_card_index]; running = False
        pygame.display.flip(); clock.tick(30)

def answering_screen(player):
    running, yes_button, no_button = True, Button((225, 400, 250, 80), "SIM", text_color=COLOR_SUCCESS, border_color=COLOR_SUCCESS), Button((525, 400, 250, 80), "NÃO", text_color=COLOR_DANGER, border_color=COLOR_DANGER)
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); yes_button.check_hover(mouse_pos); no_button.check_hover(mouse_pos)
        title = font_large.render(f"JOGADOR {player.id}", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=100))
        question_box = pygame.Rect(100, 200, 800, 150)
        pygame.draw.rect(screen, COLOR_PRIMARY, question_box, 2, border_radius=10)
        for i, line in enumerate(wrap_text_pixel(player.chosen_question, font, question_box.width - 40)):
            screen.blit(font.render(line, True, COLOR_SECONDARY), font.render(line, True, COLOR_SECONDARY).get_rect(centerx=question_box.centerx, y=question_box.y + 30 + i * 30))
        instr = font.render("Responda secretamente:", True, COLOR_SECONDARY)
        screen.blit(instr, instr.get_rect(centerx=500, y=360))
        yes_button.draw(screen); no_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.is_clicked(mouse_pos): player.secret_answer = True; running = False
                elif no_button.is_clicked(mouse_pos): player.secret_answer = False; running = False
        pygame.display.flip(); clock.tick(30)

def guessing_phase_screen(players, current_player, round_num):
    target_player, guess = None, None
    player_buttons = {p.id: Button((100, 150 + i*60, 200, 50), f"Jogador {p.id}") for i, p in enumerate(players) if p.id != current_player.id}
    guess_buttons = {"sim": Button((600, 200, 150, 60), "SIM", text_color=COLOR_SUCCESS, border_color=COLOR_SUCCESS), "nao": Button((600, 300, 150, 60), "NÃO", text_color=COLOR_DANGER, border_color=COLOR_DANGER)}
    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos()
        title = font_large.render(f"VEZ DO JOGADOR {current_player.id}", True, COLOR_PRIMARY)
        screen.blit(title, title.get_rect(centerx=500, y=50))
        screen.blit(font.render("1. Escolha um alvo:", True, COLOR_SECONDARY), (100, 120))
        for p_id, btn in player_buttons.items():
            if target_player and p_id == target_player.id: btn.border_color, btn.text_color = COLOR_SUCCESS, COLOR_SUCCESS
            else: btn.border_color, btn.text_color = COLOR_PRIMARY, COLOR_PRIMARY
            btn.check_hover(mouse_pos); btn.draw(screen)
        if target_player:
            screen.blit(font.render("2. Qual a resposta dele(a) para:", True, COLOR_SECONDARY), (400, 120))
            q_box = pygame.Rect(400, 150, 500, 180)
            pygame.draw.rect(screen, COLOR_PRIMARY, q_box, 1)
            for i, line in enumerate(wrap_text_pixel(target_player.chosen_question, small_font, q_box.width - 20)):
                screen.blit(small_font.render(line, True, COLOR_SECONDARY), (q_box.x + 10, q_box.y + 10 + i * 20))
            for g, btn in guess_buttons.items(): btn.check_hover(mouse_pos); btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not target_player:
                    for p_id, btn in player_buttons.items():
                        if btn.is_clicked(mouse_pos):
                            target_player = next(p for p in players if p.id == p_id)
                else:
                    if guess_buttons["sim"].is_clicked(mouse_pos): return target_player, True
                    elif guess_buttons["nao"].is_clicked(mouse_pos): return target_player, False
        pygame.display.flip(); clock.tick(30)

def show_result_screen(guesser, target, result_correct):
    running, continue_button = True, Button((400, 550, 200, 50), "CONTINUAR")
    if result_correct:
        title_text, title_color, sub_text = "CORRETO!", COLOR_SUCCESS, f"Jogador {guesser.id} ganhou 1 ponto. Jogador {target.id} perdeu 1 ponto."
    else:
        title_text, title_color, sub_text = "ERRADO!", COLOR_DANGER, "Ninguém pontua."
    answer_text = "'SIM'" if target.secret_answer else "'NÃO'"
    reveal_text = f"A resposta do Jogador {target.id} era {answer_text}."
    while running:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); continue_button.check_hover(mouse_pos)
        screen.blit(font_large.render(title_text, True, title_color), font_large.render(title_text, True, title_color).get_rect(centerx=500, y=150))
        screen.blit(font.render(reveal_text, True, COLOR_SECONDARY), font.render(reveal_text, True, COLOR_SECONDARY).get_rect(centerx=500, y=250))
        screen.blit(font.render(sub_text, True, COLOR_PRIMARY), font.render(sub_text, True, COLOR_PRIMARY).get_rect(centerx=500, y=350))
        continue_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and continue_button.is_clicked(mouse_pos): running = False
        pygame.display.flip(); clock.tick(30)

def end_game_screen(players):
    quit_button = Button((400, 630, 200, 50), "SAIR DO JOGO")
    winner = sorted(players, key=lambda p: p.score, reverse=True)[0]
    while True:
        draw_background(); mouse_pos = pygame.mouse.get_pos(); quit_button.check_hover(mouse_pos)
        screen.blit(font_large.render("FIM DE JOGO", True, COLOR_DANGER), font_large.render("FIM DE JOGO", True, COLOR_DANGER).get_rect(centerx=500, y=80))
        screen.blit(font.render(f"O vencedor é o Jogador {winner.id} com {winner.score} pontos!", True, COLOR_SUCCESS), font.render(f"O vencedor é o Jogador {winner.id} com {winner.score} pontos!", True, COLOR_SUCCESS).get_rect(centerx=500, y=180))
        screen.blit(font.render("Placar Final:", True, COLOR_PRIMARY), font.render("Placar Final:", True, COLOR_PRIMARY).get_rect(centerx=500, y=250))
        y_offset = 300
        for p in sorted(players, key=lambda p: p.score, reverse=True):
            score_text = f"Jogador {p.id}: {p.score} pontos"
            screen.blit(font.render(score_text, True, COLOR_SECONDARY), font.render(score_text, True, COLOR_SECONDARY).get_rect(centerx=500, y=y_offset)); y_offset += 40
        quit_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and quit_button.is_clicked(mouse_pos): pygame.quit(), sys.exit()
        pygame.display.flip(); clock.tick(30)

# ====== MAIN GAME LOGIC ======
def main():
    intro_screen()
    num_players = choose_players_screen()
    players = [Player(i + 1) for i in range(num_players)]
    
    round_num = 1
    while round_num <= MAX_ROUNDS:
        # --- FASE 1: DRAFT DE MERCADO SEQUENCIAL ---
        question_deck = list(QUESTION_POOL)
        random.shuffle(question_deck)
        market_cards = [question_deck.pop() for _ in range(num_players * 2)]
        pick_order = (list(range(num_players)) * 2)
        for i, player_index in enumerate(pick_order):
            player = players[player_index]
            pick_number = (i // num_players) + 1
            chosen_card, market_cards = market_draft_screen(player, market_cards, pick_number)
            player.hand.append(chosen_card)

        # --- FASE 2: Escolha da Pergunta Principal e Resposta Secreta ---
        for p in players:
            choose_main_question_screen(p)
            answering_screen(p)

        # --- FASE 3: Interrogatório ---
        for i in range(num_players):
            current_player = players[i]
            target, guess = guessing_phase_screen(players, current_player, 1) # Mostra sempre "RODADA 1"
            correct = (guess == target.secret_answer)
            if correct:
                current_player.score += 1
                target.score -= 1
            show_result_screen(current_player, target, correct)
            
        round_num += 1
        for p in players:
            p.hand = []

    end_game_screen(players)

if __name__ == "__main__":
    main()