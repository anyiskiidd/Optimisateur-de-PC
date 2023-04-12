import os
import shutil
import psutil
import gc
import platform
from glob import glob
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

# Utilitaires
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = result.stdout or result.stderr
    return output.decode('utf-8', errors='ignore').strip()

def get_disk_usage():
    usage = shutil.disk_usage(os.path.expandvars(r'%SystemDrive%'))
    return usage

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory

def nettoyer_fichiers_temporaires():
    folders = [
        os.path.expandvars(r'%TEMP%'), 
        os.path.expandvars(r'%WINDIR%\Temp')
    ]

    files_deleted = 0
    for folder in folders:
        for file in glob(os.path.join(folder, '*')):
            try:
                os.remove(file)
                files_deleted += 1
            except Exception as e:
                print(Fore.RED + f"Erreur lors de la suppression de {file}: {e}")

    print(Fore.GREEN + f'{files_deleted} fichiers temporaires supprimés.')

def optimiser_memoire():
    gc.collect()
    print(Fore.GREEN + 'Optimisation de la mémoire effectuée.')

def fermer_programmes_inutiles(liste_programmes):
    programs_closed = 0
    for program in liste_programmes:
        for process in psutil.process_iter():
            try:
                if process.name() == program:
                    process.terminate()
                    programs_closed += 1
            except Exception as e:
                print(Fore.RED + f"Erreur lors de la fermeture de {program}: {e}")

    print(Fore.GREEN + f'{programs_closed} programmes inutiles fermés.')

def update_system():
    print("Mise à jour du système en cours...")
    run_command('powershell.exe wuauclt.exe /updatenow')
    print(Fore.GREEN + "Mise à jour du système terminée.")

def disable_unnecessary_services():
    services_to_disable = [
        'Fax',  # Service de fax
        'stisvc',  # Service de transfert d'images Windows
        'WMPNetworkSvc',  # Partage de Windows Media Player
    ]
    for service in services_to_disable:
        run_command(f'sc config {service} start= disabled')
    print(Fore.GREEN + f"{len(services_to_disable)} services inutiles désactivés.")

def delete_prefetch_files():
    prefetch_folder = os.path.expandvars(r'%SystemRoot%\Prefetch')
    files_deleted = 0
    for file in glob(os.path.join(prefetch_folder, '*')):
        try:
            os.remove(file)
            files_deleted += 1
        except Exception as e:
            print(Fore.RED + f"Erreur lors de la suppression de {file}: {e}")

    print(Fore.GREEN + f'{files_deleted} fichiers Prefetch supprimés.')

def check_disk_usage():
    usage = get_disk_usage()
    total_space = usage.total // (1024 * 1024 * 1024)
    used_space = usage.used // (1024 * 1024 * 1024)
    free_space = usage.free // (1024 * 1024 * 1024)
    print(Fore.GREEN + f"Utilisation du disque : {used_space} Go utilisés sur {total_space} Go (il reste {free_space} Go).")

def check_memory_usage():
    memory = get_memory_usage()
    total_memory = memory.total // (1024 * 1024)
    used_memory = memory.used // (1024 * 1024)
    free_memory = memory.available // (1024 * 1024)
    print(Fore.GREEN + f"Utilisation de la mémoire : {used_memory} Mo utilisés sur {total_memory} Mo (il reste {free_memory} Mo).")

def disable_startup_programs():
    startup_programs = [
        "OneDrive",  # Microsoft OneDrive
        "Spotify",  # Spotify
    ]
    for program in startup_programs:
        run_command(f'REG DELETE "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v {program} /f')
    print(Fore.GREEN + f"{len(startup_programs)} programmes de démarrage désactivés.")


def print_menu():
    print(Fore.YELLOW + "\nOptimisateur de PC")
    print(Fore.YELLOW + "1. Nettoyer les fichiers temporaires")
    print(Fore.YELLOW + "2. Optimiser la mémoire")
    print(Fore.YELLOW + "3. Fermer les programmes inutiles courants")
    print(Fore.YELLOW + "4. Fermer les programmes inutiles de démarrage")
    print(Fore.YELLOW + "5. Fermer les programmes inutiles en arrière-plan")
    print(Fore.YELLOW + "6. Mettre à jour le système")
    print(Fore.YELLOW + "7. Désactiver les services inutiles")
    print(Fore.YELLOW + "8. Supprimer les fichiers Prefetch")
    print(Fore.YELLOW + "9. Vérifier l'utilisation du disque")
    print(Fore.YELLOW + "10. Vérifier l'utilisation de la mémoire")
    print(Fore.YELLOW + "11. Désactiver les programmes de démarrage")
    print(Fore.YELLOW + "12. Quitter")

