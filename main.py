"""
=====================================================================
  TOLEDO DEV DEFENSE
  Linguagem de Programacao Aplicada - UNINTER
  -------------------------------------------------------------------
  Enredo: Um programador do interior de Toledo (PR) precisa digitar
  comandos no seu notebook para disparar raios e eliminar os chefoes
  (bugs gigantes) que invadem a cidade.
=====================================================================
"""
import pygame
import os
import sys
import random

# ------------------------------------------------------------------
# Caminho base (funciona tanto rodando o .py quanto o .exe do PyInstaller)
# ------------------------------------------------------------------
if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

IMG = os.path.join(BASE, "imagens")
SND = os.path.join(BASE, "sons")

LARGURA, ALTURA = 800, 600
FPS = 60
CHAO_Y = 560

# Cores
BRANCO = (255, 255, 255)
PRETO = (15, 15, 25)
AZUL = (40, 80, 160)
AMARELO = (250, 200, 40)
VERDE = (60, 200, 90)
VERMELHO = (220, 60, 60)
CINZA = (90, 90, 110)

# ------------------------------------------------------------------
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


# ------------------------------------------------------------------
def carregar_img(nome, escala=None):
    caminho = os.path.join(IMG, nome)
    img = pygame.image.load(caminho).convert_alpha()
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


# Assets
img_fundo = carregar_img("fundo.png", (LARGURA, ALTURA))
img_chao = carregar_img("chao.png", (LARGURA, 40))
img_prog = carregar_img("programador.png", (70, 88))
img_raio = carregar_img("raio.png", (48, 16))
img_chefes = [
    carregar_img("chefe1.png", (100, 100)),
    carregar_img("chefe2.png", (100, 100)),
    carregar_img("chefe3.png", (110, 110)),
]

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

# Palavras (comandos) que o jogador deve digitar para atirar
COMANDOS = ["run", "print", "debug", "import", "build", "deploy",
            "loop", "class", "async", "lambda", "commit", "merge",
            "python", "uninter", "toledo", "pygame", "compile", "input"]


# ==================================================================
class Jogador:
    def __init__(self):
        self.x = 60
        self.y = CHAO_Y - 88
        self.vida = 100
        self.vel = 6

    def mover(self, teclas):
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.vel
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.vel
        self.y = max(60, min(CHAO_Y - 88, self.y))

    def desenhar(self):
        tela.blit(img_prog, (self.x, self.y))

    @property
    def centro(self):
        return (self.x + 70, self.y + 30)


class Raio:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 12

    def atualizar(self):
        self.x += self.vel

    def desenhar(self):
        tela.blit(img_raio, (self.x, self.y))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 48, 16)


class Chefe:
    def __init__(self, nivel):
        self.img = img_chefes[min(nivel, len(img_chefes) - 1)]
        self.x = LARGURA + 40
        self.y = random.randint(80, CHAO_Y - 130)
        self.vel = 1.0 + nivel * 0.6
        self.vida_max = 3 + nivel * 2
        self.vida = self.vida_max
        self.dir_y = random.choice([-1, 1])

    def atualizar(self):
        self.x -= self.vel
        self.y += self.dir_y * 1.5
        if self.y < 60 or self.y > CHAO_Y - 110:
            self.dir_y *= -1

    def desenhar(self):
        tela.blit(self.img, (self.x, self.y))
        # barra de vida
        w = 100
        pygame.draw.rect(tela, PRETO, (self.x, self.y - 12, w, 6))
        pygame.draw.rect(tela, VERDE,
                         (self.x, self.y - 12, int(w * self.vida / self.vida_max), 6))

    @property
    def rect(self):
        return pygame.Rect(self.x + 10, self.y + 15, 80, 80)


# ==================================================================
def desenhar_texto(txt, fonte, cor, x, y, centro=False):
    surf = fonte.render(txt, True, cor)
    r = surf.get_rect()
    if centro:
        r.center = (x, y)
    else:
        r.topleft = (x, y)
    tela.blit(surf, r)


