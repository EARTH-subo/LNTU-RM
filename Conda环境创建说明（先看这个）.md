# LuoHuaLabel — Conda 环境创建说明

> 本文档面向习惯使用 **Anaconda / Miniconda** 的用户，详细讲解如何用 Conda 来搭建本项目的运行环境。

***

## 目录

1. [Anaconda 下载与安装](#1-anaconda-下载与安装)
2. [配置 Conda 国内镜像源](#2-配置-conda-国内镜像源)
3. [创建项目专属 Conda 环境](#3-创建项目专属-conda-环境)
4. [安装 PyTorch](#4-安装-pytorch)
5. [安装项目依赖](#5-安装项目依赖)
6. [下载 SAM3 模型权重](#6-下载-sam3-模型权重)
7. [配置模型路径并启动](#7-配置模型路径并启动)
8. [Conda 环境日常管理命令](#8-conda-环境日常管理命令)
9. [常见问题](#9-常见问题)

***

## 1. Anaconda 下载与安装

### 1.1 选择版本

| 发行版 | 特点 | 推荐人群 |
|--------|------|----------|
| **Miniconda**（推荐） | 体积小（约 60MB），仅含 conda + python | 有经验的开发者，按需安装 |
| **Anaconda** | 体积大（约 500MB+），预装 250+ 常用包 | 新手，开箱即用 |

> **推荐 Miniconda**：本项目的依赖包都会通过 `pip` 手动安装，Miniconda 更轻量，安装更快。

### 1.2 下载

- **Miniconda 下载地址**：<https://docs.conda.io/en/latest/miniconda.html>
- **Anaconda 下载地址**：<https://www.anaconda.com/download>

根据你的系统选择 **Windows 64-bit** 版本。

### 1.3 安装步骤（Windows）

1. 双击运行下载的 `.exe` 安装程序
2. 一路点击 **Next**
3. **安装路径**：建议保持默认（如 `C:\Users\你的用户名\miniconda3`），避免路径中出现中文或空格
4. 关键一步 —— **务必勾选**：

   ```
   ☑ Add Miniconda3 to my PATH environment variable
   ```

   > 如果不勾选，安装后需要手动配置环境变量，或通过"开始菜单 → Anaconda Prompt"来使用 conda 命令。

5. 点击 **Install**，等待安装完成

### 1.4 验证安装

安装完成后，按 `Win + R`，输入 `cmd`，回车，输入：

```bash
conda --version
```

如果正常输出版本号（如 `conda 24.1.2`），说明安装成功。

同时确认 conda 自带的 Python：

```bash
python --version
```

（Conda 安装后会自带一个 base 环境中的 Python，版本通常是 3.11 或 3.12）

***

## 2. 配置 Conda 国内镜像源

Conda 默认从国外官方源下载包，速度很慢。建议先换成国内镜像源。

在命令行中依次执行以下命令（二选一）：

### 清华源（推荐）

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

### 中科大源

```bash
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

> 配置后，下载速度会显著提升。

***

## 3. 创建项目专属 Conda 环境

### 3.1 创建环境

打开命令提示符，执行：

```bash
conda create -n luohua python=3.11 -y
```

| 参数 | 含义 |
|------|------|
| `create -n luohua` | 创建名为 `luohua` 的新环境 |
| `python=3.11` | 指定 Python 版本为 3.11（项目测试版本） |
| `-y` | 自动确认，跳过交互提示 |

创建过程大约需要 1-3 分钟，Conda 会自动下载并安装 Python 3.11 及其基础依赖。

### 3.2 激活环境

```bash
conda activate luohua
```

激活成功后，命令行前面会出现 `(luohua)` 标识，例如：

```
(luohua) D:\LuoHuaLabel-main>
```

### 3.3 验证 Python 版本

```bash
python --version
```

应输出 `Python 3.11.x`。

### 3.4 切换到项目目录

```bash
cd D:\LuoHuaLabel-main
```

> 将路径替换为你电脑上项目的实际存放路径。

***

## 4. 安装 PyTorch

PyTorch 需要根据你的显卡类型和 CUDA 版本单独安装。

### 4.1 确认 NVIDIA 显卡与 CUDA 版本

输入：

```bash
nvidia-smi
```

在输出表格的右上角找到 **CUDA Version**（如 `11.8`、`12.1` 等）。

### 4.2 根据 CUDA 版本安装 PyTorch

确保 `(luohua)` 环境已激活，然后根据你的 CUDA 版本选择对应命令：

#### CUDA 11.8

```bash
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 -f https://mirrors.aliyun.com/pytorch-wheels/cu118
```

#### CUDA 12.1

```bash
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 -f https://mirrors.aliyun.com/pytorch-wheels/cu121
```

#### CUDA 12.4 及以上

```bash
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 -f https://mirrors.aliyun.com/pytorch-wheels/cu124
```

#### 无 NVIDIA 显卡（仅 CPU）

```bash
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cpu
```

> ⚠️ CPU 版只能使用手动标注功能，SAM3 智能辅助不可用。

### 4.3 验证 PyTorch 安装

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}')"
```

NVIDIA 显卡用户应看到 `CUDA可用: True`。

***

## 5. 安装项目依赖

确保 `(luohua)` 环境已激活且在项目根目录下，执行：

### 5.1 一次性安装

```bash
pip install -r requirements.txt
```

> 国内用户可使用清华源加速：
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 5.2 如果安装失败

`requirements.txt` 中有一行 `git+https://github.com/facebookresearch/sam3.git`，可能因网络问题失败。可以分步安装：

```bash
pip install pyside6 numpy opencv-python pillow einops pycocotools scipy tqdm iopath matplotlib timm ftfy psutil torchmetrics omegaconf numba huggingface-hub pandas scikit-learn setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install git+https://github.com/facebookresearch/sam3.git
```

如果 sam3 始终无法通过 git 安装，可以手动克隆后本地安装：

```bash
git clone https://github.com/facebookresearch/sam3.git
cd sam3
pip install -e .
cd ..
```

***

## 6. 下载 SAM3 模型权重

### 6.1 下载

从 HuggingFace 下载 `sam3.pt`（约 2GB+）：

🔗 [https://huggingface.co/facebook/sam3/tree/main](https://huggingface.co/facebook/sam3/tree/main/)

### 6.2 放置位置

将下载的 `sam3.pt` 放到项目根目录下：

```
D:\LuoHuaLabel-main\sam3.pt
```

***

## 7. 配置模型路径并启动

### 7.1 修改模型路径

打开项目中的 `main.py`，找到第 53 行：

```python
self.sam_client.load_model_async(r"D:\LuoHuaLabel-main\sam3.pt")  # 模型路径
```

将路径改为你的实际路径。例如：

```python
self.sam_client.load_model_async(r"E:\Models\sam3.pt")
```

> 路径前面的 **`r`** 不能删掉，它表示原始字符串，防止 `\` 被转义。

### 7.2 启动程序

```bash
conda activate luohua
cd D:\LuoHuaLabel-main
python main.py
```

程序启动后，SAM3 模型会在后台加载，状态栏会有相应提示。加载完成后即可使用完整功能。

***

## 8. Conda 环境日常管理命令

以下是常用的 Conda 命令速查：

| 操作 | 命令 |
|------|------|
| 激活环境 | `conda activate luohua` |
| 退出环境 | `conda deactivate` |
| 查看所有环境 | `conda env list` |
| 查看已安装的包 | `conda list` |
| 删除环境 | `conda remove -n luohua --all` |
| 克隆环境 | `conda create -n luohua_backup --clone luohua` |
| 导出环境配置 | `conda env export > environment.yml` |
| 从配置文件创建 | `conda env create -f environment.yml` |
| 更新 conda 自身 | `conda update conda` |

***

## 9. 常见问题

### Q1：`conda` 命令提示"不是内部或外部命令"

**原因**：安装时没有勾选"Add to PATH"。

**解决**：
- 方法一：从开始菜单打开 **Anaconda Prompt (Miniconda3)**，所有 conda 命令在其中执行
- 方法二：手动将 `C:\Users\你的用户名\miniconda3\Scripts` 添加到系统环境变量 PATH 中

### Q2：`conda create` 创建环境时下载很慢

**原因**：没有配置国内镜像源。

**解决**：按照本文第 2 节配置清华源或中科大源。

### Q3：conda 环境中 `pip` 和 `conda` 混用会不会有问题？

**一般不会**。本项目推荐的做法是先创建环境 + `pip install` 安装所有依赖，这是安全的。

> 最佳实践：先用 conda 创建环境（确定 Python 版本），再用 pip 装包。尽量避免用 conda install 和 pip install 交叉安装同一个包的不同版本。

### Q4：如何完全卸载 Anaconda/Miniconda？

```bash
conda install anaconda-clean
anaconda-clean --yes
```

然后通过 Windows "控制面板 → 程序和功能" 卸载即可。

### Q5：Conda 环境和 venv 环境有什么区别？

| 维度 | Conda | venv |
|------|-------|------|
| Python 版本管理 | 可安装任意 Python 版本 | 只能使用系统已有的 Python |
| 非 Python 依赖 | 支持（如 CUDA toolkit） | 不支持 |
| 体积 | 较大 | 轻量 |
| 使用复杂度 | 学习成本中等 | 简单 |
| 跨平台性 | 优秀 | 仅 Python 部分 |

> 两者效果等价，选自己喜欢的即可。本项目原文档推荐 venv，本文档补充 Conda 方案。

***

## 快速启动 Checklist

- [ ] Anaconda / Miniconda 已安装，`conda --version` 正常输出
- [ ] 已配置 conda 国内镜像源
- [ ] 已创建 `luohua` 环境：`conda create -n luohua python=3.11 -y`
- [ ] 已激活环境：`conda activate luohua`
- [ ] PyTorch 已安装，`torch.cuda.is_available()` 为 `True`（NVIDIA 用户）
- [ ] 项目依赖已安装：`pip install -r requirements.txt`
- [ ] `sam3.pt` 模型已下载并放到正确路径
- [ ] `main.py` 第 53 行模型路径已修改

全部确认后：

```bash
conda activate luohua
cd D:\LuoHuaLabel-main
python main.py
```
