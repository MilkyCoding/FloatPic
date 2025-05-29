@echo off
chcp 65001 > nul
title FloatPic

:: Проверка наличия Python
python --version > nul 2>&1
if errorlevel 1 (
    echo Python не установлен! Пожалуйста, установите Python 3.7 или выше.
    echo Скачать можно здесь: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Проверка наличия виртуального окружения
if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Установка зависимостей...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Запуск приложения
echo Запуск FloatPic...
python src/floatpic.py

:: Деактивация виртуального окружения при выходе
call venv\Scripts\deactivate.bat 