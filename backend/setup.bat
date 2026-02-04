@echo off
REM Script setup cho backend trên Windows

echo === Cai dat Backend ===

REM Tao virtual environment
echo Tao virtual environment...
python -m venv venv

REM Kich hoat virtual environment
call venv\Scripts\activate.bat

REM Cai dat dependencies
echo Cai dat dependencies...
pip install -r requirements.txt

REM Tao file .env
if not exist ".env" (
    echo Tao file .env...
    copy .env.example .env
    echo Vui long chinh sua file .env voi thong tin cua ban
)

echo === Setup hoan tat ===
echo De bat dau, chay lenh:
echo   venv\Scripts\activate
echo   python manage.py migrate
echo   python manage.py runserver
pause
