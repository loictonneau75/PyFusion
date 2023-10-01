import winreg
import re


def from_class_name_to_str(nom):
    # Enlever "App" à la fin
    nom = nom.replace("App", "")
    
    # Insérer un espace avant chaque majuscule, sauf s'il s'agit du premier caractère
    nom = re.sub(r'(?<=[a-z])([A-Z])', r' \1', nom)
    
    return nom

def is_os_light_mode():
        """
        Check if os is in light mode.

        Args:
            None

        Returns:
            bool: True if Windows is in light mode, False otherwise.
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            is_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return is_light_theme
        except Exception as e:
            print("Erreur lors de la détection du thème:", e)
            return None