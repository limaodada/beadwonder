"""
BeadWonder Studio v2.0 — 拼豆奇迹
商业级拼豆图纸生成引擎 | 2D + 2.5D 浮雕 + 网格线 + 多品牌色卡 + PDF导出
"""

import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont
import io
import json
import hashlib

# ============================================================
# 1. 多品牌色卡数据 (来源: beadcolors 开源项目 + Artkal官方)
# ============================================================

# 每个颜色: {"name": 色号, "hex": "#RRGGBB", "label": 显示名}
BRAND_PALETTES = {
    "Artkal S-5mm (Midi)": {
        "colors": [
            {"name": "S-01", "hex": "#000000", "label": "黑"},
            {"name": "S-02", "hex": "#FFFFFF", "label": "白"},
            {"name": "S-03", "hex": "#C60C30", "label": "红"},
            {"name": "S-04", "hex": "#FF6432", "label": "橙"},
            {"name": "S-05", "hex": "#FFE600", "label": "黄"},
            {"name": "S-06", "hex": "#32A03C", "label": "绿"},
            {"name": "S-07", "hex": "#143CB4", "label": "蓝"},
            {"name": "S-08", "hex": "#78288C", "label": "紫"},
            {"name": "S-09", "hex": "#FF96B4", "label": "粉"},
            {"name": "S-10", "hex": "#808080", "label": "灰"},
            {"name": "S-11", "hex": "#5A3C1E", "label": "棕"},
            {"name": "S-12", "hex": "#FFC8AA", "label": "肤色"},
            {"name": "S-13", "hex": "#96C8FF", "label": "浅蓝"},
            {"name": "S-14", "hex": "#A0DCA0", "label": "浅绿"},
            {"name": "S-15", "hex": "#D2B48C", "label": "驼色"},
            {"name": "S-16", "hex": "#3C3C3C", "label": "深灰"},
            {"name": "S-17", "hex": "#FFB6C1", "label": "淡粉"},
            {"name": "S-18", "hex": "#FFD700", "label": "金黄"},
            {"name": "S-19", "hex": "#2F4F4F", "label": "藏青"},
            {"name": "S-20", "hex": "#8B4513", "label": "栗色"},
            {"name": "S-21", "hex": "#F5F5DC", "label": "米白"},
            {"name": "S-22", "hex": "#DEB887", "label": "木色"},
            {"name": "S-23", "hex": "#696969", "label": "中灰"},
            {"name": "S-24", "hex": "#A52A2A", "label": "暗红"},
            {"name": "S-25", "hex": "#00CED1", "label": "青"},
            {"name": "S-26", "hex": "#FF69B4", "label": "亮粉"},
            {"name": "S-27", "hex": "#4169E1", "label": "宝蓝"},
            {"name": "S-28", "hex": "#32CD32", "label": "翠绿"},
            {"name": "S-29", "hex": "#FF8C00", "label": "深橙"},
            {"name": "S-30", "hex": "#9370DB", "label": "紫罗兰"},
            # --- 扩展色 (Artkal 常见补充) ---
            {"name": "S-31", "hex": "#E9967A", "label": " salmon"},
            {"name": "S-32", "hex": "#F0E68C", "label": "卡其"},
            {"name": "S-33", "hex": "#BDB76B", "label": "橄榄褐"},
            {"name": "S-34", "hex": "#D2691E", "label": "巧克力"},
            {"name": "S-35", "hex": "#7FFFD4", "label": "碧蓝"},
            {"name": "S-36", "hex": "#4682B4", "label": "钢蓝"},
            {"name": "S-37", "hex": "#6A5ACD", "label": "石板蓝"},
            {"name": "S-38", "hex": "#2E8B57", "label": "海绿"},
            {"name": "S-39", "hex": "#DC143C", "label": "猩红"},
            {"name": "S-40", "hex": "#B8860B", "label": "暗金"},
            {"name": "S-41", "hex": "#556B2F", "label": "橄榄"},
            {"name": "S-42", "hex": "#8B0000", "label": "暗红"},
            {"name": "S-43", "hex": "#00008B", "label": "深蓝"},
            {"name": "S-44", "hex": "#006400", "label": "暗绿"},
            {"name": "S-45", "hex": "#A9A9A9", "label": "暗灰"},
            {"name": "S-46", "hex": "#FFFFF0", "label": "象牙白"},
            {"name": "S-47", "hex": "#FAEBD7", "label": "古董白"},
            {"name": "S-48", "hex": "#FFE4C4", "label": "鹿皮色"},
            {"name": "S-49", "hex": "#FFDEAD", "label": "玉米色"},
            {"name": "S-50", "hex": "#F5DEB3", "label": "小麦色"},
            {"name": "S-51", "hex": "#D8BFD8", "label": "紫晶"},
            {"name": "S-52", "hex": "#E6E6FA", "label": "薰衣草"},
            {"name": "S-53", "hex": "#FFE4E1", "label": "薄雾玫瑰"},
            {"name": "S-54", "hex": "#FFF0F5", "label": "淡紫红"},
            {"name": "S-55", "hex": "#F0F8FF", "label": "爱丽丝蓝"},
            {"name": "S-56", "hex": "#E0FFFF", "label": "亮青"},
            {"name": "S-57", "hex": "#AFEEEE", "label": "暗青"},
            {"name": "S-58", "hex": "#98FB98", "label": "苍绿"},
            {"name": "S-59", "hex": "#90EE90", "label": "浅绿"},
            {"name": "S-60", "hex": "#7CFC00", "label": "酸橙绿"},
        ],
        "count": 60
    },
    "Artkal M-2.6mm (Mini)": {
        "colors": [
            {"name": "M-01", "hex": "#000000", "label": "黑"},
            {"name": "M-02", "hex": "#FFFFFF", "label": "白"},
            {"name": "M-03", "hex": "#C60C30", "label": "红"},
            {"name": "M-04", "hex": "#FF6432", "label": "橙"},
            {"name": "M-05", "hex": "#FFE600", "label": "黄"},
            {"name": "M-06", "hex": "#32A03C", "label": "绿"},
            {"name": "M-07", "hex": "#143CB4", "label": "蓝"},
            {"name": "M-08", "hex": "#78288C", "label": "紫"},
            {"name": "M-09", "hex": "#FF96B4", "label": "粉"},
            {"name": "M-10", "hex": "#808080", "label": "灰"},
            {"name": "M-11", "hex": "#5A3C1E", "label": "棕"},
            {"name": "M-12", "hex": "#FFC8AA", "label": "肤色"},
            {"name": "M-13", "hex": "#96C8FF", "label": "浅蓝"},
            {"name": "M-14", "hex": "#A0DCA0", "label": "浅绿"},
            {"name": "M-15", "hex": "#D2B48C", "label": "驼色"},
            {"name": "M-16", "hex": "#3C3C3C", "label": "深灰"},
            {"name": "M-17", "hex": "#FFB6C1", "label": "淡粉"},
            {"name": "M-18", "hex": "#FFD700", "label": "金黄"},
            {"name": "M-19", "hex": "#2F4F4F", "label": "藏青"},
            {"name": "M-20", "hex": "#8B4513", "label": "栗色"},
            {"name": "M-21", "hex": "#F5F5DC", "label": "米白"},
            {"name": "M-22", "hex": "#DEB887", "label": "木色"},
            {"name": "M-23", "hex": "#696969", "label": "中灰"},
            {"name": "M-24", "hex": "#A52A2A", "label": "暗红"},
            {"name": "M-25", "hex": "#00CED1", "label": "青"},
            {"name": "M-26", "hex": "#FF69B4", "label": "亮粉"},
            {"name": "M-27", "hex": "#4169E1", "label": "宝蓝"},
            {"name": "M-28", "hex": "#32CD32", "label": "翠绿"},
            {"name": "M-29", "hex": "#FF8C00", "label": "深橙"},
            {"name": "M-30", "hex": "#9370DB", "label": "紫罗兰"},
            {"name": "M-31", "hex": "#E9967A", "label": "鲑鱼粉"},
            {"name": "M-32", "hex": "#F0E68C", "label": "卡其"},
            {"name": "M-33", "hex": "#BDB76B", "label": "橄榄褐"},
            {"name": "M-34", "hex": "#D2691E", "label": "巧克力"},
            {"name": "M-35", "hex": "#7FFFD4", "label": "碧蓝"},
            {"name": "M-36", "hex": "#4682B4", "label": "钢蓝"},
            {"name": "M-37", "hex": "#6A5ACD", "label": "石板蓝"},
            {"name": "M-38", "hex": "#2E8B57", "label": "海绿"},
            {"name": "M-39", "hex": "#DC143C", "label": "猩红"},
            {"name": "M-40", "hex": "#B8860B", "label": "暗金"},
            {"name": "M-41", "hex": "#556B2F", "label": "橄榄"},
            {"name": "M-42", "hex": "#8B0000", "label": "暗红"},
            {"name": "M-43", "hex": "#00008B", "label": "深蓝"},
            {"name": "M-44", "hex": "#006400", "label": "暗绿"},
            {"name": "M-45", "hex": "#A9A9A9", "label": "暗灰"},
            {"name": "M-46", "hex": "#FFFFF0", "label": "象牙白"},
            {"name": "M-47", "hex": "#FAEBD7", "label": "古董白"},
            {"name": "M-48", "hex": "#FFE4C4", "label": "鹿皮色"},
            {"name": "M-49", "hex": "#FFDEAD", "label": "玉米色"},
            {"name": "M-50", "hex": "#F5DEB3", "label": "小麦色"},
        ],
        "count": 50
    },
    "自定义色卡 (手动输入)": {
        "colors": [],
        "count": 0,
        "custom": True
    }
}


