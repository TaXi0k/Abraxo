# /// script
# dependencies = [
#     "watchdog"
# ]
# ///

import os
import subprocess
import shutil
from pathlib import Path
from watchdog.observers import Observer     # type: ignore
from watchdog.events import FileSystemEventHandler      # type: ignore

# ==================================================

TEMP_EXTENSIONS = [
    ".crdownload",
    ".part",
    ".download",
    ".opdownload",
    ".aria2",
    ".tmp",
    ".temp",
    ".!qb",
    ".bt!"
]

EXTENSION_MAP = {
    # Images
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".jfif": "Images",
    ".pjpeg": "Images",
    ".pjp": "Images",
    ".webp": "Images",
    ".avif": "Images",
    ".jxl": "Images",
    ".gif": "Images",
    ".apng": "Images",
    ".svg": "Images",
    ".svgz": "Images",
    ".ico": "Images",
    ".cur": "Images",
    ".bmp": "Images",
    ".tiff": "Images",
    ".tif": "Images",
    ".heic": "Images",
    ".heif": "Images",
    ".psd": "Images",
    ".af": "Images",
    ".afphoto": "Images",
    ".afdesign": "Images",
    ".afpub": "Images",
    ".fig": "Images",
    ".procreate": "Images",
    ".sketch": "Images",
    ".excalidraw": "Images",
    ".ai": "Images",
    ".xcf": "Images",
    ".kra": "Images",
    ".ora": "Images",
    # Camera Raw formats
    ".raw": "Images",
    ".cr2": "Images",
    ".cr3": "Images",
    ".nef": "Images",
    ".arw": "Images",
    ".dng": "Images",
    ".orf": "Images",
    ".pef": "Images",
    ".rw2": "Images",
    ".sr2": "Images",
    ".raf": "Images",

    # Code, Config, Markup & Scripts
    ".py": "Code",
    ".pyw": "Code",
    ".ipynb": "Code",
    ".js": "Code",
    ".mjs": "Code",
    ".cjs": "Code",
    ".ts": "Code",
    ".tsx": "Code",
    ".jsx": "Code",
    ".vue": "Code",
    ".svelte": "Code",
    ".astro": "Code",
    ".go": "Code",
    ".c": "Code",
    ".h": "Code",
    ".cpp": "Code",
    ".cc": "Code",
    ".cxx": "Code",
    ".hpp": "Code",
    ".hxx": "Code",
    ".cs": "Code",
    ".java": "Code",
    ".class": "Code",
    ".jar": "Code",
    ".rb": "Code",
    ".php": "Code",
    ".swift": "Code",
    ".kt": "Code",
    ".kts": "Code",
    ".scala": "Code",
    ".rs": "Code",
    ".ron": "Code",
    ".zig": "Code",
    ".nim": "Code",
    ".lua": "Code",
    ".ex": "Code",
    ".exs": "Code",
    ".erl": "Code",
    ".hrl": "Code",
    ".clj": "Code",
    ".hs": "Code",
    ".ml": "Code",
    ".mli": "Code",
    ".html": "Code",
    ".htm": "Code",
    ".xhtml": "Code",
    ".css": "Code",
    ".scss": "Code",
    ".sass": "Code",
    ".less": "Code",
    ".json": "Code",
    ".jsonc": "Code",
    ".json5": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".toml": "Code",
    ".xml": "Code",
    ".ini": "Code",
    ".cfg": "Code",
    ".conf": "Code",
    ".env": "Code",
    ".properties": "Code",
    ".sql": "Code",
    ".prisma": "Code",
    ".graphql": "Code",
    ".gql": "Code",
    ".sh": "Code",
    ".bash": "Code",
    ".zsh": "Code",
    ".fish": "Code",
    ".bat": "Code",
    ".cmd": "Code",
    ".ps1": "Code",
    ".psm1": "Code",
    ".psd1": "Code",
    ".dockerfile": "Code",
    ".tf": "Code",
    ".tfvars": "Code",
    ".hcl": "Code",
    ".cmake": "Code",
    ".make": "Code",

    # Documents, Text & E-books
    ".pdf": "Documents",
    ".txt": "Documents",
    ".rst": "Documents",
    ".adoc": "Documents",
    ".rtf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".dot": "Documents",
    ".dotx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".xlsm": "Documents",
    ".xlsb": "Documents",
    ".xlt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".pps": "Documents",
    ".odt": "Documents",
    ".ods": "Documents",
    ".odp": "Documents",
    ".odg": "Documents",
    ".odf": "Documents",
    ".csv": "Documents",
    ".tsv": "Documents",
    ".epub": "Documents",
    ".mobi": "Documents",
    ".azw3": "Documents",
    ".djvu": "Documents",
    ".pages": "Documents",
    ".key": "Documents",
    ".numbers": "Documents",
    ".tex": "Documents",
    ".bib": "Documents",

    # Archives & Disk Images
    ".zip": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".tgz": "Archives",
    ".tbz2": "Archives",
    ".txz": "Archives",
    ".bz2": "Archives",
    ".7z": "Archives",
    ".rar": "Archives",
    ".z": "Archives",
    ".lz": "Archives",
    ".lzma": "Archives",
    ".xz": "Archives",
    ".cab": "Archives",
    ".iso": "Archives",
    ".img": "Archives",

    # Executables & Installers
    ".appimage": "Executables",
    ".exe": "Executables",
    ".msi": "Executables",
    ".dmg": "Executables",
    ".pkg": "Executables",
    ".deb": "Executables",
    ".rpm": "Executables",
    ".apk": "Executables",
    ".bin": "Executables",
    ".run": "Executables",

    # Media - Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",
    ".oga": "Audio",
    ".m4a": "Audio",
    ".m4b": "Audio",
    ".wma": "Audio",
    ".opus": "Audio",
    ".ape": "Audio",
    ".alac": "Audio",
    ".aiff": "Audio",
    ".aif": "Audio",
    ".mid": "Audio",
    ".midi": "Audio",
    ".amr": "Audio",
    ".ac3": "Audio",

    # Media - Video
    ".mp4": "Video",
    ".mkv": "Video",
    ".mov": "Video",
    ".avi": "Video",
    ".webm": "Video",
    ".flv": "Video",
    ".wmv": "Video",
    ".m4v": "Video",
    ".mpg": "Video",
    ".mpeg": "Video",
    ".m2ts": "Video",
    ".mts": "Video",
    ".ts": "Video",
    ".ogv": "Video",
    ".3gp": "Video",
    ".3g2": "Video",
    ".rm": "Video",
    ".rmvb": "Video",
    ".vob": "Video",
    ".divx": "Video",
    ".xvid": "Video",
    ".asf": "Video",
}
match (os.getenv("MD_CODE") or "false").lower():
    case "true" | "1":
        EXTENSION_MAP[".md"] = "Code"
        EXTENSION_MAP[".markdown"] = "Code"
    case _:
        EXTENSION_MAP[".md"] = "Documents"
        EXTENSION_MAP[".markdown"] = "Documents"


