import winreg
import shutil
from pathlib import Path
from importlib.resources import files
import os
import subprocess

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

def get_ahk_script_path() -> str:
    '''
    获取ahk脚本目录
    '''
    documents_path = Path.home() / "Documents"
    ahk_folder = documents_path / "AutoHotkey"
    if ahk_folder.exists():
        return str(ahk_folder)
    else:
        raise FileNotFoundError("AutoHotkey脚本目录不存在")


def get_rime_user_path() -> str:
    '''
    获取Rime用户目录
    '''
    rime_user_path = Path.home() / "AppData" / "Roaming" / "Rime"
    if rime_user_path.exists():
        return str(rime_user_path)
    else:
        raise FileNotFoundError("Rime用户目录不存在")

def get_weasel_install_path():
    '''
    智能获取小狼毫 (Weasel) 的安装根目录
    优先查询注册表，若失败则扫描默认安装路径
    '''
    sub_key = r'SOFTWARE\WOW6432Node\Rime\Weasel' # 64位系统下的32位程序路径
    
    # 1. 尝试从注册表读取
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key) as key:
            install_dir, _ = winreg.QueryValueEx(key, 'InstallDir')
            if install_dir:
                return Path(install_dir)
    except (FileNotFoundError, OSError):
        pass

    # 2. 注册表失败，尝试手动扫描默认路径
    # 小狼毫通常安装在 Program Files (x86)\Rime
    prog_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
    possible_path = Path(prog_x86) / "Rime"
    
    if possible_path.exists():
        return possible_path
        
    return None

def get_weasel_deployer_path():
    '''
    在安装目录下寻找最新的 WeaselDeployer.exe
    '''
    install_dir = get_weasel_install_path()
    if not install_dir:
        return None
    
    # 小狼毫的结构通常是 Rime\weasel-x.x.x\WeaselDeployer.exe
    # 使用 glob 查找所有符合条件的 exe
    deployers = list(install_dir.glob("weasel-*/WeaselDeployer.exe"))
    
    if not deployers:
        # 尝试直接在根目录下找（以防版本结构变化）
        deployers = list(install_dir.glob("**/WeaselDeployer.exe"))

    if deployers:
        # 返回版本号最大的那一个（最新版）
        return str(sorted(deployers)[-1])
    
    return None

def rime_deploy():
    '''
    执行部署命令
    '''
    deployer = get_weasel_deployer_path()
    
    if not deployer:
        print("错误：未找到 WeaselDeployer.exe，请确认小狼毫已安装。")
        return False
        
    try:
        print(f"正在触发部署: {deployer}")
        # /deploy 参数是静默部署的核心
        subprocess.run([deployer, "/deploy"], check=True)
        print("部署任务已启动 (请观察任务栏图标颜色变化)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"部署失败: {e}")
        return False

def run_ahk_script(script_path: str) -> bool:
    '''
    启动指定的AHK脚本
    '''
    ahk_path = get_ahk_path()
    if not ahk_path:
        print("错误：未找到 AutoHotkey，请确认已安装。")
        return False
    try:
        subprocess.Popen([ahk_path, script_path])
        print(f"已启动AHK脚本: {script_path}")
        return True
    except Exception as e:
        print(f"启动AHK脚本失败: {e}")
        return False
    
    
def copy_asset(package: str, filename: str, target_dir: str):
    '''
    复制资源到指定目录
    '''
    source = files(package).joinpath(filename)
    dest = Path(target_dir) / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)

def start_colemak_for_qwerty_win():
    '''
    在windows上启用colemak的autohotkey映射和rime映射
    '''
    autohotkey_file = 'colemak_dh_ansi.ahk'
    autohotkey_script_dir = get_ahk_script_path()
    copy_asset('bootme.assets.autohotkeys', autohotkey_file, autohotkey_script_dir)
    
    # TODO: rime
    
    run_ahk_script(os.path.join(autohotkey_script_dir, autohotkey_file))
    rime_deploy()
    
