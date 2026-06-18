"""
Gerador de assets (imagens e sons) para o jogo "Toledo Dev Defense".
Cria os arquivos PNG na pasta /imagens e WAV na pasta /sons.
Executar uma unica vez para gerar os assets.
"""
import pygame
import numpy as np
import os
import math

pygame.init()
pygame.display.set_mode((1, 1))  # contexto de video p/ convert

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "imagens")
SND = os.path.join(BASE, "sons")
os.makedirs(IMG, exist_ok=True)
os.makedirs(SND, exist_ok=True)

# ------------------------------------------------------------------ IMAGENS

def salvar(surf, nome):
    pygame.image.save(surf, os.path.join(IMG, nome))
    print("imagem:", nome)


def criar_programador():
    """Programador do interior com notebook."""
    s = pygame.Surface((64, 80), pygame.SRCALPHA)
    # cabeca
    pygame.draw.circle(s, (240, 200, 160), (32, 18), 14)
    # cabelo
    pygame.draw.rect(s, (60, 40, 25), (18, 4, 28, 12), border_radius=6)
    # olhos
    pygame.draw.circle(s, (20, 20, 20), (27, 18), 2)
    pygame.draw.circle(s, (20, 20, 20), (37, 18), 2)
    # chapeu de palha (interior)
    pygame.draw.ellipse(s, (200, 170, 90), (10, 2, 44, 12))
    pygame.draw.ellipse(s, (170, 140, 60), (20, -2, 24, 10))
    # corpo / camisa xadrez
    pygame.draw.rect(s, (180, 60, 60), (16, 30, 32, 30), border_radius=4)
    for x in range(18, 48, 8):
        pygame.draw.line(s, (120, 30, 30), (x, 30), (x, 60), 1)
    for y in range(34, 60, 8):
        pygame.draw.line(s, (120, 30, 30), (16, y), (48, y), 1)
    # bracos
    pygame.draw.rect(s, (240, 200, 160), (8, 40, 8, 18), border_radius=3)
    pygame.draw.rect(s, (240, 200, 160), (48, 40, 8, 18), border_radius=3)
    # notebook
    pygame.draw.rect(s, (40, 40, 50), (14, 56, 36, 18), border_radius=2)
    pygame.draw.rect(s, (90, 200, 255), (18, 58, 28, 10))
    # pernas
    pygame.draw.rect(s, (40, 50, 90), (20, 70, 10, 10))
    pygame.draw.rect(s, (40, 50, 90), (34, 70, 10, 10))
    salvar(s, "programador.png")


def criar_chefe(cor, nome):
    s = pygame.Surface((90, 90), pygame.SRCALPHA)
    # corpo monstro / bug gigante
    pygame.draw.ellipse(s, cor, (10, 20, 70, 60))
    # detalhe escuro
    c2 = (max(cor[0]-50,0), max(cor[1]-50,0), max(cor[2]-50,0))
    pygame.draw.ellipse(s, c2, (22, 34, 46, 34))
    # chifres
    pygame.draw.polygon(s, c2, [(20, 22), (12, 4), (30, 18)])
    pygame.draw.polygon(s, c2, [(70, 22), (78, 4), (60, 18)])
    # olhos vermelhos
    pygame.draw.circle(s, (255, 40, 40), (34, 42), 7)
    pygame.draw.circle(s, (255, 40, 40), (56, 42), 7)
    pygame.draw.circle(s, (20, 0, 0), (34, 42), 3)
    pygame.draw.circle(s, (20, 0, 0), (56, 42), 3)
    # boca
    pygame.draw.arc(s, (10, 10, 10), (30, 52, 30, 20), math.pi, 2*math.pi, 3)
    # pernas
    for px in (20, 35, 55, 70):
        pygame.draw.line(s, c2, (px, 76), (px, 88), 4)
    salvar(s, nome)


def criar_raio():
    s = pygame.Surface((40, 12), pygame.SRCALPHA)
    pygame.draw.polygon(s, (120, 220, 255),
                        [(0, 6), (28, 1), (28, 4), (40, 6), (28, 8), (28, 11)])
    pygame.draw.polygon(s, (255, 255, 255),
                        [(4, 6), (26, 4), (38, 6), (26, 8)])
    salvar(s, "raio.png")


