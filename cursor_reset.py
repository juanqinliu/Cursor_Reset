import os
import sys
import shutil
import random
import string
import subprocess
import threading
import time
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# 设置customtkinter主题
ctk.set_appearance_mode("System")  # 跟随系统主题
ctk.set_default_color_theme("blue")  # 蓝色主题

# 适配不同系统的 Cursor 配置文件路径
CONFIG_PATHS = {
    "windows": os.path.expanduser("~\\AppData\\Roaming\\Cursor\\machineid"),
    "darwin": os.path.expanduser("~/Library/Application Support/Cursor/machineid"),
    "linux": os.path.expanduser("~/.config/Cursor/machineid"),
}

LOG_FILE = os.path.expanduser("~/.cursor_reset_log")

# 获取当前系统
def get_system():
    platform = sys.platform
    if platform.startswith("win"):
        return "windows"
    elif platform == "darwin":
        return "darwin"
    elif platform.startswith("linux"):
        return "linux"
    else:
        messagebox.showerror("Error", "Unsupported OS.")
        sys.exit(1)

# 关闭 Cursor 进程
def kill_cursor():
    try:
        if sys.platform.startswith("win"):
            subprocess.run(["taskkill", "/F", "/IM", "cursor.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-f", "Cursor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to close Cursor: {e}")

# 备份 machineid 文件
def backup_machineid(config_path):
    if os.path.exists(config_path):
        backup_dir = os.path.join(os.path.dirname(config_path), "Backups")
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f"machineid_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        shutil.copy(config_path, backup_file)
        return backup_file
    return None

# 生成新的随机设备 ID
def generate_device_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))

# 重置 machineid
def reset_machineid(config_path):
    if os.path.exists(config_path):
        new_id = generate_device_id()
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_id)
        return new_id
    return None

# 记录重置历史
def log_reset():
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - Cursor trial reset\n")

class CursorResetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cursor 重置工具")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("cursor.ico")
        except:
            pass
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 状态显示
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label_title = ctk.CTkLabel(self.status_frame, text="状态信息:", font=("Helvetica", 12, "bold"))
        self.status_label_title.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="就绪", font=("Helvetica", 12))
        self.status_label.pack(side="left", padx=5)
        
        # 操作按钮区域
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        
        self.button_frame_label = ctk.CTkLabel(self.button_frame, text="操作选项", font=("Helvetica", 14, "bold"))
        self.button_frame_label.pack(pady=5)
        
        self.button_container = ctk.CTkFrame(self.button_frame)
        self.button_container.pack(fill="x", padx=20, pady=5)
        
        self.reset_button = ctk.CTkButton(
            self.button_container, 
            text="重置 Cursor",
            command=self.reset_cursor,
            width=200,
            height=40,
            corner_radius=8,
            font=("Helvetica", 14, "bold")
        )
        self.reset_button.pack(side="left", padx=10, pady=10)
        
        self.backup_button = ctk.CTkButton(
            self.button_container, 
            text="备份当前配置",
            command=self.backup_current,
            width=200,
            height=40,
            corner_radius=8,
            font=("Helvetica", 14, "bold")
        )
        self.backup_button.pack(side="right", padx=10, pady=10)
        
        # 日志显示
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_label = ctk.CTkLabel(self.log_frame, text="操作日志", font=("Helvetica", 14, "bold"))
        self.log_label.pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(self.log_frame, height=300, width=460, font=("Courier", 12))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 加载历史日志
        self.load_logs()
    
    def log(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert("end", f"[{current_time}] {message}\n")
        self.log_text.see("end")
        self.status_label.configure(text=message)
        
    def load_logs(self):
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    logs = f.readlines()[-10:]  # 只显示最后10条日志
                    for log in logs:
                        self.log_text.insert("end", log)
                self.log_text.see("end")
                self.log("历史日志加载完成")
            else:
                self.log("暂无历史日志")
        except Exception as e:
            self.log(f"加载日志失败: {e}")
    
    def backup_current(self):
        system = get_system()
        config_path = CONFIG_PATHS.get(system)
        if config_path and os.path.exists(config_path):
            backup_file = backup_machineid(config_path)
            self.log(f"已创建配置文件备份: {backup_file}")
            messagebox.showinfo("备份成功", f"Cursor 配置已备份至:\n{backup_file}")
        else:
            messagebox.showerror("错误", "未找到 Cursor 配置文件")
            self.log("备份失败: 未找到配置文件")
    
    def reset_cursor(self):
        if messagebox.askyesno("确认", "确定要重置 Cursor 吗？\n这将关闭当前运行的 Cursor 并重置试用期。"):
            self.log("开始重置 Cursor...")
            self.reset_button.configure(state='disabled')
            
            def reset_thread():
                try:
                    system = get_system()
                    config_path = CONFIG_PATHS.get(system)
                    
                    if not config_path:
                        self.root.after(0, lambda: messagebox.showerror("错误", "不支持的操作系统"))
                        self.root.after(0, lambda: self.log("重置失败: 不支持的操作系统"))
                        return
                    
                    self.log("正在关闭 Cursor...")
                    kill_cursor()
                    
                    # 等待0.5秒确保 Cursor 完全关闭
                    time.sleep(0.5)
                    
                    self.log("正在备份配置...")
                    backup_file = backup_machineid(config_path)
                    if backup_file:
                        self.log(f"备份创建成功: {backup_file}")
                    
                    self.log("正在重置配置...")
                    new_id = reset_machineid(config_path)
                    if new_id:
                        self.log(f"重置成功，新设备ID: {new_id}")
                    else:
                        self.root.after(0, lambda: messagebox.showerror("错误", "Cursor 配置文件未找到"))
                        self.log("重置失败: 配置文件未找到")
                        return
                    
                    self.log("正在记录操作...")
                    log_reset()
                    
                    self.log("重置完成！")
                    
                    # 先显示完成消息框，然后再关闭窗口
                    def show_completion():
                        messagebox.showinfo("完成", f"Cursor 已重置完成！\n新设备ID: {new_id}")
                        self.root.destroy()
                    
                    self.root.after(0, show_completion)
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("错误", f"重置过程中出错: {e}"))
                    self.log(f"重置失败: {e}")
                finally:
                    self.root.after(0, lambda: self.reset_button.configure(state='normal'))
            
            threading.Thread(target=reset_thread, daemon=True).start()

# 主函数
def main():
    root = ctk.CTk()  # 使用CTk代替Tk
    app = CursorResetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
