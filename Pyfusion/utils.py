import re
from typing import Union

#TODO transformer cecie en static methode

def from_class_name_to_str(nom: str) -> str:
    nom: str = nom.replace("App", "")
    nom: str = re.sub(r'(?<=[a-z])([A-Z])', r' \1', nom).lower()
    return nom

def is_os_light_mode(os: str) -> bool | None:
        match os:
            case "Windows":
                return is_os_light_mode_windows()
            case "Darwin":
                return is_os_light_mode_mac()

def is_os_light_mode_windows() -> bool | None:
    #TODO fair le type hint depuis un windows
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        #TODO ligne pour voir le type de key
        #print (f"key = {key},\ntype = {type(key)}")
        is_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return is_light_theme
    except Exception as e:
        print("Erreur lors de la détection du thème:", e)
        return None

def is_os_light_mode_mac() -> bool | None:
    import subprocess
    try:
        result: subprocess.CompletedProcess = subprocess.run(['osascript', '-e', 'tell application "System Events" to tell appearance preferences to get dark mode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return result.stdout.strip() == 'false'
    except Exception as e:
        print("Erreur lors de la détection du thème:", e)
        return None