# ==================================================================
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

        desenhar_texto("TOLEDO DEV DEFENSE", fonte_g, AMARELO, LARGURA // 2, 110, True)
        desenhar_texto("Um programador do interior contra os bugs gigantes",
                       fonte_p, BRANCO, LARGURA // 2, 160, True)

        # caixa de comandos de controle
        cx, cy, cw, ch = 130, 230, 540, 230
        box = pygame.Surface((cw, ch), pygame.SRCALPHA)
        box.fill((10, 10, 30, 200))
        tela.blit(box, (cx, cy))
        pygame.draw.rect(tela, AMARELO, (cx, cy, cw, ch), 2)

        desenhar_texto("COMANDOS DE CONTROLE", fonte_m, AMARELO, LARGURA // 2, cy + 28, True)
        controles = [
            "DIGITAR a palavra do bug + ENTER  -  Disparar o RAIO",
            "W / SETA CIMA   -  Subir o programador",
            "S / SETA BAIXO  -  Descer o programador",
            "BACKSPACE       -  Apagar letra digitada",
            "ESC             -  Sair do jogo",
        ]
        for i, c in enumerate(controles):
            desenhar_texto(c, fonte_pp, BRANCO, cx + 25, cy + 65 + i * 30)

        desenhar_texto("Pressione  [ENTER]  para JOGAR",
                       fonte_m, VERDE, LARGURA // 2, 500, True)
        desenhar_texto("Cenario: Toledo - PR   |   UNINTER - LPA",
                       fonte_pp, CINZA, LARGURA // 2, 560, True)

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


# ==================================================================
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
            desenhar_texto("Toledo esta livre dos bugs! Deploy concluido.",
                           fonte_p, BRANCO, LARGURA // 2, 270, True)
        else:
            desenhar_texto("GAME OVER", fonte_g, VERMELHO, LARGURA // 2, 200, True)
            desenhar_texto("Os bugs derrubaram o servidor...",
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


# ==================================================================
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

    TOTAL_CHEFES = 8       # condicao de vitoria: derrotar 8 chefoes
    derrotados = 0
    spawn_timer = 0
    spawn_delay = 110

    rodando = True
    while rodando:
        relogio.tick(FPS)

        # ---- eventos ----
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                elif e.key == pygame.K_BACKSPACE:
                    digitado = digitado[:-1]
                elif e.key == pygame.K_RETURN:
                    # tenta disparar: procura chefe cuja palavra bate
                    alvo = None
                    for c in chefes:
                        if getattr(c, "palavra", "") == digitado.lower() and digitado:
                            alvo = c
                            break
                    if alvo or digitado:
                        raios.append(Raio(*jogador.centro))
                        if som_tiro:
                            som_tiro.play()
                        # guarda a palavra-alvo no raio
                        raios[-1].alvo_palavra = digitado.lower()
                    digitado = ""
                else:
                    ch = e.unicode
                    if ch.isalnum():
                        digitado += ch

        teclas = pygame.key.get_pressed()
        jogador.mover(teclas)

        # ---- spawn de chefes ----
        spawn_timer += 1
        if spawn_timer >= spawn_delay and len(chefes) < 4 and (derrotados + len(chefes)) < TOTAL_CHEFES:
            nivel = random.randint(0, 2)
            c = Chefe(nivel)
            c.palavra = random.choice(COMANDOS)
            chefes.append(c)
            spawn_timer = 0
            spawn_delay = max(70, spawn_delay - 3)

        # ---- atualiza raios ----
        for r in raios[:]:
            r.atualizar()
            if r.x > LARGURA:
                raios.remove(r)

        # ---- atualiza chefes + colisoes ----
        for c in chefes[:]:
            c.atualizar()
            # raio acerta
            for r in raios[:]:
                if r.rect.colliderect(c.rect):
                    # raio so dano se a palavra digitada era a do chefe (ou dano simples)
                    if getattr(r, "alvo_palavra", "") == c.palavra:
                        c.vida -= 3
                    else:
                        c.vida -= 1
                    if r in raios:
                        raios.remove(r)
                    if som_hit:
                        som_hit.play()
                    if c.vida <= 0:
                        if c in chefes:
                            chefes.remove(c)
                        derrotados += 1
                    break
            # chefe alcanca o jogador (esquerda) -> dano
            if c.x < 20:
                if c in chefes:
                    chefes.remove(c)
                jogador.vida -= 20
                if som_dano:
                    som_dano.play()

        # ---- condicoes de fim ----
        if jogador.vida <= 0:
            return tela_fim(False)
        if derrotados >= TOTAL_CHEFES:
            return tela_fim(True)

        # ---- desenho ----
        tela.blit(img_fundo, (0, 0))
        tela.blit(img_chao, (0, CHAO_Y))
        jogador.desenhar()
        for r in raios:
            r.desenhar()
        for c in chefes:
            c.desenhar()
            # palavra-comando acima do chefe
            destaque = digitado and c.palavra.startswith(digitado.lower())
            cor = AMARELO if destaque else BRANCO
            desenhar_texto(c.palavra, fonte_p, cor, c.x + 50, c.y - 30, True)

        # HUD
        pygame.draw.rect(tela, PRETO, (10, 10, 204, 24))
        pygame.draw.rect(tela, VERMELHO, (12, 12, 200, 20))
        pygame.draw.rect(tela, VERDE, (12, 12, int(200 * max(jogador.vida, 0) / 100), 20))
        desenhar_texto("VIDA", fonte_pp, BRANCO, 220, 12)
        desenhar_texto(f"Bugs eliminados: {derrotados}/{TOTAL_CHEFES}",
                       fonte_p, AMARELO, LARGURA - 280, 14)

        # caixa do "terminal" onde aparece o que esta sendo digitado
        pygame.draw.rect(tela, (10, 10, 25), (10, ALTURA - 40, LARGURA - 20, 32))
        pygame.draw.rect(tela, VERDE, (10, ALTURA - 40, LARGURA - 20, 32), 1)
        desenhar_texto(">>> " + digitado + "_", fonte_p, VERDE, 20, ALTURA - 35)

        pygame.display.flip()

    return False


# ==================================================================
def main():
    if not tela_menu():
        pygame.quit()
        sys.exit()
    while True:
        novamente = jogar()
        if not novamente:
            break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
