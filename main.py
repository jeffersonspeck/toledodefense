"""
=====================================================================
  TOLEDO DEV DEFENSE
  Linguagem de Programacao Aplicada - UNINTER
  -------------------------------------------------------------------
  Enredo: Um programador do interior de Toledo (PR) precisa digitar o
  nome dos erros (bugs) que invadem a cidade. Ao digitar o nome do erro
  e apertar ENTER, um raio sai do notebook e voa direto ate o bug certo.
=====================================================================
"""
import pygame
import os
import sys
import random
import math

if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

IMG = os.path.join(BASE, "imagens")
SND = os.path.join(BASE, "sons")

LARGURA, ALTURA = 800, 600
FPS = 60
CHAO_Y = 560
# faixa estreita da rua onde o programador anda (com pouco espaco vertical)
PROG_ALT = 88
Y_RUA_MAX = CHAO_Y - PROG_ALT      # pes do programador na beira da rua
Y_RUA_MIN = Y_RUA_MAX - 70         # pouco espaco para subir/descer

BRANCO = (255, 255, 255)
PRETO = (15, 15, 25)
AZUL = (40, 80, 160)
AMARELO = (250, 200, 40)
VERDE = (60, 200, 90)
VERMELHO = (220, 60, 60)
CINZA = (90, 90, 110)
CIANO = (120, 220, 255)

pygame.init()
try:
    pygame.mixer.init()
    SOM_OK = True
except Exception:
    SOM_OK = False

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Toledo Dev Defense - UNINTER")
relogio = pygame.time.Clock()

fonte_g = pygame.font.SysFont("consolas", 48, bold=True)
fonte_m = pygame.font.SysFont("consolas", 28, bold=True)
fonte_p = pygame.font.SysFont("consolas", 20)
fonte_pp = pygame.font.SysFont("consolas", 16)


def carregar_img(nome, escala=None):
    img = pygame.image.load(os.path.join(IMG, nome)).convert_alpha()
    if escala:
        img = pygame.transform.scale(img, escala)
    return img


def carregar_som(nome):
    if not SOM_OK:
        return None
    try:
        return pygame.mixer.Sound(os.path.join(SND, nome))
    except Exception:
        return None


img_fundo = carregar_img("fundo.png", (LARGURA, ALTURA))
img_chao = carregar_img("chao.png", (LARGURA, 40))
img_prog = carregar_img("programador.png", (70, 88))
img_raio = carregar_img("raio.png", (48, 16))
img_chefes = [carregar_img("chefe%d.png" % i, (90, 90)) for i in range(1, 7)]

som_tiro = carregar_som("tiro.wav")
som_hit = carregar_som("hit.wav")
som_dano = carregar_som("dano.wav")
som_vitoria = carregar_som("vitoria.wav")
som_derrota = carregar_som("derrota.wav")

if SOM_OK:
    try:
        pygame.mixer.music.load(os.path.join(SND, "musica.wav"))
        pygame.mixer.music.set_volume(0.4)
    except Exception:
        pass

ERROS = [
    "SyntaxError", "IndentationError", "NameError", "TypeError",
    "ValueError", "KeyError", "IndexError", "AttributeError",
    "ImportError", "ZeroDivisionError", "RuntimeError", "FileNotFoundError",
]


class Jogador:
    def __init__(self):
        self.x = 60
        self.y = Y_RUA_MAX
        self.vida = 100
        self.vel = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.vel
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.vel
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.vel
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.vel
        # anda na faixa da rua, com pouco espaco para subir/descer
        self.x = max(10, min(LARGURA - 80, self.x))
        self.y = max(Y_RUA_MIN, min(Y_RUA_MAX, self.y))

    def desenhar(self):
        tela.blit(img_prog, (self.x, self.y))

    @property
    def centro(self):
        return (self.x + 60, self.y + 35)

    @property
    def rect(self):
        return pygame.Rect(self.x + 8, self.y + 8, 54, 78)


class Raio:
    def __init__(self, x, y, alvo):
        self.x = float(x)
        self.y = float(y)
        self.vel = 14
        self.alvo = alvo
        self.ang = 0

    def atualizar(self):
        if self.alvo and self.alvo.vivo:
            ax, ay = self.alvo.centro
            dx, dy = ax - self.x, ay - self.y
            dist = math.hypot(dx, dy) or 1
            self.x += self.vel * dx / dist
            self.y += self.vel * dy / dist
            self.ang = math.degrees(math.atan2(-dy, dx))
        else:
            self.x += self.vel

    def desenhar(self):
        img = pygame.transform.rotate(img_raio, self.ang)
        r = img.get_rect(center=(int(self.x), int(self.y)))
        tela.blit(img, r)

    @property
    def rect(self):
        return pygame.Rect(self.x - 20, self.y - 8, 40, 16)

    def fora(self):
        return (self.x < -50 or self.x > LARGURA + 50 or
                self.y < -50 or self.y > ALTURA + 50)


