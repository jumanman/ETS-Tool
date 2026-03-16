import os
import glob
import win32com.client


class DirectoryScanner:
    def __init__(self):
        self.keywords = ["ETS", "E听说中学", "E听说"]
    
    def find_soundfiles_directory(self):
        """查找 ETS/E听说软件的 soundfiles 目录"""
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            start_menu = shell.SpecialFolders("StartMenu")
            programs = os.path.join(start_menu, "Programs")
            
            if not os.path.exists(programs):
                return None
            
            found_dirs = []
            
            for root, dirs, files in os.walk(programs):
                for dir_name in dirs:
                    if any(keyword.lower() in dir_name.lower() for keyword in self.keywords):
                        dir_path = os.path.join(root, dir_name)
                        lnk_files = glob.glob(os.path.join(dir_path, "*.lnk"))
                        
                        for lnk_file in lnk_files:
                            shortcut = shell.CreateShortCut(lnk_file)
                            target_path = shortcut.Targetpath
                            
                            if target_path and os.path.exists(target_path):
                                app_dir = os.path.dirname(target_path)
                                soundfiles_path = os.path.join(app_dir, "soundfiles")
                                
                                if os.path.exists(soundfiles_path):
                                    found_dirs.append(soundfiles_path)
            
            if found_dirs:
                return found_dirs[0]
            
            return None
            
        except Exception as e:
            print(f"扫描出错: {e}")
            return None