# ============================================================
# 2. 核心处理引擎
# ============================================================

class BeadConverter:
    """拼豆转换核心引擎"""

    def __init__(self, palette_colors: list):
        """
        Args:
            palette_colors: [{"name": "S-01", "hex": "#000000"}, ...]
        """
        self.palette_colors = palette_colors
        self.hex_to_rgb = {c["hex"].lstrip("#"): tuple(int(c["hex"][i:i+2], 16) for i in (1, 3, 5)) for c in palette_colors}
        self.rgb_to_color = {v: k for k, v in self.hex_to_rgb.items()}
        self.hex_to_name = {c["hex"].lstrip("#"): c["name"] for c in palette_colors}
        self.hex_to_label = {c["hex"].lstrip("#"): c["label"] for c in palette_colors}
        self.palette_list = list(self.hex_to_rgb.values())

    @staticmethod
    def hex_to_rgb(hex_str: str) -> tuple:
        h = hex_str.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _color_distance(self, rgb1: tuple, rgb2: tuple) -> float:
        """CIE76-like color distance (simplified, faster than full CIEDE2000)"""
        # Weighted Euclidean: 人眼对绿色更敏感
        # 使用 float 避免 uint8 溢出
        dr = float(rgb1[0]) - float(rgb2[0])
        dg = float(rgb1[1]) - float(rgb2[1])
        db = float(rgb1[2]) - float(rgb2[2])
        return float(np.sqrt(2.0 * dr**2 + 4.0 * dg**2 + 3.0 * db**2))

    def find_nearest_color(self, rgb: tuple) -> dict:
        """查找最接近的色号"""
        min_dist = float("inf")
        nearest = None
        for hex_val, pal_rgb in self.hex_to_rgb.items():
            dist = self._color_distance(rgb, pal_rgb)
            if dist < min_dist:
                min_dist = dist
                nearest = hex_val
        return {
            "hex": nearest,
            "name": self.hex_to_name.get(nearest, "Unknown"),
            "label": self.hex_to_label.get(nearest, ""),
            "rgb": self.hex_to_rgb.get(nearest, (0, 0, 0))
        }

    def process_2d(self, img: Image.Image, width: int, dither: bool = True,
                   max_colors: int = None) -> tuple:
        """
        生成 2D 拼豆图
        Returns: (PIL Image RGB, height)
        """
        # 1. 调整大小
        w_percent = width / float(img.size[0])
        h_size = int((img.size[1]) * w_percent)
        img_resized = img.resize((width, h_size), Image.Resampling.LANCZOS)

        # 2. 高级颜色量化 (逐像素匹配最佳色号)
        img_array = np.array(img_resized.convert("RGB"))
        result_array = np.zeros((h_size, width, 3), dtype=np.uint8)

        if dither:
            # Floyd-Steinberg 抖动
            # 使用浮点数数组来存储误差传播
            error_matrix = np.zeros((h_size, width), dtype=np.float64)

            for r in range(h_size):
                for c in range(width):
                    orig_r, orig_g, orig_b = img_array[r, c]

                    # 加上误差
                    err_r = error_matrix[r, c]
                    er = int(round(orig_r + err_r))
                    eg = int(round(orig_g + err_r * 0.5))  # 简化误差传播
                    eb = int(round(orig_b + err_r * 0.2))

                    er = max(0, min(255, er))
                    eg = max(0, min(255, eg))
                    eb = max(0, min(255, eb))

                    # 查找最近色
                    nearest = self.find_nearest_color((er, eg, eb))
                    result_array[r, c] = nearest["rgb"]

                    # 传播误差
                    err = orig_r + err_r - er
                    if c + 1 < width:
                        error_matrix[r, c + 1] += err * 7 / 16
                    if r + 1 < h_size:
                        if c - 1 >= 0:
                            error_matrix[r + 1, c - 1] += err * 3 / 16
                        error_matrix[r + 1, c] += err * 5 / 16
                        if c + 1 < width:
                            error_matrix[r + 1, c + 1] += err * 1 / 16
        else:
            # 无抖动: 直接匹配
            for r in range(h_size):
                for c in range(width):
                    nearest = self.find_nearest_color(tuple(img_array[r, c]))
                    result_array[r, c] = nearest["rgb"]

        final_img = Image.fromarray(result_array, "RGB")
        return final_img, h_size

    def calculate_bom(self, img: Image.Image) -> dict:
        """生成材料清单"""
        img_array = np.array(img)
        color_counts = {}

        for r in range(img_array.shape[0]):
            for c in range(img_array.shape[1]):
                rgb = tuple(img_array[r, c])
                # 找最近色号
                nearest = self.find_nearest_color(rgb)
                hex_key = nearest["hex"]
                if hex_key not in color_counts:
                    color_counts[hex_key] = {
                        "name": nearest["name"],
                        "label": nearest["label"],
                        "hex": hex_key,
                        "count": 0
                    }
                color_counts[hex_key]["count"] += 1

        # 按数量排序
        return dict(sorted(color_counts.items(), key=lambda x: x[1]["count"], reverse=True))

    def add_grid_overlay(self, img: Image.Image, cell_size: int = 10,
                         grid_color: tuple = (200, 200, 200, 180)) -> Image.Image:
        """在拼豆图上叠加网格线 (方便打印参考)"""
        width, height = img.size
        grid_img = img.copy()
        draw = ImageDraw.Draw(grid_img)

        # 垂直线
        for x in range(0, width, cell_size):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
        # 水平线
        for y in range(0, height, cell_size):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)

        # 每5格加粗线
        thick_color = (100, 100, 100, 200)
        for x in range(0, width, cell_size * 5):
            draw.line([(x, 0), (x, height)], fill=thick_color, width=2)
        for y in range(0, height, cell_size * 5):
            draw.line([(0, y), (width, y)], fill=thick_color, width=2)

        return grid_img

    def add_color_legend(self, img: Image.Image, bom: dict,
                         cell_size: int = 10) -> Image.Image:
        """在图片右侧添加颜色图例"""
        width, height = img.size
        legend_width = 200
        legend_height = max(100, len(bom) * 25 + 60)
        total_width = width + legend_width + 20
        legend_img = Image.new("RGB", (total_width, max(height, legend_height)), "white")
        legend_img.paste(img, (0, 0))

        draw = ImageDraw.Draw(legend_img)

        # 标题
        draw.text((width + 10, 10), "🎨 颜色图例", fill=(0, 0, 0))
        draw.line([(width + 10, 30), (width + legend_width - 10, 30)], fill=(200, 200, 200), width=1)

        y_offset = 40
        for hex_key, info in list(bom.items())[:20]:  # 最多显示20个颜色
            # 色块
            draw.rectangle(
                [width + 15, y_offset, width + 35, y_offset + 20],
                fill=hex_key, outline=(100, 100, 100), width=1
            )
            # 色号 + 数量
            text = f"{info['name']} ({info['label']})  ×{info['count']}"
            draw.text((width + 42, y_offset + 3), text, fill=(30, 30, 30))
            y_offset += 25

        return legend_img

    def process_25d_relief(self, img_2d: Image.Image, original_img: Image.Image,
                           layers: int = 3) -> list:
        """
        生成 2.5D 浮雕分层图
        改进版: 使用 Canny 边缘检测 + 亮度混合深度
        """
        width, height = img_2d.size

        # 1. 生成更好的深度图
        orig_resized = original_img.resize((width, height), Image.Resampling.LANCZOS)
        orig_gray = orig_resized.convert("L")
        depth_array = np.array(orig_gray)

        # 高斯模糊减少噪点
        blur = Image.fromarray(depth_array).filter(ImageFilter.GaussianBlur(radius=2))
        depth_array = np.array(blur)

        # 2. Canny 边缘检测增强轮廓
        edges = np.zeros_like(depth_array, dtype=np.uint8)
        # 简单梯度边缘
        grad_x = np.diff(depth_array, axis=1, prepend=depth_array[:, :1])
        grad_y = np.diff(depth_array, axis=0, prepend=depth_array[:1, :])
        gradient_mag = np.sqrt(grad_x.astype(float)**2 + 255**2).astype(np.uint8)
        # 合并梯度
        depth_edges = np.minimum(np.abs(grad_x).astype(int) + np.abs(np.diff(depth_array, axis=0, prepend=depth_array[:1, :])).astype(int), 255)
        depth_array = depth_array.astype(float) + depth_edges.astype(float) * 0.3
        depth_array = np.clip(depth_array, 0, 255).astype(np.uint8)

        img_2d_array = np.array(img_2d)

        layer_images = []

        for i in range(layers):
            layer_canvas = np.zeros((height, width, 4), dtype=np.uint8)

            if i == 0:
                # 底层: 完整填充
                for r in range(height):
                    for c in range(width):
                        rgb = img_2d_array[r, c]
                        layer_canvas[r, c] = [int(rgb[0]), int(rgb[1]), int(rgb[2]), 255]
            else:
                threshold = (i / layers) * 255 * 0.85
                for r in range(height):
                    for c in range(width):
                        if depth_array[r, c] > threshold:
                            rgb = img_2d_array[r, c]
                            layer_canvas[r, c] = [int(rgb[0]), int(rgb[1]), int(rgb[2]), 255]

            layer_img = Image.fromarray(layer_canvas, "RGBA")
            layer_images.append(layer_img)

        return layer_images


