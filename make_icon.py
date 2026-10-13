import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer


def svg_to_png(svg_path: Path, png_path: Path, size: int = 512):
    renderer = QSvgRenderer(str(svg_path))
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    renderer.render(painter)
    painter.end()

    image.save(str(png_path), "PNG")
    print(f"✓ {png_path.name}")


def main():
    app = QGuiApplication(sys.argv)   # لازمه برای QImage/QPainter

    assets = Path(__file__).parent / "assets"
    svg_path = assets / "app_icon.svg"

    if not svg_path.exists():
        print(f"✗ {svg_path} not found")
        return

    # SVG → PNG (512×512)
    svg_to_png(svg_path, assets / "app_icon.png", size=512)

    # PNG → ICO (بدون Pillow، مستقیم با Qt)
    from PySide6.QtGui import QIcon
    icon = QIcon(str(assets / "app_icon.png"))

    # Qt می‌تونه ICO رو با چند تا سایز ذخیره کنه اگه PNG همراهش باشه،
    # ولی برای ویندوز ساده‌ترین راه: خود PNG رو نگه می‌داریم و ICO می‌سازیم
    # با ذخیره‌ی PNG به عنوان ICO (Qt فقط PNG رو مستقیم می‌نویسه)
    img = QImage(str(assets / "app_icon.png"))
    img.save(str(assets / "app_icon.ico"), "ICO")
    print("✓ app_icon.ico")

    # راه مطمئن‌تر برای ویندوز: چند سایز PNG کنار هم
    for s in (16, 24, 32, 48, 64, 128, 256):
        svg_to_png(svg_path, assets / f"app_icon_{s}.png", size=s)

    print("\nDone. app_icon.png + app_icon.ico ساخته شدن.")


if __name__ == "__main__":
    main()