@echo off
REM ============================================================
REM   Build do Toledo Dev Defense para Windows (.exe)
REM   UNINTER - Linguagem de Programacao Aplicada
REM ============================================================

echo Instalando dependencias...
pip install pygame numpy pyinstaller

echo.
echo Compilando o jogo...
python -m PyInstaller --onefile --noconsole --name ToledoDevDefense main.py

echo.
echo Copiando assets para a pasta dist...
xcopy /E /I /Y imagens dist\imagens
xcopy /E /I /Y sons dist\sons

echo.
echo ============================================================
echo  BUILD CONCLUIDO!
echo  O executavel esta em: dist\ToledoDevDefense.exe
echo  As pastas imagens e sons ja foram copiadas para dist.
echo  Agora compacte a pasta 'dist' em um .ZIP para entregar.
echo ============================================================
pause
