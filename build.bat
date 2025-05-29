@echo off
echo Building FloatPic...

REM Переход в директорию скрипта
cd /d "%~dp0"

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

REM Проверка наличия директории src
if not exist "src" (
    echo Директория src не найдена!
    pause
    exit /b 1
)

REM Проверка наличия файла floatpic.py
if not exist "src\floatpic.py" (
    echo Файл src\floatpic.py не найден!
    pause
    exit /b 1
)

REM Установка зависимостей
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Очистка старых файлов сборки
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "FloatPic.spec" del /f /q "FloatPic.spec"

REM Сборка .exe
echo Building executable...
pyinstaller --noconfirm --onefile --windowed --name "FloatPic" "src\floatpic.py"

REM Проверка успешности сборки
if exist "dist\FloatPic.exe" (
    echo Build completed successfully!
    echo Executable location: dist\FloatPic.exe
) else (
    echo Build failed!
)

pause 