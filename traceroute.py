import subprocess
import platform
import socket
from urllib.parse import urlsplit

def execute_traceroute(destination, save_output=None):
    """
    Exécute une commande traceroute/tracert selon l'OS.
    Args:
        destination: IP ou domaine cible
        save_output: Fichier de sortie optionnel
    """
    cmd = ["tracert" if platform.system().lower() == "windows" else "traceroute", destination]
    
    try:
        result = subprocess.run(cmd, text=True, capture_output=True)
        output = result.stdout
        
        print(output)
        if save_output:
            with open(save_output, "w") as f:
                f.write(output)
                
    except Exception as e:
        print(f"Erreur: {e}")
        exit(1)

def get_ip(target, is_url=False):
    """
    Valide/résout l'adresse cible.
    Retourne l'IP si valide, sinon None.
    """
    try:
        if is_url:
            domain = urlsplit(target).netloc or urlsplit(target).path
            return socket.gethostbyname(domain)
        return target if subprocess.run(["ping", target], capture_output=True).returncode == 0 else None
    except:
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Traceroute helper")
    parser.add_argument("target", help="Adresse IP ou URL cible")
    parser.add_argument("-o", "--output", help="Fichier de sortie")
    parser.add_argument("--url", action="store_true", help="La cible est une URL")
    
    args = parser.parse_args()
    
    ip = get_ip(args.target, args.url)
    if not ip:
        print("Adresse invalide")
        exit(1)
        
    print(f"Traceroute vers {ip}")
    execute_traceroute(ip, args.output)
