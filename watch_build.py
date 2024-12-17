import os
import sys
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Répertoire des fichiers à traiter
KEYMAPS_DIR = Path("keymaps")
DIST_DIR = Path("dist")

# Commande Kalamine
KALAMINE_COMMAND = "kalamine"


# Fonction pour construire un fichier
def build_file(file_path):
    try:
        output_file = file_path.with_suffix(".json")
        subprocess.run(
            [KALAMINE_COMMAND, "build", str(file_path), "--out", str(output_file)],
            check=True,
        )
        print(f"Built: {file_path} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error building {file_path}: {e}")


# Fonction pour traiter tous les fichiers
def build_all():
    for file_path in KEYMAPS_DIR.rglob("*.toml"):
        build_file(file_path)
    for file_path in KEYMAPS_DIR.rglob("*.yaml"):
        build_file(file_path)


# Classe pour surveiller les modifications
class WatchHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".toml", ".yaml")):
            build_file(Path(event.src_path))


def watch_files():
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, str(KEYMAPS_DIR), recursive=True)
    observer.start()
    print(f"Watching for changes in {KEYMAPS_DIR}... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Installation
def install():
    print("Installing keymap...")
    subprocess.run(
        [KALAMINE_COMMAND, "install", str(KEYMAPS_DIR / "ergol.toml")], check=True
    )


# Désinstallation
def uninstall():
    print("Uninstalling keymap...")
    subprocess.run([KALAMINE_COMMAND, "remove", "fr/ergol"], check=True)


# Nettoyage des fichiers générés
def clean():
    if DIST_DIR.exists():
        for file in DIST_DIR.iterdir():
            try:
                file.unlink()
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
    else:
        print("No files to clean.")


# Commande principale
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py [all|watch|dev|clean|install|uninstall]")
        return

    command = sys.argv[1]
    if command == "build":
        build_all()
    elif command == "watch":
        watch_files()
    elif command == "dev":
        subprocess.run(["pipx", "install", "kalamine"], check=True)
    elif command == "clean":
        clean()
    elif command == "install":
        install()
    elif command == "uninstall":
        uninstall()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