class Chefe:
    def __init__(self, nome):
        self.nome = nome
        self.img = random.choice(img_chefes)
        self.x = random.randint(LARGURA // 2, LARGURA - 130)
        self.y = random.randint(70, CHAO_Y - 130)
        self.vx = random.choice([-1, 1]) * random.uniform(1.0, 2.2)
        self.vy = random.choice([-1, 1]) * random.uniform(0.8, 1.8)
        self.vida_max = 3
        self.vida = self.vida_max
        self.vivo = True
        self.dano_timer = 0

    def atualizar(self, jogador):
        if random.random() < 0.02:
            self.vx += random.uniform(-0.6, 0.6)
            self.vy += random.uniform(-0.6, 0.6)
        self.vx = max(-2.5, min(2.5, self.vx))
        self.vy = max(-2.5, min(2.5, self.vy))
        self.x += self.vx
        self.y += self.vy
        # area que os bugs ocupam: descem ate a altura do jogador para alcanca-lo
        if self.x < 20 or self.x > LARGURA - 110:
            self.vx *= -1
            self.x = max(20, min(LARGURA - 110, self.x))
        if self.y < 60 or self.y > CHAO_Y - 90:
            self.vy *= -1
            self.y = max(60, min(CHAO_Y - 90, self.y))
        # dano por toque/colisao com o jogador
        if self.rect.colliderect(jogador.rect):
            self.dano_timer += 1
            if self.dano_timer >= 30:
                self.dano_timer = 0
                jogador.vida -= 6
                if som_dano:
                    som_dano.play()
        else:
            self.dano_timer = 0

    def desenhar(self):
        tela.blit(self.img, (self.x, self.y))
        w = 90
        pygame.draw.rect(tela, PRETO, (self.x, self.y - 12, w, 6))
        pygame.draw.rect(tela, VERDE,
                         (self.x, self.y - 12, int(w * self.vida / self.vida_max), 6))

    @property
    def centro(self):
        return (self.x + 45, self.y + 45)

    @property
    def rect(self):
        return pygame.Rect(self.x + 8, self.y + 12, 74, 74)


def desenhar_texto(txt, fonte, cor, x, y, centro=False):
    surf = fonte.render(txt, True, cor)
    r = surf.get_rect()
    if centro:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    tela.blit(surf, r)


def tela_menu():
    if SOM_OK:
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass
    while True:
        tela.blit(img_fundo, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 120))
        tela.blit(overlay, (0, 0))

        desenhar_texto("TOLEDO DEV DEFENSE", fonte_g, AMARELO, LARGURA // 2, 95, True)
        desenhar_texto("O programador de Toledo-PR contra os bugs do Python",
                       fonte_p, BRANCO, LARGURA // 2, 145, True)

        cx, cy, cw, ch = 110, 195, 580, 270
        box = pygame.Surface((cw, ch), pygame.SRCALPHA)
        box.fill((10, 10, 30, 205))
        tela.blit(box, (cx, cy))
        pygame.draw.rect(tela, AMARELO, (cx, cy, cw, ch), 2)

        desenhar_texto("COMANDOS DE CONTROLE", fonte_m, AMARELO, LARGURA // 2, cy + 26, True)
        controles = [
            "DIGITE o nome do erro (bug) + ENTER  -  Dispara o RAIO no bug",
            "Exemplo: digite  SyntaxError  e tecle ENTER",
            "",
            "W / A / S / D  ou  SETAS   -  Mover o programador",
            "BACKSPACE                  -  Apagar letra digitada",
            "ESC                        -  Sair do jogo",
        ]
        for i, c in enumerate(controles):
            cor = CIANO if c.startswith("Exemplo") else BRANCO
            desenhar_texto(c, fonte_pp, cor, cx + 25, cy + 60 + i * 28)

        desenhar_texto("Pressione  [ENTER]  para JOGAR",
                       fonte_m, VERDE, LARGURA // 2, 500, True)
        desenhar_texto("Catedral Cristo Rei | Lago | Agro  -  UNINTER LPA",
                       fonte_pp, AMARELO, LARGURA // 2, 555, True)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return True
                if e.key == pygame.K_ESCAPE:
                    return False
        pygame.display.flip()
        relogio.tick(FPS)


def tela_fim(venceu):
    if SOM_OK:
        pygame.mixer.music.stop()
        s = som_vitoria if venceu else som_derrota
        if s:
            s.play()
    t0 = pygame.time.get_ticks()
    while True:
        tela.blit(img_fundo, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 160))
        tela.blit(overlay, (0, 0))
        if venceu:
            desenhar_texto("VITORIA!", fonte_g, VERDE, LARGURA // 2, 200, True)
            desenhar_texto("Toledo esta livre de bugs! Build limpo.",
                           fonte_p, BRANCO, LARGURA // 2, 270, True)
        else:
            desenhar_texto("GAME OVER", fonte_g, VERMELHO, LARGURA // 2, 200, True)
            desenhar_texto("Os bugs derrubaram o sistema...",
                           fonte_p, BRANCO, LARGURA // 2, 270, True)
        desenhar_texto("[ENTER] Jogar novamente    [ESC] Sair",
                       fonte_m, AMARELO, LARGURA // 2, 380, True)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN and pygame.time.get_ticks() - t0 > 400:
                if e.key == pygame.K_RETURN:
                    return True
                if e.key == pygame.K_ESCAPE:
                    return False
        pygame.display.flip()
        relogio.tick(FPS)


def jogar():
    if SOM_OK:
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    jogador = Jogador()
    raios = []
    chefes = []
    digitado = ""
    aviso = ""
    aviso_timer = 0

    TOTAL = 12
    derrotados = 0
    spawn_timer = 0
    spawn_delay = 90
    MAX_TELA = 6

    while True:
        relogio.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                elif e.key == pygame.K_BACKSPACE:
                    digitado = digitado[:-1]
                elif e.key == pygame.K_RETURN:
                    if digitado:
                        alvo = None
                        for c in chefes:
                            if c.vivo and c.nome.lower() == digitado.lower():
                                alvo = c
                                break
                        if alvo:
                            raios.append(Raio(jogador.centro[0], jogador.centro[1], alvo))
                            if som_tiro:
                                som_tiro.play()
                        else:
                            aviso = "Nenhum bug '" + digitado + "' na tela!"
                            aviso_timer = 90
                        digitado = ""
                else:
                    ch = e.unicode
                    if ch.isalnum():
                        digitado += ch

        teclas = pygame.key.get_pressed()
        jogador.mover(teclas)

        spawn_timer += 1
        if (spawn_timer >= spawn_delay and len(chefes) < MAX_TELA
                and (derrotados + len(chefes)) < TOTAL):
            chefes.append(Chefe(random.choice(ERROS)))
            spawn_timer = 0
            spawn_delay = max(45, spawn_delay - 2)

        for r in raios[:]:
            r.atualizar()
            acertou = False
            if r.alvo and r.alvo.vivo and r.rect.colliderect(r.alvo.rect):
                r.alvo.vida -= 3
                acertou = True
                if som_hit:
                    som_hit.play()
                if r.alvo.vida <= 0:
                    r.alvo.vivo = False
            if acertou or r.fora() or (r.alvo and not r.alvo.vivo):
                if r in raios:
                    raios.remove(r)

        for c in chefes[:]:
            if not c.vivo:
                chefes.remove(c)
                derrotados += 1
                continue
            c.atualizar(jogador)

        if jogador.vida <= 0:
            return tela_fim(False)
        if derrotados >= TOTAL:
            return tela_fim(True)

        if aviso_timer > 0:
            aviso_timer -= 1
        else:
            aviso = ""

        tela.blit(img_fundo, (0, 0))
        tela.blit(img_chao, (0, CHAO_Y))
        jogador.desenhar()
        for r in raios:
            r.desenhar()
        for c in chefes:
            c.desenhar()
            destaque = digitado and c.nome.lower().startswith(digitado.lower())
            cor = AMARELO if destaque else BRANCO
            desenhar_texto(c.nome, fonte_pp, cor, c.centro[0], c.y - 24, True)

        pygame.draw.rect(tela, PRETO, (10, 10, 204, 24))
        pygame.draw.rect(tela, VERMELHO, (12, 12, 200, 20))
        pygame.draw.rect(tela, VERDE, (12, 12, int(200 * max(jogador.vida, 0) / 100), 20))
        desenhar_texto("VIDA", fonte_pp, BRANCO, 220, 12)
        desenhar_texto("Bugs eliminados: %d/%d" % (derrotados, TOTAL),
                       fonte_p, AMARELO, LARGURA - 290, 12)

        if aviso:
            desenhar_texto(aviso, fonte_p, VERMELHO, LARGURA // 2, 50, True)

        pygame.draw.rect(tela, (10, 10, 25), (10, ALTURA - 40, LARGURA - 20, 32))
        pygame.draw.rect(tela, VERDE, (10, ALTURA - 40, LARGURA - 20, 32), 1)
        desenhar_texto(">>> " + digitado + "_", fonte_p, VERDE, 20, ALTURA - 35)

        pygame.display.flip()


def main():
    if not tela_menu():
        pygame.quit()
        sys.exit()
    while True:
        if not jogar():
            break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