BOLD = "\033[1m"
COLOR_MAIN = "\033[1m\033[38;2;255;100;68m"
COLOR_DARK = "\033[1m\033[38;2;168;63;42m"
RESET = "\033[0m"
MOTD_ART = f"""{COLOR_MAIN}
 @@@@@@@{COLOR_DARK}.    -{COLOR_MAIN}@@@@@@@@@#  {COLOR_DARK}:{COLOR_MAIN}@@@@@@@@@{COLOR_DARK}@{COLOR_MAIN}     @@@@@@{COLOR_DARK}@{COLOR_MAIN}     @@@@@{COLOR_DARK}@{COLOR_MAIN} @@@@{COLOR_DARK}@{COLOR_MAIN}   .@@@@@{COLOR_DARK}@{COLOR_MAIN}
 {COLOR_DARK}-#.{COLOR_MAIN}@@@@@     @*@@    @@@  @+@@    @@@{COLOR_DARK}#{COLOR_MAIN}   {COLOR_DARK}@-{COLOR_MAIN}@@@@@{COLOR_DARK}@{COLOR_MAIN}    {COLOR_DARK}.+{COLOR_MAIN}@@{COLOR_DARK}@. .{COLOR_MAIN}@@{COLOR_DARK}@.{COLOR_MAIN} {COLOR_DARK}-{COLOR_MAIN}@@@   {COLOR_DARK}-{COLOR_MAIN}@@{COLOR_DARK}@{COLOR_MAIN}
   @@{COLOR_DARK}.{COLOR_MAIN} @@@     {COLOR_DARK}:{COLOR_MAIN}@@...#@{COLOR_DARK}@@{COLOR_MAIN}   {COLOR_DARK}.{COLOR_MAIN}@@   {COLOR_DARK}.{COLOR_MAIN}@@@     {COLOR_DARK}:{COLOR_MAIN}@@  @{COLOR_DARK}@:{COLOR_MAIN}      *@@@@{COLOR_DARK}@{COLOR_MAIN}    @@{COLOR_DARK}@{COLOR_MAIN}      @@@
  @@@@@@@@@     @@---*@@{COLOR_DARK}@.{COLOR_MAIN}   @@@@@@        @@@@@@@@      {COLOR_DARK}.{COLOR_MAIN}@@@@@    {COLOR_DARK}@{COLOR_MAIN}@@      {COLOR_DARK}@{COLOR_MAIN}@@
{COLOR_DARK}.{COLOR_MAIN}#@@{COLOR_DARK}.{COLOR_MAIN}    @@{COLOR_DARK}=.{COLOR_MAIN}   @@    *@@@   @@   @@@@@@{COLOR_DARK}.{COLOR_MAIN} @@    {COLOR_DARK}.{COLOR_MAIN}%@@   {COLOR_DARK}:{COLOR_MAIN}@@  {COLOR_DARK}.%{COLOR_MAIN}@@@  {COLOR_DARK}-@{COLOR_MAIN}@@   {COLOR_DARK}:{COLOR_MAIN}@@@
@@@@@{COLOR_DARK}. :{COLOR_MAIN}@@@@@ @@@@@@@@@@   @@@@@@   @@  @@@@@@  @@@@@@@@@@@ @@@@@@   {COLOR_DARK}-@{COLOR_MAIN}@@@@@
{RESET}"""


