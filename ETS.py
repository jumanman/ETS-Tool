import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from scanner import DirectoryScanner
from monitor import XMLMonitor


class XMLMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETS检测器")
        self.root.geometry("900x600")
        self.root.minsize(700, 400)
        
        # 设置主题色
        self.bg_color = "#f5f5f5"
        self.primary_color = "#2196F3"
        self.text_bg = "#ffffff"
        self.text_fg = "#333333"
        self.accent_color = "#4CAF50"
        
        self.root.configure(bg=self.bg_color)
        
        # 初始化模块
        self.scanner = DirectoryScanner()
        self.monitor = XMLMonitor(self)
        
        # 监控相关变量
        self.watch_dir = None
        
        self._create_ui()
        self._auto_scan()
        
    def _create_ui(self):
        # 顶部标题栏
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="ETS检测器", 
            font=("Microsoft YaHei", 14, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=8)
        
        # 主内容区
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 控制按钮区
        control_frame = tk.Frame(content_frame, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.select_btn = tk.Button(
            control_frame,
            text="选择目录",
            font=("Microsoft YaHei", 10),
            bg=self.primary_color,
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.select_directory
        )
        self.select_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.scan_btn = tk.Button(
            control_frame,
            text="自动扫描",
            font=("Microsoft YaHei", 10),
            bg="#FF9800",
            fg="white",
            activebackground="#F57C00",
            activeforeground="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.auto_scan_directory
        )
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.start_btn = tk.Button(
            control_frame,
            text="开始监控",
            font=("Microsoft YaHei", 10),
            bg=self.accent_color,
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.toggle_monitoring,
            state=tk.DISABLED
        )
        self.start_btn.pack(side=tk.LEFT)
        
        # 状态标签
        self.status_label = tk.Label(
            control_frame,
            text="就绪 - 请选择要监控的目录",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            fg="#666666"
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # 目录显示
        self.dir_frame = tk.Frame(content_frame, bg=self.bg_color)
        self.dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        dir_label = tk.Label(
            self.dir_frame,
            text="当前目录:",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            fg="#555555"
        )
        dir_label.pack(side=tk.LEFT)
        
        self.dir_var = tk.StringVar(value="未选择")
        self.dir_display = tk.Label(
            self.dir_frame,
            textvariable=self.dir_var,
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            fg="#888888",
            anchor=tk.W
        )
        self.dir_display.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # 输出区域
        output_frame = tk.Frame(content_frame, bg=self.bg_color)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题栏（包含标签和清空按钮）
        output_header = tk.Frame(output_frame, bg=self.bg_color)
        output_header.pack(fill=tk.X, pady=(0, 5))
        
        output_label = tk.Label(
            output_header,
            text="解析结果",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self.bg_color,
            fg="#333333"
        )
        output_label.pack(side=tk.LEFT)
        
        self.clear_btn = tk.Button(
            output_header,
            text="清空",
            font=("Microsoft YaHei", 9),
            bg="#757575",
            fg="white",
            activebackground="#616161",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.clear_output
        )
        self.clear_btn.pack(side=tk.RIGHT)
        
        # 使用 scrolledtext 作为输出区域
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=self.text_bg,
            fg=self.text_fg,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED,
            exportselection=False  # 禁用文本选择
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 禁用所有选择相关的绑定
        self.output_text.bind("<Button-1>", lambda e: "break" if self.output_text.tag_names(tk.CURRENT) else None)
        self.output_text.bind("<B1-Motion>", lambda e: "break")
        self.output_text.bind("<Double-Button-1>", lambda e: "break")
        self.output_text.bind("<Triple-Button-1>", lambda e: "break")
        self.output_text.bind("<Shift-Button-1>", lambda e: "break")
        self.output_text.bind("<Control-a>", lambda e: "break")
        self.output_text.bind("<Control-c>", lambda e: "break")
        
        # 配置标签样式 - 柔和颜色，10种
        self.output_text.tag_configure("c1", foreground="#5C6BC0")   # 靛蓝
        self.output_text.tag_configure("c2", foreground="#26A69A")   # 青绿
        self.output_text.tag_configure("c3", foreground="#EF5350")   # 珊瑚红
        self.output_text.tag_configure("c4", foreground="#AB47BC")   # 紫罗兰
        self.output_text.tag_configure("c5", foreground="#FFA726")   # 橙黄
        self.output_text.tag_configure("c6", foreground="#42A5F5")   # 天蓝
        self.output_text.tag_configure("c7", foreground="#7E57C2")   # 深紫
        self.output_text.tag_configure("c8", foreground="#66BB6A")   # 草绿
        self.output_text.tag_configure("c9", foreground="#EC407A")   # 粉红
        self.output_text.tag_configure("c10", foreground="#8D6E63")  # 棕色
        self.output_text.tag_configure("fold", foreground="#2196F3", underline=True)  # 可点击的蓝色
        self.output_text.tag_configure("hidden", elide=True)  # 隐藏标签
        self.output_text.tag_configure("bold", foreground="#37474F", font=("Consolas", 11, "bold"))  # 深灰加粗
        
        # 存储折叠状态和完整数据
        self.folded_data = {}  # {mark_name: (parts, max_show, color_tag)}
        self.fold_index = 0
        
        # 绑定点击事件
        self.output_text.tag_bind("fold", "<Button-1>", self._on_fold_click)
        self.output_text.tag_bind("fold", "<Enter>", lambda e: self.output_text.config(cursor="hand2"))
        self.output_text.tag_bind("fold", "<Leave>", lambda e: self.output_text.config(cursor=""))
        
    def _auto_scan(self):
        """启动时自动扫描"""
        self.root.after(500, self.auto_scan_directory)
    
    def select_directory(self):
        """让用户选择要监控的目录"""
        folder_path = filedialog.askdirectory(title="选择要监控的目录")
        
        if not folder_path:
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("错误", f"目录不存在: {folder_path}")
            return
        
        self.watch_dir = folder_path
        self.dir_var.set(folder_path)
        self.start_btn.config(state=tk.NORMAL)
        
    def auto_scan_directory(self):
        """自动扫描开始菜单，查找 ETS/E听说软件目录下的 soundfiles"""
        self.status_label.config(text="正在扫描...", fg="#FF9800")
        self.root.update()
        
        soundfiles_dir = self.scanner.find_soundfiles_directory()
        
        if soundfiles_dir:
            self.watch_dir = soundfiles_dir
            self.dir_var.set(soundfiles_dir)
            self.start_btn.config(state=tk.NORMAL)
            self.status_label.config(text="扫描成功 - 已找到目录", fg=self.accent_color)
        else:
            messagebox.showinfo("扫描结果", "未找到 ETS 或 E听说软件的 soundfiles 目录\n请手动选择目录")
            self.status_label.config(text="扫描失败 - 未找到目录", fg="#666666")
    
    def toggle_monitoring(self):
        """开始或停止监控"""
        if not self.monitor.is_monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        """开始监控"""
        if not self.watch_dir:
            return
            
        if self.monitor.start(self.watch_dir):
            self.start_btn.config(text="停止监控", bg="#f44336", activebackground="#d32f2f")
            self.status_label.config(text="正在监控中...", fg=self.accent_color)
            self.select_btn.config(state=tk.DISABLED)
            self.scan_btn.config(state=tk.DISABLED)
        else:
            messagebox.showerror("错误", "启动监控失败")
            
    def stop_monitoring(self):
        """停止监控"""
        self.monitor.stop()
        self.start_btn.config(text="开始监控", bg=self.accent_color, activebackground="#45a049")
        self.status_label.config(text="监控已停止", fg="#666666")
        self.select_btn.config(state=tk.NORMAL)
        self.scan_btn.config(state=tk.NORMAL)
        
    def update_results(self, results):
        """更新解析结果显示 - keypoint保留1行，keyword保留3行，后面的可点击展开"""
        self.output_text.config(state=tk.NORMAL)
        
        # 颜色标签列表 - 10种柔和颜色
        color_tags = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10"]
        
        if results:
            for result_idx, (result_type, result_value) in enumerate(results):
                # 按 | 分隔
                parts = result_value.split("|")
                # 清理空白
                parts = [p.strip() for p in parts if p.strip()]
                
                if not parts:
                    continue
                
                # 每个结果使用一种颜色
                color_tag = color_tags[result_idx % len(color_tags)]
                
                # 根据类型决定显示方式
                if result_type == "keypoint":
                    # keypoint 显示所有内容，不折叠
                    for i, part in enumerate(parts):
                        tag = "bold" if i == 0 else color_tag
                        self.output_text.insert(tk.END, f"{i+1}. {part}\n", tag)
                    self.output_text.insert(tk.END, "\n")
                else:
                    # keyword 显示前3行，后面的可折叠
                    max_show = 3
                    
                    # 显示前N行
                    show_count = min(max_show, len(parts))
                    for i in range(show_count):
                        tag = "bold" if i == 0 else color_tag
                        self.output_text.insert(tk.END, f"{i+1}. {parts[i]}\n", tag)
                    
                    # 如果有更多内容，显示可点击的折叠提示
                    if len(parts) > max_show:
                        fold_mark = f"fold_{self.fold_index}"
                        self.fold_index += 1
                        
                        # 创建标记
                        self.output_text.mark_set(fold_mark, tk.INSERT)
                        self.output_text.mark_gravity(fold_mark, tk.LEFT)
                        
                        # 存储数据用于展开
                        self.folded_data[fold_mark] = (parts, max_show, color_tag, False)  # False = 折叠状态
                        
                        # 插入可点击的箭头提示
                        start_idx = self.output_text.index(tk.INSERT)
                        self.output_text.insert(tk.END, f"   ▶ {len(parts)-max_show}\n", ("fold", fold_mark))
                        end_idx = self.output_text.index(tk.INSERT)
                        
                        # 为这部分添加fold标签
                        self.output_text.tag_add("fold", start_idx, end_idx)
                    
                    self.output_text.insert(tk.END, "\n")
        
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def _on_fold_click(self, event):
        """处理折叠提示点击事件"""
        # 获取点击位置的索引
        index = self.output_text.index(f"@{event.x},{event.y}")
        
        # 查找点击位置的所有标记
        for mark_name in self.folded_data.keys():
            # 检查点击是否在标记范围内
            mark_range = self.output_text.tag_nextrange(mark_name, "1.0", tk.END)
            if mark_range:
                start, end = mark_range
                if self.output_text.compare(start, "<=", index) and self.output_text.compare(index, "<", end):
                    self._toggle_fold(mark_name)
                    return
    
    def _toggle_fold(self, mark_name):
        """切换折叠/展开状态"""
        if mark_name not in self.folded_data:
            return
        
        parts, max_show, color_tag, is_expanded = self.folded_data[mark_name]
        
        self.output_text.config(state=tk.NORMAL)
        
        # 获取标记范围
        mark_range = self.output_text.tag_nextrange(mark_name, "1.0", tk.END)
        if not mark_range:
            self.output_text.config(state=tk.DISABLED)
            return
        
        start, end = mark_range
        
        if not is_expanded:
            # 展开：删除提示，插入隐藏的内容
            self.output_text.delete(start, end)
            
            # 先插入折叠箭头
            self.output_text.insert(start, "   ▼\n", ("fold", mark_name))
            
            # 再按顺序插入隐藏的内容（从后往前插入，这样显示顺序正确）
            insert_pos = f"{start}+1l"
            for i in range(max_show, len(parts)):
                self.output_text.insert(insert_pos, f"{i+1}. {parts[i]}\n", color_tag)
            
            self.folded_data[mark_name] = (parts, max_show, color_tag, True)
        else:
            # 折叠：删除展开的内容，恢复提示
            # 计算要删除的行数
            lines_to_delete = len(parts) - max_show + 1  # +1 for the fold line
            
            # 删除所有展开的内容
            self.output_text.delete(start, f"{start}+{lines_to_delete}l")
            
            # 插入折叠箭头
            self.output_text.insert(start, f"   ▶ {len(parts)-max_show}\n", ("fold", mark_name))
            end = self.output_text.index(start + "+1l")
            self.output_text.tag_add("fold", start, end)
            
            self.folded_data[mark_name] = (parts, max_show, color_tag, False)
        
        self.output_text.config(state=tk.DISABLED)
    
    def clear_output(self):
        """清空输出区域"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = XMLMonitorApp(root)
    
    # 窗口关闭时停止监控
    def on_closing():
        if app.monitor.is_monitoring:
            app.stop_monitoring()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