def criar_fundo():
    """Cenario de Toledo-PR: ceu, lago, catedral, silos e plantacoes."""
    w, h = 800, 600
    s = pygame.Surface((w, h))
    # ceu em degrade
    for y in range(h):
        t = y / h
        cor = (int(120 + 110*t), int(175 + 55*t), int(225 - 20*t))
        pygame.draw.line(s, cor, (0, y), (w, y))
    # sol
    pygame.draw.circle(s, (255, 240, 180), (690, 90), 42)

    base = 410  # linha do horizonte

    # ---- CATEDRAL CRISTO REI (esquerda) ----
    cx = 90
    pygame.draw.rect(s, (225, 220, 210), (cx, base - 70, 70, 70))
    pygame.draw.polygon(s, (170, 90, 70),
                        [(cx - 6, base - 70), (cx + 76, base - 70), (cx + 35, base - 95)])
    pygame.draw.rect(s, (235, 230, 220), (cx + 26, base - 130, 18, 60))
    pygame.draw.polygon(s, (120, 140, 170),
                        [(cx + 24, base - 130), (cx + 46, base - 130), (cx + 35, base - 165)])
    pygame.draw.line(s, (60, 60, 60), (cx + 35, base - 165), (cx + 35, base - 180), 2)
    pygame.draw.line(s, (60, 60, 60), (cx + 30, base - 175), (cx + 40, base - 175), 2)
    pygame.draw.rect(s, (120, 80, 50), (cx + 30, base - 24, 12, 24))
    pygame.draw.circle(s, (90, 140, 200), (cx + 36, base - 50), 7)

    # ---- SILOS DO AGRO (centro-direita) ----
    for i, sx in enumerate((470, 510, 548)):
        sh = 70 + (i % 2) * 14
        pygame.draw.rect(s, (200, 205, 210), (sx, base - sh, 30, sh))
        pygame.draw.ellipse(s, (170, 175, 185), (sx, base - sh - 10, 30, 20))
        for ry in range(base - sh + 8, base, 12):
            pygame.draw.line(s, (160, 165, 175), (sx, ry), (sx + 30, ry), 1)

    # ---- CASARIO simples do interior ----
    import random
    random.seed(11)
    for bx in (200, 250, 300, 350, 600, 650, 700, 745):
        bh = random.randint(35, 60)
        pygame.draw.rect(s, (180, 150, 130), (bx, base - bh, 42, bh))
        pygame.draw.polygon(s, (150, 70, 60),
                            [(bx - 4, base - bh), (bx + 46, base - bh), (bx + 21, base - bh - 16)])
        pygame.draw.rect(s, (110, 150, 200), (bx + 14, base - bh + 14, 12, 12))

    # ---- LAGO (Parque dos Lagos) ----
    lago_top = base
    pygame.draw.rect(s, (70, 130, 180), (0, lago_top, w, 40))
    for ly in range(lago_top + 6, lago_top + 40, 8):
        pygame.draw.line(s, (110, 170, 215), (0, ly), (w, ly), 1)

    # ---- CAMPO / PLANTACAO (agro) ----
    campo_top = base + 40
    pygame.draw.rect(s, (95, 165, 75), (0, campo_top, w, h - campo_top))
    for fx in range(-40, w, 36):
        pygame.draw.line(s, (75, 145, 60), (fx, campo_top), (fx + 60, h), 3)
    for ry in range(campo_top + 20, h, 26):
        pygame.draw.line(s, (70, 135, 55), (0, ry), (w, ry), 2)

    salvar(s, "fundo.png")


def criar_chao():
    s = pygame.Surface((800, 40))
    s.fill((110, 80, 50))
    pygame.draw.rect(s, (90, 160, 70), (0, 0, 800, 10))
    for x in range(0, 800, 20):
        pygame.draw.line(s, (80, 60, 40), (x, 12), (x, 40), 1)
    salvar(s, "chao.png")


criar_programador()
criar_chefe((150, 80, 200), "chefe1.png")
criar_chefe((200, 120, 60), "chefe2.png")
criar_chefe((80, 180, 120), "chefe3.png")
criar_chefe((200, 70, 90), "chefe4.png")
criar_chefe((70, 130, 200), "chefe5.png")
criar_chefe((210, 180, 60), "chefe6.png")
criar_raio()
criar_fundo()
criar_chao()

# ------------------------------------------------------------------ SONS
SR = 22050

def salvar_som(nome, samples):
    samples = np.clip(samples, -1, 1)
    audio = (samples * 32767).astype(np.int16)
    stereo = np.column_stack((audio, audio))
    snd = pygame.sndarray.make_sound(stereo.copy())
    # exportar como wav manualmente
    import wave
    path = os.path.join(SND, nome)
    with wave.open(path, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(stereo.astype(np.int16).tobytes())
    print("som:", nome)


def tom(freqs, dur, decay=5.0, vol=0.4):
    t = np.linspace(0, dur, int(SR * dur), False)
    wave_ = np.zeros_like(t)
    for f in freqs:
        wave_ += np.sin(2 * np.pi * f * t)
    wave_ /= len(freqs)
    env = np.exp(-decay * t)
    return wave_ * env * vol


# tiro: raio eletrico (frequencia descendente + ruido)
t = np.linspace(0, 0.18, int(SR*0.18), False)
freq = np.linspace(900, 200, t.size)
tiro = np.sin(2*np.pi*freq*t) + 0.3*np.random.uniform(-1, 1, t.size)
tiro *= np.exp(-8*t) * 0.4
salvar_som("tiro.wav", tiro)

# hit no chefe
salvar_som("hit.wav", tom([220, 277, 330], 0.25, decay=8, vol=0.5))

# dano no jogador
salvar_som("dano.wav", tom([150, 110], 0.4, decay=4, vol=0.5))

# vitoria
v = np.concatenate([tom([523], 0.15, 4, 0.4), tom([659], 0.15, 4, 0.4),
                    tom([784], 0.15, 4, 0.4), tom([1047], 0.4, 3, 0.4)])
salvar_som("vitoria.wav", v)

# derrota
d = np.concatenate([tom([392], 0.2, 4, 0.4), tom([311], 0.2, 4, 0.4),
                    tom([262], 0.5, 3, 0.4)])
salvar_som("derrota.wav", d)

# musica de fundo (loop simples)
notas = [262, 330, 392, 330, 294, 349, 440, 349]
musica = np.concatenate([tom([n, n*2], 0.35, decay=2.5, vol=0.18) for n in notas])
salvar_som("musica.wav", musica)

print("Assets gerados com sucesso!")
pygame.quit()
