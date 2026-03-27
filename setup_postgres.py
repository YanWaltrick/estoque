#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guia rápido de instalação MySQL para Sistema de Estoque"""

print('Instalador MySQL - uso manual')
print('1) Baixe MySQL Community Server: https://dev.mysql.com/downloads/mysql/')
print('2) Instale e anote a senha do root.')
print('3) Crie banco e usuário:')
print('   mysql -u root -p')
print('   CREATE DATABASE IF NOT EXISTS estoque_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
print("   CREATE USER IF NOT EXISTS 'estoque_user'@'%' IDENTIFIED BY '12345';")
print('   GRANT ALL PRIVILEGES ON estoque_db.* TO "estoque_user"@"%";')
print('   FLUSH PRIVILEGES;')
print('   EXIT;')
print('4) Atualize .env para: mysql+pymysql://estoque_user:12345@localhost:3306/estoque_db')
print('5) Execute python app.py')
