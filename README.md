# Cursor 重置工具

这是一个用于重置 Cursor 编辑器试用期的工具。

## 功能特点

- 支持 Windows、macOS 和 Linux 系统
- 自动备份当前配置
- 重置 Cursor 试用期
- 操作日志记录


## 安装方法

1. 克隆仓库：
```bash
git clone https://github.com/你的用户名/cursor-reset-tool.git
cd cursor-reset-tool
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：直接运行可执行文件

1. 双击 `dist/cursor_reset` 或 `dist/cursor_reset.exe`（Windows）
2. 点击 "Reset Cursor" 按钮
3. 确认关闭 Cursor 进程
4. 等待重置完成
5. 关闭

### 方法二：从源代码运行

1. 确保已安装 Python 3.6 或更高版本
2. 运行 `python cursor_reset.py`
3. 按照界面提示操作

## 从源代码构建可执行文件

如果你想自己打包可执行文件，可以按照以下步骤操作：

1. 安装依赖：`pip install pyinstaller`
2. 运行构建脚本：`pyinstaller --onefile --windowed cursor_reset.py`
3. 构建完成后，可执行文件将位于 `dist` 目录中

## 支持的操作系统

- Windows
- macOS
- Linux

## 注意事项

- 使用本工具前，请确保已关闭 Cursor
- 重置后，Cursor 将被识别为一个新设备
- 原始配置会被备份到 Cursor 配置目录下的 Backups 文件夹中

## 版本历史

- v1.0.0：初始版本

## 许可证

MIT License 