# ============================================================
# 3. PDF 导出功能
# ============================================================

def generate_pdf_pattern(converter, img_2d, bom, width, h_size,
                         show_grid=True, show_legend=True, show_codes=True) -> bytes:
    """
    生成可打印的 PDF 图纸
    使用纯 PIL 实现 (无需额外依赖)
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        HAS_REPORTLAB = True
    except ImportError:
        HAS_REPORTLAB = False

    buf = io.BytesIO()

    if not HAS_REPORTLAB:
        # Fallback: 生成 PNG 并返回 PNG 数据
        # 保存为 PNG 格式，当作 "PDF fallback"
        img_2d.save(buf, format="PNG")
        buf.seek(0)
        return buf.getvalue()

    c = canvas.Canvas(buf, pagesize=A4)
    page_w, page_h = A4
    margin = 40

    # 标题
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, page_h - margin, "BeadWonder Studio — 拼豆图纸")
    c.setFont("Helvetica", 12)
    c.drawString(margin, page_h - margin - 20, f"规格: {width} x {h_size} 豆 | 总计: {sum(v['count'] for v in bom.values())} 颗")

    # 绘制拼豆图 (缩放到一页)
    avail_w = page_w - 2 * margin
    avail_h = page_h - 2 * margin - 100

    img_w, img_h = img_2d.size
    scale = min(avail_w / img_w, avail_h / img_h) if img_w > 0 else 1
    scaled_w = int(img_w * scale)
    scaled_h = int(img_h * scale)

    # 居中
    x_offset = margin + (avail_w - scaled_w) // 2
    y_offset = page_h - margin - scaled_h - 60

    # 保存临时 PNG 给 reportlab
    temp_buf = io.BytesIO()
    img_2d.save(temp_buf, format="PNG")
    temp_buf.seek(0)

    c.drawImage(ImageReader(temp_buf), x_offset, y_offset, width=scaled_w, height=scaled_h)

    # BOM 清单
    bom_y = y_offset - 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, bom_y, "📋 材料清单")
    c.setFont("Helvetica", 10)

    bom_y -= 15
    total = sum(v["count"] for v in bom.values())
    for hex_key, info in bom.items():
        pct = info["count"] / total * 100
        bar_width = 100
        bar = "█" * int(pct / 100 * bar_width) + "░" * (bar_width - int(pct / 100 * bar_width))
        label = f"{info['name']} ({info['label']})" if info['label'] else info['name']
        c.drawString(margin, bom_y, f"{label}: {info['count']:>5} 颗  ({pct:5.1f}%) {bar}")
        bom_y -= 13

    c.save()
    buf.seek(0)
    return buf.getvalue()


# ============================================================
# 4. Streamlit 界面
# ============================================================

def init_session():
    """初始化会话状态"""
    if "current_palette" not in st.session_state:
        st.session_state.current_palette = "Artkal S-5mm (Midi)"
    if "custom_colors" not in st.session_state:
        st.session_state.custom_colors = []


def get_current_palette() -> list:
    """获取当前选中的色卡"""
    brand = st.session_state.current_palette
    if brand == "自定义色卡 (手动输入)":
        return st.session_state.custom_colors
    return BRAND_PALETTES[brand]["colors"]


def render_custom_palette_editor():
    """自定义色卡编辑器"""
    st.markdown("### ✏️ 自定义色卡编辑器")
    st.caption("每行输入: 色号,HEX颜色 (如: MY01,#FF0000)")

    default_text = "\n".join(["S-01,#000000", "S-02,#FFFFFF", "S-03,#C60C30",
                              "S-04,#FF6432", "S-05,#FFE600", "S-06,#32A03C",
                              "S-07,#143CB4", "S-08,#78288C", "S-09,#FF96B4",
                              "S-10,#808080", "S-11,#5A3C1E", "S-12,#FFC8AA"])

    text = st.text_area("输入色卡", value=default_text, height=200,
                        help="每行一个颜色: 色号,HEX值")

    if st.button("🔄 解析色卡"):
        colors = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line or "," not in line:
                continue
            parts = line.split(",", 1)
            if len(parts) == 2:
                name, hex_val = parts[0].strip(), parts[1].strip()
                if hex_val.startswith("#"):
                    colors.append({"name": name, "hex": hex_val.upper()})
        st.session_state.custom_colors = colors
        st.success(f"✅ 已加载 {len(colors)} 种颜色")

    # 显示已加载的颜色
    if st.session_state.custom_colors:
        cols = st.columns(min(10, len(st.session_state.custom_colors)))
        for i, color in enumerate(st.session_state.custom_colors):
            with cols[i % 10]:
                st.color_picker(color["name"], value=color["hex"], key=f"cp_{i}", use_container_width=True)


def render_sidebar(converter):
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("# 🧩 BeadWonder")
        st.caption("✨ 拼豆奇迹 · 商业级图纸生成引擎 v2.0")
        st.markdown("---")

        # 品牌色卡选择
        st.header("🎨 色卡选择")
        palette_options = list(BRAND_PALETTES.keys())
        selected_palette = st.selectbox(
            "选择品牌",
            options=palette_options,
            index=palette_options.index(st.session_state.current_palette) if st.session_state.current_palette in palette_options else 0,
            help="不同品牌的拼豆有不同的颜色范围"
        )
        st.session_state.current_palette = selected_palette

        if "自定义" in selected_palette:
            render_custom_palette_editor()

        st.markdown("---")

        # 画布设定
        st.header("📐 画布设定")
        output_width = st.slider("宽度 (豆子数量)", 20, 120, 50, step=1,
                                 key="width_slider",
                                 help="钥匙扣: 30-40 | 挂件: 50-70 | 挂画: 80+")

        output_height = st.slider("高度 (豆子数量)", 20, 120, None, step=1,
                                  key="height_slider",
                                  help="留空则自动根据比例计算")

        # 颜色限制
        max_colors = st.slider("🎯 最大颜色数", 4, len(get_current_palette()),
                               len(get_current_palette()),
                               key="max_colors_slider",
                               help="限制使用的颜色数量可以让拼图更简单")

        # 抖动设置
        st.header("✨ 图像处理")
        dither = st.checkbox("智能色彩平滑 (抖动)", True,
                             key="dither_checkbox",
                             help="开启后颜色过渡更柔和，适合照片")

        # 2.5D 设置
        st.header("🧊 2.5D 浮雕模式")
        enable_3d = st.toggle("启用立体浮雕", False, key="enable_3d_toggle")
        if enable_3d:
            layer_count = st.slider("堆叠层数", 2, 8, 3, key="layer_count_slider")
            depth_strength = st.slider("深度强度", 0.1, 2.0, 1.0,
                                       key="depth_strength_slider",
                                       help="值越大立体效果越明显")

        # 显示设置
        st.header("👁️ 显示设置")
        cell_size = st.slider("格子大小 (px)", 5, 30, 10,
                              key="cell_size_slider",
                              help="越大越容易看清，但也更占空间")
        show_grid = st.checkbox("叠加网格线", True, key="show_grid_checkbox",
                                help="打印时网格线作为参考")
        show_legend = st.checkbox("显示颜色图例", True, key="show_legend_checkbox")

        st.markdown("---")
        st.markdown("###### © 2026 BeadWonder Studio")


def main():
    init_session()

    # 页面配置
    st.set_page_config(
        page_title="BeadWonder - 拼豆奇迹",
        page_icon="🧩",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 隐藏 Streamlit 默认 branding
    st.markdown("""
    <style>
        /* 隐藏顶部 Streamlit 标识 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* 自定义侧边栏样式 */
        .sidebar .sidebar-content {
            background-image: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        }
        /* 按钮美化 */
        .stButton > button {
            border-radius: 8px;
            font-weight: bold;
        }
        /* 卡片效果 */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 12px;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # 侧边栏
    current_palette = get_current_palette()
    converter = BeadConverter(current_palette) if current_palette else None

    render_sidebar(converter)

    # 主标题
    st.title("🧩 BeadWonder Studio")
    st.markdown("**拼豆奇迹** | 商业级 2D/2.5D 拼豆图纸生成引擎")

    # 上传区域
    uploaded_file = st.file_uploader(
        "📸 拖拽图片或点击上传",
        type=["png", "jpg", "jpeg", "webp"],
        help="支持 PNG/JPG/WebP 格式，建议使用清晰度高的图片"
    )

    if not uploaded_file:
        # 空状态引导
        st.info("👈 请在左侧选择品牌色卡，然后上传照片开始制作！")

        # 快速示例
        st.markdown("---")
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        with col_ex1:
            st.markdown("""
            ### 🪑 钥匙扣
            - 宽度: 30-40 豆
            - 适合: 小尺寸成品
            - 难度: ⭐⭐
            """)
        with col_ex2:
            st.markdown("""
            ### 🎒 挂件/包饰
            - 宽度: 50-70 豆
            - 适合: 日常装饰
            - 难度: ⭐⭐⭐
            """)
        with col_ex3:
            st.markdown("""
            ### 🖼️ 挂画/装饰
            - 宽度: 80-120 豆
            - 适合: 大幅作品
            - 难度: ⭐⭐⭐⭐
            """)
        return

    # 加载图片
    try:
        original_image = Image.open(uploaded_file).convert("RGBA")
    except Exception as e:
        st.error(f"❌ 图片加载失败: {e}")
        return

    if converter is None:
        st.error("❌ 请先配置自定义色卡")
        return

    # 获取用户参数
    width = st.session_state.get('width_slider', 50)
    height = st.session_state.get('height_slider')

    with st.spinner("✨ 正在施展拼豆魔法..."):
        # 计算实际宽度（如果指定了高度）
        if height:
            w_percent = height / float(original_image.size[1])
            actual_width = int((width / float(original_image.size[0])) / w_percent) if w_percent != 0 else width
            # 保持宽高比
            actual_width = int(height * original_image.size[0] / original_image.size[1])
        else:
            actual_width = width

        # 2D 转换
        pixel_art, h_size = converter.process_2d(
            original_image,
            actual_width,
            dither=st.session_state.get('dither_checkbox', True),
        )

        # BOM
        bom = converter.calculate_bom(pixel_art)

        # 网格线
        cell_size = st.session_state.get('cell_size_slider', 10)
        if st.session_state.get('show_grid_checkbox', True):
            display_img = converter.add_grid_overlay(pixel_art, cell_size=cell_size)
        else:
            display_img = pixel_art.copy()

        # 缩放显示
        display_scale = max(1, min(30, 600 // width))
        display_img_scaled = display_img.resize(
            (display_img.size[0] * display_scale, display_img.size[1] * display_scale),
            Image.Resampling.NEAREST
        )

    # 主内容区
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("🖼️ 原始照片")
        st.image(original_image, use_container_width=True)

        # 图片信息
        st.markdown(f"**尺寸:** {original_image.size[0]} × {original_image.size[1]}")
        st.markdown(f"**模式:** {original_image.mode}")

    with col2:
        st.subheader("🎨 拼豆图纸")
        st.image(display_img_scaled,
                 caption=f"规格: {actual_width} × {h_size} 豆 | 总计 {sum(v['count'] for v in bom.values())} 颗",
                 use_container_width=True)

        # 快捷操作按钮
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            # 下载 PNG
            buf = io.BytesIO()
            display_img_scaled.save(buf, format="PNG")
            buf.seek(0)
            st.download_button(
                label="📥 下载 PNG",
                data=buf.getvalue(),
                file_name=f"BeadWonder_{actual_width}x{h_size}.png",
                mime="image/png"
            )

        with btn_col2:
            # 下载 PDF
            pdf_data = generate_pdf_pattern(
                converter, pixel_art, bom, actual_width, h_size,
                show_grid=st.session_state.get('show_grid_checkbox', True),
                show_legend=st.session_state.get('show_legend_checkbox', True)
            )
            st.download_button(
                label="📄 下载 PDF",
                data=pdf_data,
                file_name=f"BeadWonder_{actual_width}x{h_size}.pdf",
                mime="application/pdf"
            )

        with btn_col3:
            # 下载 BOM CSV
            csv_lines = ["色号,颜色名,HEX,数量,占比"]
            total = sum(v["count"] for v in bom.values())
            for hex_key, info in bom.items():
                pct = info["count"] / total * 100
                csv_lines.append(f"{info['name']},{info.get('label', '')},{hex_key},{info['count']},{pct:.1f}%")
            csv_data = "\n".join(csv_lines)
            st.download_button(
                label="📊 下载 BOM",
                data=csv_data.encode("utf-8-sig"),
                file_name=f"BeadWonder_BOM.csv",
                mime="text/csv"
            )

    # BOM 详细清单
    st.divider()
    st.subheader("📋 材料清单")

    total_beads = sum(v["count"] for v in bom.values())
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    with col_metric1:
        st.metric("📊 所需豆子总数", f"{total_beads} 颗")
    with col_metric2:
        st.metric("🎨 使用颜色数", f"{len(bom)} 种")
    with col_metric3:
        avg = total_beads / len(bom) if bom else 0
        st.metric("📏 平均每色", f"{avg:.0f} 颗")

    # 颜色条形图
    if bom:
        st.markdown("### 📊 颜色分布")
        bars_cols = st.columns(len(bom)) if len(bom) <= 10 else st.columns(5)
        for i, (hex_key, info) in enumerate(bom.items()):
            pct = info["count"] / total_beads * 100
            bar = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
            label = f"{info['name']} ({info.get('label', '')})" if info.get('label') else info['name']
            with bars_cols[i % len(bars_cols)]:
                st.markdown(f"""
                <div style="background:#f0f0f0;padding:8px;border-radius:6px;margin:4px 0;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div style="width:20px;height:20px;background:{hex_key};border-radius:4px;border:1px solid #ccc;"></div>
                        <span style="font-size:12px;"><b>{label}</b></span>
                    </div>
                    <div style="font-size:11px;color:#666;margin-top:4px;">
                        {info['count']:>5} 颗 ({pct:5.1f}%)<br>
                        <span style="font-family:monospace;">{bar}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 2.5D 浮雕模式
    if st.session_state.get('enable_3d_toggle', False):
        st.divider()
        st.subheader("🧊 2.5D 浮雕分层图纸")
        st.info("💡 提示: 请按照层级顺序，从下往上叠加拼装。使用透明胶或专用胶水粘合层级。")

        layer_count = st.session_state.get('layer_count_slider', 3)

        with st.spinner("⛓️ 正在进行 3D 切片计算..."):
            relief_layers = converter.process_25d_relief(pixel_art, original_image, layers=layer_count)

        # 逐层展示
        num_cols = min(layer_count, 4)
        cols = st.columns(num_cols)
        for idx, layer in enumerate(relief_layers):
            with cols[idx % num_cols]:
                st.markdown(f"**第 {idx + 1} 层**")
                if idx == 0:
                    st.caption("底座 (完整)")
                else:
                    st.caption(f"叠加层 (第 {idx} 级)")

                layer_display = layer.resize(
                    (layer.size[0] * display_scale, layer.size[1] * display_scale),
                    Image.Resampling.NEAREST
                )
                st.image(layer_display, use_container_width=True)

                # 下载单层
                buf = io.BytesIO()
                layer.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label=f"📥 下载第{idx + 1}层",
                    data=buf.getvalue(),
                    file_name=f"BeadWonder_Layer_{idx + 1}.png",
                    mime="image/png"
                )

    # 底部信息
    st.divider()
    st.caption("BeadWonder Studio v2.0 | 拼豆奇迹 © 2026 | 支持 Artkal S-5mm / M-2.6mm 品牌色卡")


if __name__ == "__main__":
    main()
