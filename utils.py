import winreg


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