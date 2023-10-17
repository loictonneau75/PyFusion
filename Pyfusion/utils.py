import re


def from_class_name_to_str(nom):
    nom = nom.replace("App", "")
    nom = re.sub(r'(?<=[a-z])([A-Z])', r' \1', nom).lower()
    return nom

def is_os_light_mode(os):
        match os:
            case "Windows":
                return is_os_light_mode_windows()
            case "Darwin":
                return is_os_light_mode_mac()

def is_os_light_mode_windows():
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        is_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return is_light_theme
    except Exception as e:
        print("Erreur lors de la détection du thème:", e)
        return None
    
def is_os_light_mode_mac():
    import subprocess
    try:
        result = subprocess.run(['osascript', '-e', 'tell application "System Events" to tell appearance preferences to get dark mode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if result.returncode == 0:
            return result.stdout.strip() == 'false'  # 'false' means light mode
        else:
            print("Erreur lors de la détection du thème:", result.stderr)
            return None
    except Exception as e:
        print("Erreur lors de la détection du thème:", e)
        return None