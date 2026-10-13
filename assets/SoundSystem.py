import threading 
import winsound

class SoundManager : 
    _thread = None 
    _stop_event = threading.Event()

    COMPLETION_SOUNDS =  {
    "None": None,

    # ── بهبود صداهای قبلی ─────────────────────────
    "Gentle": [
        (659, 180),   # E5
        (784, 180),   # G5
        (988, 350),   # B5 — آکورد نرم
    ],
    "Classic": [
        (523, 120),   # C5
        (659, 120),   # E5
        (784, 120),   # G5
        (1047, 400),  # C6 — گام بالارو
    ],
    "Digital": [
        (800, 70),
        (1200, 70),
        (1600, 70),
        (2000, 180),
    ],
    "Success": [
        (784, 100),   # G5
        (988, 100),   # B5
        (1319, 300),  # E6
    ],

    # ── صداهای جدید ───────────────────────────────
    "Encourage": [        # 🎈 شاد و امیدوارکننده
        (523, 100),   # C5
        (659, 100),   # E5
        (784, 100),   # G5
        (1047, 150),  # C6
        (784, 100),   # G5
        (1047, 300),  # C6
    ],

    "Achievement": [      # 🏆 تادای کلاسیک
        (392, 80),    # G4
        (523, 80),    # C5
        (659, 80),    # E5
        (784, 400),   # G5 — نتیجهگیری قوی
    ],

    "Celebration": [      # 🎉 فانفار جشن
        (523, 100), (523, 100), (523, 100),  # C5,C5,C5
        (659, 300),  # E5
        (784, 400),  # G5
    ],

    "Music Box": [        # 🎵 جعبهموزیک، آروم و رؤیایی
        (659, 150),   # E5
        (784, 150),   # G5
        (1047, 200),  # C6
        (784, 150),   # G5
        (659, 300),   # E5
    ],

    "Motivational": [     # 🚀 گام بالارو، حس پیشرفت
        (392, 90),   # G4
        (440, 90),   # A4
        (494, 90),   # B4
        (523, 90),   # C5
        (587, 90),   # D5
        (659, 90),   # E5
        (784, 350),  # G5
    ],

    "Cheer": [            # 📣 هلهله و تشویق
        (523, 80),    # C5
        (659, 80),    # E5
        (880, 80),    # A5
        (1047, 100),  # C6
        (880, 80),    # A5
        (1047, 100),  # C6
        (1319, 350),  # E6
    ],

    "Applause": [         # 👏 دستزدن سریع
        (1500, 30), (1000, 30), (1800, 30), (1200, 30),
        (1600, 30), (900, 30),  (1700, 30), (1100, 30),
        (1400, 30), (1900, 30), (1000, 30), (1600, 30),
        (1300, 30), (1500, 30), (1100, 30), (1700, 30),
    ],
}
    @classmethod
    def stop(cls) :
        cls._stop_event.set()
        try :
            winsound.PlaySound(
                None , 
                winsound.SND_PURGE
            )
        except RuntimeError : 
            pass
    @classmethod 
    def play_completion(cls , sound_name) : 
        pattern = cls.COMPLETION_SOUNDS.get(sound_name)
        if not pattern : 
            return
        cls.stop()
        cls._stop_event = threading.Event()

        def play() : 
            for frequency , duration in pattern : 
                if cls._stop_event.is_set() : 
                    return
                try : 
                    winsound.Beep(
                        frequency , 
                        duration
                    )         
                except RuntimeError : 
                    return
        cls._thread = threading.Thread(
            target=play , 
            daemon=True
        )        
        cls._thread.start()

    @classmethod
    def play_error(cls):
        try : 
            winsound.MessageBeep(
                winsound.MB_ICONHAND
            )
        except RuntimeError :
            pass
    @classmethod
    def play_warning(cls) :
        try :
            winsound.MessageBeep(
                winsound.MB_ICONEXCLAMATION
            )        
        except RuntimeError :
            pass
    @classmethod 
    def play_info(cls) :
        try : 
            winsound.MessageBeep(
                winsound.MB_ICONASTERISK
            )        
        except RuntimeError : 
            pass

    @classmethod
    def play_success(cls) :
        try :
            winsound.MessageBeep(
                winsound.MB_OK
            )        
        except RuntimeError :
            pass