# 项目说明

该项目是一个用于监控本地文件夹中新添加的图片文件，并自动通过电子邮件将其发送到指定邮箱的Python脚本。

## 环境要求

- Python 3.x
- pip 包管理器

## 安装依赖

在运行脚本之前，需要安装以下Python库：

- watchdog：用于监控文件系统事件。
  使用以下命令安装：

```bash
pip install watchdog
```

## 设置指南

### 1. 谷歌账号安全设置

由于脚本使用Gmail SMTP服务器发送邮件，需要对谷歌账号进行以下设置：

- **开启两步验证**：
  - 前往谷歌账户的安全设置，启用两步验证。
- **生成应用专用密码（App passwords）**：
  - 搜索谷歌邮箱App passwords，生成一个应用专用密码。
  - 记录生成的16位密码，稍后将在脚本中使用。

**注意**：如果未开启两步验证，将无法生成应用专用密码。

### 2. 修改脚本配置

在脚本中，找到以下部分并进行修改：

```python
# 配置邮件发送信息
# 发送者邮箱（建议使用谷歌邮箱）
EMAIL_ADDRESS = '你的谷歌邮箱地址'
# 发送者邮箱的应用专用密码
EMAIL_PASSWORD = '你的应用专用密码'

# 配置接收者邮箱
TO_ADDRESS = '接收者的邮箱地址'

# 监控的本地文件夹路径（注意路径格式，Windows使用反斜杠\\，Linux使用正斜杠/）
path = '你要监控的本地文件夹路径'
```

请确保：
- 使用有效的谷歌邮箱地址和应用专用密码。
- 接收者邮箱地址正确无误。
- 监控的文件夹路径存在且具有访问权限。

### 注意事项

- **不要在虚拟机环境下运行**：由于虚拟机可能无法正确检测到文件变化，建议在物理机上运行脚本。
- **SMTP服务器信息**：脚本使用Gmail的SMTP服务器，服务器地址为smtp.gmail.com，端口为587。

### 运行脚本

在完成上述配置和依赖安装后，可以通过以下命令运行脚本：

```bash
python your_script_name.py
```

替换 `your_script_name.py` 为你的脚本文件名。

运行后，脚本将开始监控指定的文件夹：

```plaintext
开始监控 your_folder_path 文件夹...
```

当有新图片创建时，脚本将：
- 检测到新图片并输出提示：
  - `检测到新文件：xxxx`
- 通过邮件将新图片作为附件发送到指定的接收者邮箱。
  - `已发送 file_name 到 recipient_email`
