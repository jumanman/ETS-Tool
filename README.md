# ETS检测器

一个基于 Python 的 ETS/E听说 软件答案检测工具，支持实时监控 XML 文件变化并解析答案。

## 免责声明

**注意：不要滥用，禁止将本工具用于非法用途（包括但不限于作弊）。**

本工具提供给学习成绩好但不想做ETS的学生（成绩不好就老老实实做ETS）。

本工具仅适用于 Windows，并且需要安装 ETS 的电脑版。

**Note: Do not abuse this tool; it is prohibited to use it for illegal purposes (including but not limited to cheating).**

This tool is intended for students with good grades who are unable to take the ETS exam (students with poor grades should take the ETS exam honestly).

This tool is only compatible with Windows and requires the installation of the PC version of ETS.

## 功能特性

- 自动扫描开始菜单寻找 ETS 软件目录
- 简洁美观的 GUI 界面
- 支持结果折叠/展开

## 系统要求

- Windows 10/11
- Python 3.13+

## 安装依赖

```bash
pip install watchdog pywin32
```

## 使用方法

### 运行源码

```bash
python ETS.py
```


## 项目结构

```
ETS/
├── ETS.py                 # 主程序文件
├── scanner.py              # 目录扫描模块
├── xml_parser.py           # XML 解析模块
├── monitor.py              # 文件监控模块
├── ETS.spec               # PyInstaller 配置
└── .gitignore             # Git 忽略文件
```

## 注意事项

- 需要管理员权限才能监控某些系统目录
- 首次运行可能需要防火墙权限

## 许可证

本项目仅供学习交流使用。
