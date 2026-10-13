from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QPoint, Qt
from PySide6.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect

from ui.animations.easing import SMOOTH


class AnimationManager:
    _animations = []

    @staticmethod
    def _cleanup(animation):
        if animation in AnimationManager._animations:
            AnimationManager._animations.remove(animation)

    @staticmethod
    def transition_page(stack, target_page):
        current_page = stack.currentWidget()

        if current_page is target_page:
            return

        w = stack.width()
        h = stack.height()

        old_pix = current_page.grab()
        new_pix = target_page.grab()

        overlay = QWidget(stack)
        overlay.setGeometry(0, 0, w, h)
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        overlay.show()

        old_label = QLabel(overlay)
        old_label.setPixmap(old_pix)
        old_label.setGeometry(0, 0, w, h)

        new_label = QLabel(overlay)
        new_label.setPixmap(new_pix)
        new_label.setGeometry(w, 0, w, h)

        old_effect = QGraphicsOpacityEffect(old_label)
        old_label.setGraphicsEffect(old_effect)

        new_effect = QGraphicsOpacityEffect(new_label)
        new_label.setGraphicsEffect(new_effect)

        old_fade = QPropertyAnimation(old_effect, b"opacity")
        old_fade.setDuration(320)
        old_fade.setStartValue(1.0)
        old_fade.setEndValue(0.0)
        old_fade.setEasingCurve(SMOOTH)

        old_slide = QPropertyAnimation(old_label, b"pos")
        old_slide.setDuration(320)
        old_slide.setStartValue(QPoint(0, 0))
        old_slide.setEndValue(QPoint(-w // 2, 0))
        old_slide.setEasingCurve(SMOOTH)

        new_fade = QPropertyAnimation(new_effect, b"opacity")
        new_fade.setDuration(320)
        new_fade.setStartValue(0.0)
        new_fade.setEndValue(1.0)
        new_fade.setEasingCurve(SMOOTH)

        new_slide = QPropertyAnimation(new_label, b"pos")
        new_slide.setDuration(320)
        new_slide.setStartValue(QPoint(w, 0))
        new_slide.setEndValue(QPoint(0, 0))
        new_slide.setEasingCurve(SMOOTH)

        stack.setCurrentWidget(target_page)

        group = QParallelAnimationGroup(overlay)
        group.addAnimation(old_fade)
        group.addAnimation(old_slide)
        group.addAnimation(new_fade)
        group.addAnimation(new_slide)

        def cleanup():
            overlay.deleteLater()
            AnimationManager._cleanup(group)

        group.finished.connect(cleanup)

        AnimationManager._animations.append(group)
        group.start()