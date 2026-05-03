import winreg
from pathlib import Path

def get_ahk_path():
    '''
    获取AutoHotkey的路径
    '''
    sub_key = r'Software\AutoHotkey'

    for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(root, sub_key) as key:
                install_dir, _ = winreg.QueryValueEx(key, 'InstallDir')
                return f"{install_dir}\\v2\\AutoHotkey64.exe"
        except FileNotFoundError:
            continue
    return None

def get_ahk_folder() -> str:
    '''
    获取ahk脚本目录
    '''
    documents_path = Path.home() / "Documents"
    ahk_folder = documents_path / "AutoHotkey"
    if ahk_folder.exists():
        return str(ahk_folder)
    else:
        raise FileNotFoundError("AutoHotkey脚本目录不存在")

