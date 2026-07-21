# BeadWonder Studio — 拼豆奇迹

> 🧩 商业级 2D/2.5D 拼豆图纸生成引擎
> 把照片变成拼豆图纸，支持 Artkal 品牌 60+ 色

## ✨ 功能特性

- 🎨 **60色 Artkal 色卡** — 覆盖日常95%拼豆需求
- 🧊 **2.5D 浮雕模式** — 独家多层叠加立体图纸（市面唯一！）
- 📐 **网格线叠加** — 打印即可当拼图参考
- 📄 **PDF图纸导出** — 专业打印格式
- 📊 **CSV材料清单** — 采购统计一目了然
- 🎯 **智能色彩平滑** — Floyd-Steinberg 抖动算法
- ✏️ **自定义色卡** — 手动输入HEX值扩展色卡

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app_v2.py
```

## 📦 部署

### Streamlit Community Cloud (推荐)
1. 推送到 GitHub
2. 前往 https://streamlit.io/cloud
3. 连接 repo → 选择 `app_v2.py` → Deploy

### HuggingFace Spaces
```bash
# 使用 Docker
docker build -t beadwonder .
docker run -p 7860:7860 beadwonder
```

## 📝 License

Apache 2.0
