import subprocess
import sys
import re
import argparse
from urllib.parse import urlsplit
import socket

def get_ip_from_url(url):
    try:
        domain = urlsplit(url).netloc or urlsplit(url).path
        return socket.gethostbyname(domain)
    except:
        print("URL invalide")
        sys.exit(1)

def extract_ip(line):
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, line)
    return ips[0] if ips else None

def traceroute(target, progressive=False, output_file=None):
    try:
        cmd = "traceroute" if sys.platform != "win32" else "tracert"
        subprocess.run(["which", cmd], check=True, capture_output=True)
        
        output_ips = []
        process = subprocess.Popen([cmd, target], 
                                stdout=subprocess.PIPE, 
                                text=True)
        
        for line in process.stdout:
            ip = extract_ip(line)
            if ip:
                output_ips.append(ip + '\n')
                if progressive:
                    print(ip)
                    
        if not progressive:  # Affichage non progressif
            for ip in output_ips:
                print(ip.strip())
                
        if output_file:  # Sauvegarde dans un fichier
            with open(output_file, 'w') as f:
                f.writelines(output_ips)
                
    except subprocess.CalledProcessError:
        print(f"Erreur: {cmd} n'est pas installé")
        print(f"Installez-le avec: sudo apt install traceroute")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Traceroute avec IPs")
    parser.add_argument("target", help="IP ou URL cible")
    parser.add_argument("-p", "--progressive", action="store_true", 
                       help="Affichage progressif")
    parser.add_argument("-o", "--output-file", help="Fichier de sortie")
    parser.add_argument("--url", action="store_true", 
                       help="La cible est une URL")
    
    args = parser.parse_args()
    
    # Conversion URL -> IP si nécessaire
    target = get_ip_from_url(args.target) if args.url else args.target
    
    traceroute(target, args.progressive, args.output_file)

if __name__ == "__main__":
    main()
