@echo off
REM Instalador MySQL - Sistema Estoque

echo.
echo ======================================
echo Instalador MySQL (manual)
echo ======================================
echo.
echo Este script nao instalará automaticamente.
echo Siga as instrucoes abaixo:
   echo 1) Baixe e instale MySQL Community Server:
      echo    https://dev.mysql.com/downloads/mysql/
      echo 2) Durante a instalacao, anote a senha do usuario root.
      echo 3) Certifique-se de que sqlcmd esta no PATH.
      echo 4) Crie banco e usuario:
         echo    mysql -u root -p
         echo    CREATE DATABASE IF NOT EXISTS estoque_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
         echo    CREATE USER IF NOT EXISTS 'estoque_user'@'%' IDENTIFIED BY '12345';
         echo    GRANT ALL PRIVILEGES ON estoque_db.* TO 'estoque_user'@'%';
         echo    FLUSH PRIVILEGES;
         echo    EXIT;
         echo.
         echo 5) Atualize .env com DATABASE_URL=mysql+pymysql://estoque_user:12345@localhost:3306/estoque_db
         echo.
         echo Pressione qualquer tecla para sair...
         pause >nul
         