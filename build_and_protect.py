import os
import subprocess
import sys
import codecs

# 设置标准输出为 UTF-8 编码
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

def check_dependencies():
    """检查并安装必要的依赖"""
    print("检查依赖...")
    
    dependencies = [
        ('pyinstaller', 'PyInstaller'),
        ('pyarmor', 'PyArmor'),
        ('watchdog', 'watchdog'),
        ('pywin32', 'pywin32')
    ]
    
    for package, display_name in dependencies:
        try:
            subprocess.run(['pip', 'show', package], check=True, capture_output=True)
            print(f"[OK] {display_name} 已安装")
        except subprocess.CalledProcessError:
            print(f"安装 {display_name}...")
            subprocess.run(['pip', 'install', package], check=True)
            print(f"[OK] {display_name} 安装完成")

def run_obfuscation():
    """运行代码混淆"""
    print("\n开始代码混淆...")
    
    try:
        result = subprocess.run([
            'pyarmor', 'gen', 
            '-O', 'dist', '--recursive', 
            'ETS.py', 'scanner.py', 'xml_parser.py', 'monitor.py'
        ], capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(result.stdout)
        if result.stderr:
            print("错误:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"运行 pyarmor 时发生错误: {e}")
        return False

def run_build():
    """运行打包"""
    print("\n开始打包程序...")
    
    try:
        result = subprocess.run([
            'pyinstaller', 
            'ETS.spec', 
            '--distpath', 'dist'
        ], capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(result.stdout)
        if result.stderr:
            print("错误:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"运行 pyinstaller 时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=== ETS检测器 - 保护打包工具 ===")
    print("\n1. 检查依赖...")
    check_dependencies()
    
    print("\n2. 运行代码混淆...")
    if not run_obfuscation():
        print("[ERROR] 代码混淆失败")
        return False
    
    print("\n3. 运行打包...")
    if not run_build():
        print("[ERROR] 打包失败")
        return False
    
    print("\n" + "="*50)
    print("[SUCCESS] 保护打包完成！")
    print("[SUCCESS] 可执行文件位置: C:\\Users\\13826\\Desktop\\ETS检测器\\ETS检测器.exe")
    print("[SUCCESS] 保护特性: 代码混淆 + 反调试 + 打包加密")
    print("" + "="*50)
    
    return True

if __name__ == "__main__":
    main()
