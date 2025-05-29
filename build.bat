@echo off
echo Building FloatPic...

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не установлен! Пожалуйста, установите Python 3.8 или выше.
    pause
    exit /b 1
)

REM Проверка наличия pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip не установлен! Пожалуйста, установите pip.
    pause
    exit /b 1
)

REM Установка зависимостей
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Создание директории для сборки
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM Сборка .exe
echo Building executable...
pyinstaller --noconfirm --onefile --windowed --icon "assets/icon.ico" --add-data "src;src/" --name "FloatPic" "src/floatpic.py"

REM Проверка успешности сборки
if exist "dist\FloatPic.exe" (
    echo Build completed successfully!
    echo Executable location: dist\FloatPic.exe
) else (
    echo Build failed!
)

pause 