# ==================================================

def get_downloads_dir():
    # Check if downloads directory is specified in env
    path = os.getenv('DOWNLOADS_DIRECTORY')
    if path:
        print(f"* Downloads directory set in ENV to: {path}")
        return os.path.expanduser(path)
    
    # Try to get downloads directory form xdg
    try:
        result = subprocess.run(
            ["xdg-user-dir", "DOWNLOAD"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        
        path = result.stdout.strip()
        
        if path:
            print(f"* xdg-user-dir returned successfully: {path}")
            return path
    
    except Exception:
        print(f"* Failed to get downloads directory from 'xdg-user-dir' as well as env, falling back to: {os.path.expanduser('~/Downloads')}")
        pass
    
    # Fallback
    return os.path.expanduser("~/Downloads")

# ==================================================

def safe_move(downloads_dir: str, file_path: Path, dest_folder: str):    
    try:
        target_dir = Path(os.path.join(downloads_dir, dest_folder))
        dest_path = target_dir / file_path.name
        
        if dest_path.exists():
            base = file_path.stem
            suffix = file_path.suffix
            counter = 1
            while dest_path.exists():
                dest_path = target_dir / f"{base}_{counter}{suffix}"
                counter += 1
        
        shutil.move(str(file_path), str(dest_path))
        print(f"Moved: {file_path.name} -> {dest_path}")
        
    except Exception as e:
        print(f"Ignored error on {file_path.name}: {e}")

# ==================================================

def ensure_subdirectories(downloads_dir: str):
    
    subdirs = ["Images", "Code", "Documents", "Archives", "Executables", "Audio", "Video"] # These exclude Others, for reason just look down :3
    
    # Check if directory Others exists
    if not os.path.isdir(os.path.join(downloads_dir, "Others")):
        # Check "Others" is a file, if so rename it to "Others.temp"
        if os.path.isfile(os.path.join(downloads_dir, "Others")):
            os.rename(os.path.join(downloads_dir, "Others"), os.path.join(downloads_dir, "Others.temp"))
        # Create the directory
        os.mkdir(os.path.join(downloads_dir, "Others"))
        # If "Others.temp" exists move it and rename back
        if os.path.isfile(os.path.join(downloads_dir, "Others.temp")):
            shutil.move(os.path.join(downloads_dir, "Others.temp"), os.path.join(downloads_dir, "Others" , "Others"))
        
    for subdir in subdirs:
        subdir_path = os.path.join(downloads_dir, subdir)
        if not os.path.isdir(subdir_path):
            # Check if subdir is a file, if it is, move it to Others (since it has no extension)
            if os.path.isfile(subdir_path):
                safe_move(downloads_dir, Path(subdir_path), "Others")
            # Create the directory
            os.mkdir(os.path.join(downloads_dir, subdir))

# ==================================================

def sort_file(downloads_dir: str, file_path: Path):
    if (
            file_path.is_file()
            and not file_path.name.startswith("#")
            and not file_path.name.startswith(".")
            and file_path.suffix.lower() not in TEMP_EXTENSIONS
        ):
        extension = file_path.suffix.lower()
        dest_folder = "Others"
        
        if extension in EXTENSION_MAP:
            dest_folder = EXTENSION_MAP[extension]
            
        safe_move(downloads_dir, file_path, dest_folder)
    else:        
        if file_path.name not in ["Images", "Code", "Documents", "Archives", "Executables", "Audio", "Video", "Others"]:
            print(f"* Skipping {file_path.name}")

# ==================================================

class FsEventsHandler(FileSystemEventHandler):
    def __init__(self, downloads_dir: str):
        super().__init__()
        self.downloads_dir = downloads_dir
    
    def on_moved(self, event):
        if not event.is_directory:
            sort_file(self.downloads_dir, Path(event.dest_path))
        
    def on_created(self, event):
        if not event.is_directory:
            sort_file(self.downloads_dir, Path(event.src_path))

# ==================================================

def main():
    print(MOTD_ART)
    print(f"{BOLD}Initializing Abraxo...{RESET}")
    
    # Get Downloads directoriy path
    print(f"{BOLD}\nGetting downloads directory path...{RESET}")
    downloads_dir = get_downloads_dir()

    # Ensure all subdirectories used by this app are present
    print(f"{BOLD}\nEnsuring presence of subdirectories...{RESET}")
    ensure_subdirectories(downloads_dir)

    # Sort files already present in Downloads
    print(f"{BOLD}\nSorting files present in {downloads_dir}...{RESET}")
    files = os.listdir(downloads_dir)
    for file in files:
        # print(file)
        sort_file(downloads_dir, Path(os.path.join(downloads_dir, file)))
        
    # Loop handling new files
    event_handler = FsEventsHandler(downloads_dir)
    observer = Observer()
    observer.schedule(event_handler, downloads_dir, recursive=False)
    observer.start()

# ==================================================

if __name__ == "__main__":
    main()