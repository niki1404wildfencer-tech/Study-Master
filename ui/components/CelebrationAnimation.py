import random
import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPolygonF


class CelebrationAnimation(QWidget):
    """انیمیشن جشن بزرگتر، طولانیتر و رنگارنگتر"""

    COLORS = [
        "#FF3B7B",  # صورتی تند
        "#4F7CFF",  # آبی برند
        "#22C55E",  # سبز
        "#FBBF24",  # طلایی
        "#A855F7",  # بنفش
        "#F97316",  # نارنجی
        "#06B6D4",  # فیروزهای
        "#EF4444",  # قرمز
        "#EC4899",  # سرخابی
        "#84CC16",  # لیمویی
        "#8B5CF6",  # بنفش روشن
        "#14B8A6",  # تیل
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(320, 320)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._particles = []
        self._sparkles = []
        self._tick = 0
        self._max_ticks = 260   # ~4.3 ثانیه
        self._center_scale = 0.0
        self._center_pulse = 0.0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        self._timer.setInterval(16)

    def start(self):
        self._particles = []
        self._sparkles = []
        self._tick = 0
        self._center_scale = 0.0
        self._center_pulse = 0.0

        cx = self.width() / 2
        cy = self.height() / 2

        # ── موج اول: کاغذرنگیهای بزرگ (انفجار) ──
        for _ in range(70):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 11)
            self._particles.append({
                "x": cx, "y": cy,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed - 3,
                "color": random.choice(self.COLORS),
                "size": random.uniform(6, 11),
                "rot": random.uniform(0, 360),
                "rot_speed": random.uniform(-12, 12),
                "life": random.randint(140, 240),
                "max_life": 240,
                "shape": random.choice(["rect", "circle", "star", "ribbon"]),
                "gravity": random.uniform(0.20, 0.30),
            })

        # ── موج دوم: جرقههای ریز درخشان ──
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(40, 120)
            self._sparkles.append({
                "x": cx + math.cos(angle) * dist,
                "y": cy + math.sin(angle) * dist,
                "color": random.choice(self.COLORS),
                "size": random.uniform(2, 4),
                "phase": random.uniform(0, 2 * math.pi),
                "life": random.randint(100, 200),
                "max_life": 200,
            })

        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _update(self):
        self._tick += 1

        # آیکون مرکزی
        if self._center_scale < 1.0:
            self._center_scale = min(1.0, self._center_scale + 0.055)
        # ضربان ملایم بعد از ظاهر شدن کامل
        if self._center_scale >= 1.0:
            self._center_pulse += 0.12

        # ذرات
        for p in self._particles:
            p["vy"] += p["gravity"]
            p["vx"] *= 0.992   # اصطکاک خیلی کم
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["rot"] += p["rot_speed"]
            p["life"] -= 1

        self._particles = [p for p in self._particles if p["life"] > 0]

        # جرقهها
        for s in self._sparkles:
            s["phase"] += 0.15
            s["life"] -= 1

        self._sparkles = [s for s in self._sparkles if s["life"] > 0]

        self.update()

        if self._tick >= self._max_ticks and not self._particles and not self._sparkles:
            self._timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ── جرقهها ──
        for s in self._sparkles:
            alpha_ratio = s["life"] / s["max_life"]
            pulse = (math.sin(s["phase"]) + 1) / 2
            alpha = int(255 * alpha_ratio * pulse)
            if alpha <= 0:
                continue
            color = QColor(s["color"])
            color.setAlpha(alpha)

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            r = s["size"] * (0.6 + pulse * 0.8)
            painter.drawEllipse(QPointF(s["x"], s["y"]), r, r)

        # ── ذرات ──
        for p in self._particles:
            alpha = int(255 * min(1.0, p["life"] / p["max_life"]))
            color = QColor(p["color"])
            color.setAlpha(alpha)

            painter.save()
            painter.translate(p["x"], p["y"])
            painter.rotate(p["rot"])

            # سایه ملایم برای عمق
            shadow = QColor(0, 0, 0, alpha // 5)
            painter.setBrush(QBrush(shadow))
            painter.setPen(Qt.PenStyle.NoPen)
            s = p["size"]
            painter.drawRoundedRect(QRectF(-s/2 + 1, -s/2 + 2, s, s*1.6), 2, 2)

            painter.setBrush(QBrush(color))
            if p["shape"] == "rect":
                painter.drawRoundedRect(QRectF(-s/2, -s/2, s, s*1.6), 2, 2)
            elif p["shape"] == "circle":
                painter.drawEllipse(QPointF(0, 0), s/2, s/2)
            elif p["shape"] == "ribbon":
                painter.drawRoundedRect(QRectF(-s/4, -s*0.9, s/2, s*1.8), 1, 1)
            else:
                self._draw_star(painter, s)

            painter.restore()

        # ── آیکون مرکزی ──
        self._draw_center_icon(painter)

    def _draw_star(self, painter, size):
        points = []
        for i in range(10):
            r = size if i % 2 == 0 else size / 2.2
            angle = math.radians(i * 36 - 90)
            points.append(QPointF(math.cos(angle) * r, math.sin(angle) * r))
        painter.drawPolygon(QPolygonF(points))

    def _draw_center_icon(self, painter):
        cx = self.width() / 2
        cy = self.height() / 2

        # ضربان ملایم
        pulse = 1.0 + math.sin(self._center_pulse) * 0.04 if self._center_pulse else 1.0
        base_radius = 52 * self._center_scale * pulse

        if base_radius < 1:
            return

        # ── هاله بیرونی ──
        for layer in range(3, 0, -1):
            glow = QColor("#22C55E")
            glow.setAlpha(int(25 / layer))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            r = base_radius * (1.0 + layer * 0.35)
            painter.drawEllipse(QPointF(cx, cy), r, r)

        # ── حلقه سفید ──
        painter.setBrush(Qt.BrushStyle.NoBrush)
        white_ring = QColor("white")
        white_ring.setAlpha(200)
        painter.setPen(QPen(white_ring, 3))
        painter.drawEllipse(QPointF(cx, cy), base_radius * 1.12, base_radius * 1.12)

        # ── دایره سبز ──
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#22C55E")))
        painter.drawEllipse(QPointF(cx, cy), base_radius, base_radius)

        # ── تیک سفید ──
        painter.setPen(QPen(
            QColor("white"),
            9 * self._center_scale,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        ))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        r = base_radius
        pts = [
            QPointF(cx - r * 0.45, cy + r * 0.05),
            QPointF(cx - r * 0.12, cy + r * 0.38),
            QPointF(cx + r * 0.48, cy - r * 0.35),
        ]
        for i in range(len(pts) - 1):
            painter.drawLine(pts[i], pts[i + 1])