# Toledo Dev Defense
### Trabalho de Linguagem de Programação Aplicada - UNINTER

Jogo 2D feito em **Python + Pygame**.

## Enredo
Um programador do interior de **Toledo (PR)** precisa **digitar comandos** no seu
notebook para disparar **raios** e eliminar os **chefões** (bugs gigantes) que
invadem a cidade.

## Como o jogo atende aos requisitos do trabalho
- **Jogo 2D** (não é via console/cmd). ✔
- **Controle do jogador**: mover (W/S) e digitar comandos para atirar. ✔
- **Desafio**: ondas de chefões que avançam pela tela. ✔
- **Condição de vitória**: eliminar 8 chefões. ✔
- **Condição de derrota**: a vida do programador chegar a zero. ✔
- **Menu** com os **comandos de controle** escritos na tela. ✔
- **Imagens e sons** incluídos (pasta `imagens` e `sons`). ✔

## Comandos de controle (também aparecem no menu)
- **Digitar a palavra do bug + ENTER** → dispara o raio
- **W / Seta Cima** → subir
- **S / Seta Baixo** → descer
- **BACKSPACE** → apagar letra
- **ESC** → sair

---

## Como executar (modo desenvolvimento)
```
pip install pygame numpy
python main.py
```

## Como gerar o .exe para Windows (entregar o ZIP exigido)
Na sua máquina **Windows**:

1. Instale o PyInstaller:
   ```
   pip install pyinstaller pygame
   ```
2. Rode o script de build incluso:
   ```
   build_windows.bat
   ```
   (ou manualmente: `pyinstaller --onefile --noconsole --name ToledoDevDefense main.py`)

3. Após compilar, copie as pastas **`imagens`** e **`sons`** para **dentro da
   pasta `dist`**, ao lado do `ToledoDevDefense.exe`, mantendo a mesma hierarquia.

   A estrutura final em `dist` deve ficar:
   ```
   dist/
     ToledoDevDefense.exe
     imagens/   (todos os .png)
     sons/      (todos os .wav)
   ```
4. Compacte a pasta `dist` em um **.ZIP** e entregue.

> Observação: os assets já estão prontos nas pastas `imagens` e `sons`.
> Se quiser regenerá-los, rode `python gerar_assets.py`.
