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
    """Cenario de Toledo-PR: ceu, campo e silhueta de cidade."""
    w, h = 800, 600
    s = pygame.Surface((w, h))
    for y in range(h):
        t = y / h
        cor = (int(120 + 100*t), int(180 + 50*t), int(230 - 30*t))
        pygame.draw.line(s, cor, (0, y), (w, y))
    # sol
    pygame.draw.circle(s, (255, 240, 180), (660, 110), 45)
    # silhueta cidade (predios pequenos do interior)
    base = 430
    import random
    random.seed(7)
    x = 0
    while x < w:
        bw = random.randint(40, 80)
        bh = random.randint(40, 120)
        pygame.draw.rect(s, (90, 110, 130), (x, base - bh, bw, bh))
        for wy in range(base - bh + 8, base, 16):
            for wx in range(x + 6, x + bw - 6, 14):
                pygame.draw.rect(s, (200, 220, 120), (wx, wy, 6, 8))
        x += bw + 6
    # campo verde (agro de Toledo)
    pygame.draw.rect(s, (90, 160, 70), (0, base, w, h - base))
    for fx in range(0, w, 40):
        pygame.draw.line(s, (70, 140, 55), (fx, base), (fx + 20, h), 2)
    # silo/torre
    pygame.draw.rect(s, (200, 200, 200), (120, base - 60, 30, 60))
    pygame.draw.polygon(s, (180, 90, 60), [(115, base-60), (155, base-60), (135, base-85)])
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