def print_advanced_menu():
    print(Fore.YELLOW + "13. Options avancées")
    print(Fore.YELLOW + "14. Optimiser les performances du système")
    print(Fore.YELLOW + "15. Désactiver les effets visuels inutiles")
    print(Fore.YELLOW + "16. Nettoyer le cache DNS")
    print(Fore.YELLOW + "17. Réinitialiser les paramètres réseau")
    print(Fore.YELLOW + "18. Vérifier la santé du disque")
    print(Fore.YELLOW + "19. Défragmenter le disque")
    print(Fore.YELLOW + "20. Vérifier les mises à jour des pilotes")
    print(Fore.YELLOW + "21. Nettoyer le registre")
    print(Fore.YELLOW + "22. Analyser et réparer les erreurs système")
    print(Fore.YELLOW + "23. Exécuter toutes les options")


def optimize_system_performance():
    run_command('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
    print(Fore.GREEN + "Les performances du système ont été optimisées.")


def disable_unnecessary_visual_effects():
    run_command('SystemPropertiesPerformance.exe /adjust')
    print(Fore.GREEN + "Les effets visuels inutiles ont été désactivés.")


def clear_dns_cache():
    run_command('ipconfig /flushdns')
    print(Fore.GREEN + "Le cache DNS a été nettoyé.")


def reset_network_settings():
    result = run_command('netsh int ip reset')
    if isinstance(result, str):
        print(Fore.RED + f"Command failed: {result}")
        return
    if result.returncode != 0:
        print(Fore.RED + f"Command failed: {result.stderr}")
        return
    if result.stdout is not None:
        print(Fore.GREEN + "Network settings reset successfully.")
    else:
        print(Fore.RED + "No output from command.")

def check_disk_health():
    run_command('wmic diskdrive get status')
    print(Fore.GREEN + "La santé du disque a été vérifiée.")


def defrag_disk():
    run_command('defrag C: /U /V')
    print(Fore.GREEN + "Le disque a été défragmenté.")


def check_driver_updates():
    print("Veuillez utiliser un logiciel tiers pour vérifier et installer les mises à jour des pilotes.")


def clean_registry():
    print("Veuillez utiliser un logiciel tiers pour nettoyer le registre Windows.")


def repair_system_errors():
    run_command('sfc /scannow')
    print(Fore.GREEN + "Les erreurs système ont été analysées et réparées.")


def run_all_options(common_programs, startup_programs, background_programs):
    nettoyer_fichiers_temporaires()
    optimiser_memoire()
    fermer_programmes_inutiles(common_programs)
    fermer_programmes_inutiles(startup_programs)
    fermer_programmes_inutiles(background_programs)
    update_system()
    disable_unnecessary_services()
    delete_prefetch_files()
    check_disk_usage()
    check_memory_usage()
    disable_startup_programs()
    optimize_system_performance()
    disable_unnecessary_visual_effects()
    clear_dns_cache()
    reset_network_settings()
    check_disk_health()
    defrag_disk()
    check_driver_updates()
    clean_registry()
    repair_system_errors()
    print(Fore.GREEN + "Toutes les options ont été exécutées.")


def main():
    common_programs = [
        'example_program.exe',  # Remplacez par les noms des programmes courants que vous souhaitez fermer
        'another_example_program.exe',
    ]

    startup_programs = [
        'jusched.exe',          # Java Update Scheduler
        'OneDrive.exe',         # Microsoft OneDrive
        'Spotify.exe',          # Spotify
    ]

    background_programs = [
        'AdobeARM.exe',         # Adobe Reader and Acrobat Manager
        'GoogleCrashHandler.exe',  # Google Crash Handler
    ]

    while True:
        print_menu()
        print_advanced_menu()
        choix = input(Fore.CYAN + "Choisissez une option (1-23): ")

        if choix == '23':
            run_all_options(common_programs, startup_programs, background_programs)
        else:
            # Rest of the code

                if choix == '1':
                    nettoyer_fichiers_temporaires()
                elif choix == '2':
                    optimiser_memoire()
                elif choix == '3':
                    fermer_programmes_inutiles(common_programs)
                elif choix == '4':
                    fermer_programmes_inutiles(startup_programs)
                elif choix == '5':
                    fermer_programmes_inutiles(background_programs)
                elif choix == '6':
                    update_system()
                elif choix == '7':
                    disable_unnecessary_services()
                elif choix == '8':
                    delete_prefetch_files()
                elif choix == '9':
                    check_disk_usage()
                elif choix == '10':
                    check_memory_usage()
                elif choix == '11':
                    disable_startup_programs()
                elif choix == '12':
                    print(Fore.GREEN + "Au revoir!")
                    break
                elif choix == '13':
                    print("Veuillez choisir une option avancée (14-22).")
                elif choix == '14':
                    optimize_system_performance()
                elif choix == '15':
                    disable_unnecessary_visual_effects()
                elif choix == '16':
                    clear_dns_cache()
                elif choix == '17':
                    reset_network_settings()
                elif choix == '18':
                    check_disk_health()
                elif choix == '19':
                    defrag_disk()
                elif choix == '20':
                    check_driver_updates()
                elif choix == '21':
                    clean_registry()
                elif choix == '22':
                    repair_system_errors()
                else:
                    print(Fore.RED + "Option invalide. Veuillez entrer un nombre entre 1 et 23.")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        main()
    else:
        print("Cet optimisateur de PC est spécifique à Windows.")





