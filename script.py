#!/usr/bin/env python3
import os
import sys

# Função para verificar se o script está rodando como root
def verificar_root():
    if os.geteuid() != 0:
        print("[ERRO] Este script precisa ser executado com privilégios de superusuário (root ou sudo).")
        sys.exit(1)

def main():
    print("=== Iniciando Automação de Servidor Web (Fedora Linux) ===")
    verificar_root()

    # 1. Atualização do Sistema
    print("\n[1/5] Atualizando o sistema com o dnf...")
    retorno = os.system("dnf update -y")
    if retorno != 0:
        print("[ERRO] Falha ao atualizar o sistema.")
        sys.exit(1)

    # 2. Instalação de Dependências (Apache e Git)
    print("\n[2/5] Instalando Apache (httpd) e Git...")
    retorno = os.system("dnf install -y httpd git")
    if retorno != 0:
        print("[ERRO] Falha ao instalar as dependências.")
        sys.exit(1)

    # 3. Gerenciamento do Serviço (Iniciar e Habilitar)
    print("\n[3/5] Iniciando e habilitando o serviço do Apache (httpd)...")
    os.system("systemctl start httpd")
    os.system("systemctl enable httpd")

    # 4. Deploy da Aplicação
    print("\n[4/5] Realizando o deploy da aplicação...")
    
    # Clonando o repositório em um diretório temporário
    print("-> Clonando repositório do GitHub...")
    os.system("git clone https://github.com/denilsonbonatti/mundo-invertido.git /tmp/mundo-invertido")

    # Copiando os arquivos para a pasta padrão do Apache
    print("-> Copiando arquivos para /var/www/html/...")
    os.system("cp -R /tmp/mundo-invertido/* /var/www/html/")

    # Removendo os arquivos temporários clonados
    print("-> Limpando diretório temporário...")
    os.system("rm -rf /tmp/mundo-invertido")

    # 5. Ajuste de Permissões / SELinux (Bônus)
    print("\n[5/5] Ajustando permissões e contexto do SELinux...")
    # Ajusta o contexto de segurança SELinux para arquivos web do Apache
    os.system("restorecon -Rv /var/www/html/")

    print("\n=== Automação concluída com sucesso! ===")
    print("O servidor web está rodando e a aplicação 'Mundo Invertido' foi publicada.")

if __name__ == "__main__":
    main()