# ETS检测器 - 打包和反编译保护说明

## 概述

本项目提供了代码混淆和打包成可执行文件的功能，以提升程序的反编译保护能力。

## 依赖安装

在开始之前，请确保安装以下依赖：

```bash
pip install pyinstaller pyarmor watchdog pywin32
```

## 打包流程

### 一键打包（推荐）

使用 `build_and_protect.py` 自动完成代码混淆和打包：

```bash
python build_and_protect.py
```

打包后的可执行文件位于 `dist/ETS检测器.exe`

### 手动打包

如需手动控制打包过程，可以分步执行：

```bash
# 第一步：代码混淆
pyarmor gen -O dist --recursive ETS.py scanner.py xml_parser.py monitor.py

# 第二步：打包
pyinstaller ETS.spec --distpath dist
```

## 文件说明

- **ETS.py** - 主程序文件
- **scanner.py** - 目录扫描模块
- **xml_parser.py** - XML解析模块
- **monitor.py** - 监控模块
- **ETS.spec** - PyInstaller 配置文件
- **build_and_protect.py** - 一键打包脚本（包含代码混淆）

## 保护级别说明

### 基础保护（PyInstaller）
- 将 Python 代码编译为字节码
- 打包成单个可执行文件
- 隐藏源代码
- 使用 UPX 压缩可执行文件

### 高级保护（PyArmor + PyInstaller）
- 代码加密混淆
- 反调试保护
- 防止反编译工具分析

## 注意事项

1. **测试打包结果**：打包后请测试可执行文件是否正常运行
2. **更新依赖**：如果修改了代码或依赖，需要重新打包
3. **杀毒软件**：打包后的程序可能被杀毒软件误报，请添加信任

## 常见问题

### Q: 打包后程序无法运行？
A: 检查是否所有依赖都已安装，确保 `ETS.spec` 中的 `hiddenimports` 包含所有需要的模块。

### Q: PyArmor 混淆后程序报错？
A: 某些动态导入的代码可能无法混淆，可以尝试只混淆主要模块。

### Q: 如何去除 UPX 压缩？
A: 在 `ETS.spec` 中将 `upx=True` 改为 `upx=False`

## 清理构建文件

如需清理构建文件，删除以下目录：
- `build/` - PyInstaller 构建目录
- `dist/` - 打包输出目录
- `__pycache__/` - Python 缓存目录

## 许可证

本程序仅供学习和个人使用。
