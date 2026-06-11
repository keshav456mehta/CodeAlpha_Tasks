"""
auron_synthwave.py
AURON — Generative AI & LLMs Oracle
Theme: SYNTHWAVE  |  Deep purple · Hot pink · Amber · Neon city skyline BG
Run with: python auron_synthwave.py
"""

import tkinter as tk
import threading
import time
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from chatbot_engine import FAQChatbot

# ── Synthwave Palette ──────────────────────────────────────────────────────────
BG_VOID      = "#08050F"   # deepest void purple
BG_PANEL     = "#110A20"   # main panel
BG_CARD      = "#1C1035"   # card surface
BG_GLASS     = "#2E1A55"   # glass layer

PINK         = "#E91E8C"   # hot pink — primary accent
AMBER        = "#F5A623"   # amber — secondary accent
PURPLE_LIGHT = "#B06EFF"   # light violet
CYAN_NEON    = "#00FFFF"   # rare cyan pop
PINK_GLOW    = "#FF5CB8"   # bright pink glow

TEXT_PRIMARY = "#F0EAFF"   # soft lavender white
TEXT_MUTED   = "#6040A0"   # muted purple
TEXT_DIM     = "#2E1A55"   # very dim

USER_BG      = "#110A20"
BOT_BG       = "#07040E"

# ── Fonts ──────────────────────────────────────────────────────────────────────
FONT_DISPLAY = ("Courier New", 18, "bold")
FONT_HEADING = ("Courier New", 12, "bold")
FONT_BODY    = ("Consolas",    11)
FONT_SMALL   = ("Consolas",     9)
FONT_BADGE   = ("Courier New",  8, "bold")
FONT_INPUT   = ("Consolas",    12)
FONT_MONO    = ("Courier New",  9)


# ── Synthwave City Canvas ──────────────────────────────────────────────────────
class SynthwaveCanvas(tk.Canvas):
    """
    Neon city skyline with flickering windows, meteor shower, floating particles,
    amber moon with scan-stripes, scrolling perspective grid, and CRT vignette.
    """
    METEOR_MAX   = 8
    PARTICLE_NUM = 45

    def __init__(self, master, **kw):
        super().__init__(master, bg=BG_VOID, highlightthickness=0, **kw)
        self.meteors    = []
        self.particles  = []
        self.buildings  = []
        self.grid_off   = 0.0
        self._flicker_t = 0.0
        self._stars     = []
        self.bind("<Configure>", self._on_resize)
        self.after(100, self._init_scene)

    def _on_resize(self, e=None):
        self._init_scene()

    def _init_scene(self):
        W = self.winfo_width()  or 1400
        H = self.winfo_height() or 900
        self._W = W; self._H = H
        self._ground_y = int(H * 0.60)
        self._build_city()
        self._build_particles()
        self._build_stars()
        if not self.meteors:
            for _ in range(4): self._spawn_meteor()
        self._animate()

    # ── scene constructors ─────────────────────────────────────────────────────
    def _build_city(self):
        W, H = self._W, self._H
        gy = self._ground_y
        self.buildings = []
        x = 0
        while x < W:
            w = random.randint(18, 52)
            h = random.randint(30, min(100, gy - 10))
            windows = []
            rows = h // 14
            cols = w // 10
            for r in range(rows):
                for c in range(cols):
                    if random.random() < 0.55:
                        windows.append({
                            'x': x + 4 + c*10,
                            'y': gy - h + 6 + r*14,
                            'on': random.random() < 0.65,
                            'col': AMBER if random.random() < 0.5 else PURPLE_LIGHT,
                        })
            self.buildings.append({'x': x, 'w': w, 'h': h, 'windows': windows})
            x += w + random.randint(2, 10)

    def _build_particles(self):
        W, H = self._W, self._H
        colors = [PINK, PURPLE_LIGHT, AMBER, "#CC88FF"]
        self.particles = [
            {
                'x':     random.uniform(0, W),
                'y':     random.uniform(0, self._ground_y * 0.9),
                'r':     random.uniform(0.5, 1.8),
                'vy':    -random.uniform(0.12, 0.35),
                'phase': random.uniform(0, math.tau),
                'alpha': random.uniform(0.2, 0.6),
                'col':   random.choice(colors),
            }
            for _ in range(self.PARTICLE_NUM)
        ]

    def _build_stars(self):
        W, H = self._W, self._H
        self._stars = [
            (random.uniform(0, W), random.uniform(0, self._ground_y * 0.85),
             random.uniform(0.3, 0.8), random.random() * math.tau)
            for _ in range(90)
        ]

    def _spawn_meteor(self):
        W = self._W
        color = random.choice([PINK, PURPLE_LIGHT, AMBER, CYAN_NEON])
        self.meteors.append({
            'x':   random.uniform(0, W * 1.3),
            'y':   random.uniform(-60, -5),
            'vx':  -(1.8 + random.uniform(0, 3.2)),
            'vy':   2.5 + random.uniform(0, 4),
            'len':  70 + random.uniform(0, 130),
            'col':  color,
            'alpha': 0.55 + random.random() * 0.4,
        })

    # ── helpers ────────────────────────────────────────────────────────────────
    @staticmethod
    def _hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _blend(hex_color, bg_rgb, alpha):
        r, g, b = SynthwaveCanvas._hex_to_rgb(hex_color)
        r2 = int(bg_rgb[0] + (r - bg_rgb[0]) * alpha)
        g2 = int(bg_rgb[1] + (g - bg_rgb[1]) * alpha)
        b2 = int(bg_rgb[2] + (b - bg_rgb[2]) * alpha)
        return f'#{r2:02x}{g2:02x}{b2:02x}'

    # ── main loop ──────────────────────────────────────────────────────────────
    def _animate(self):
        self.delete("sw")
        W = self._W; H = self._H
        gy = self._ground_y
        t = time.time()

        # ── sky gradient (simulated with 4 horizontal bands) ──────────────────
        bg_rgb = (8, 5, 15)
        sky_cols = [
            (0.00, "#08050F"),
            (0.30, "#0E0820"),
            (0.55, "#1C1035"),
            (1.00, "#08050F"),
        ]
        step_h = max(1, H // len(sky_cols))
        for i, (frac, col) in enumerate(sky_cols):
            y0 = int(frac * gy)
            y1 = gy if i == len(sky_cols)-1 else int(sky_cols[i+1][0] * gy)
            self.create_rectangle(0, y0, W, y1, fill=col, outline="", tags="sw")

        # ── stars ─────────────────────────────────────────────────────────────
        for sx, sy, base_a, phase in self._stars:
            blink = base_a * (0.4 + 0.6 * abs(math.sin(t * 0.8 + phase)))
            col = self._blend("#F0EAFF", bg_rgb, blink)
            self.create_oval(sx-0.7, sy-0.7, sx+0.7, sy+0.7,
                             fill=col, outline="", tags="sw")

        # ── moon ──────────────────────────────────────────────────────────────
        mx = int(W * 0.77); my = int(H * 0.17); mr = 32
        # halo rings
        for ring, a in [(mr*2.8, 0.08), (mr*2.0, 0.14), (mr*1.4, 0.22)]:
            rc = self._blend(PINK, bg_rgb, a)
            self.create_oval(mx-ring, my-ring, mx+ring, my+ring,
                             fill=rc, outline="", tags="sw")
        # disk
        self.create_oval(mx-mr, my-mr, mx+mr, my+mr,
                         fill=AMBER, outline="", tags="sw")
        # scanlines on moon
        for s in range(-mr, mr, 6):
            hw = max(0, int(math.sqrt(max(0, mr*mr - s*s))))
            self.create_rectangle(mx-hw, my+s, mx+hw, my+s+3,
                                  fill="#08050F", stipple="", outline="", tags="sw")
            self.create_rectangle(mx-hw, my+s, mx+hw, my+s+1,
                                  fill="#08050F", outline="", tags="sw")

        # ── horizon glow ──────────────────────────────────────────────────────
        for band, col, a in [
            (gy-50, PINK,   0.12),
            (gy-30, PINK,   0.18),
            (gy-10, AMBER,  0.10),
        ]:
            bc = self._blend(col, bg_rgb, a)
            self.create_rectangle(0, band, W, gy, fill=bc, outline="", tags="sw")

        # ── meteors ───────────────────────────────────────────────────────────
        alive_meteors = []
        for m in self.meteors:
            m['x'] += m['vx']; m['y'] += m['vy']
            if m['y'] > gy or m['x'] < -250:
                continue
            angle = math.atan2(m['vy'], m['vx'])
            tx = m['x'] - math.cos(angle) * m['len']
            ty = m['y'] - math.sin(angle) * m['len']
            # tail (3 steps for glow)
            for width, frac_a in [(3, 0.15), (2, 0.45), (1.2, m['alpha'])]:
                tc = self._blend(m['col'], bg_rgb, frac_a)
                self.create_line(tx, ty, m['x'], m['y'],
                                 fill=tc, width=width, tags="sw")
            # head glow
            for gr, ga in [(5, 0.3), (3, 0.7)]:
                gc = self._blend(m['col'], bg_rgb, ga)
                self.create_oval(m['x']-gr, m['y']-gr, m['x']+gr, m['y']+gr,
                                 fill=gc, outline="", tags="sw")
            alive_meteors.append(m)
        self.meteors = alive_meteors
        if len(self.meteors) < self.METEOR_MAX and random.random() < 0.04:
            self._spawn_meteor()

        # ── floating particles ────────────────────────────────────────────────
        for p in self.particles:
            p['y'] += p['vy']
            p['x'] += math.sin(t * 0.5 + p['phase']) * 0.18
            if p['y'] < -5: p['y'] = float(gy)
            pc = self._blend(p['col'], bg_rgb, p['alpha'])
            r = p['r']
            self.create_oval(p['x']-r, p['y']-r, p['x']+r, p['y']+r,
                             fill=pc, outline="", tags="sw")

        # ── city buildings ────────────────────────────────────────────────────
        # flicker windows periodically
        if t - self._flicker_t > 0.9:
            self._flicker_t = t
            for b in self.buildings:
                for w in b['windows']:
                    if random.random() < 0.07:
                        w['on'] = not w['on']

        for b in self.buildings:
            bx, bw, bh = b['x'], b['w'], b['h']
            # silhouette
            self.create_rectangle(bx, gy-bh, bx+bw, gy+2,
                                  fill="#07040E", outline="", tags="sw")
            # pink neon roof edge
            rc = self._blend(PINK, bg_rgb, 0.6)
            self.create_line(bx, gy-bh, bx+bw, gy-bh,
                             fill=rc, width=1, tags="sw")
            # windows
            for w in b['windows']:
                if w['on']:
                    wc = self._blend(w['col'], (7, 4, 14), 0.85)
                    self.create_rectangle(w['x'], w['y'], w['x']+5, w['y']+7,
                                         fill=wc, outline="", tags="sw")

        # ── ground fill ───────────────────────────────────────────────────────
        self.create_rectangle(0, gy, W, H, fill=BG_VOID, outline="", tags="sw")

        # ── perspective grid (ground) ─────────────────────────────────────────
        self.grid_off = (self.grid_off + 0.009) % 1.0
        vp_x = W // 2

        # vertical converging lines
        VCOLS = 18
        for i in range(VCOLS+1):
            bx = int((i / VCOLS) * W)
            a  = 0.06 + 0.22 * (1 - abs(i/VCOLS - 0.5) * 2)
            gc = self._blend(PURPLE_LIGHT, (8, 5, 15), a)
            self.create_line(vp_x, gy, bx, H,
                             fill=gc, width=1, tags="sw")

        # horizontal scrolling lines
        HLINES = 14
        for i in range(HLINES):
            frac  = ((i / HLINES) + self.grid_off) % 1.0
            persp = frac ** 2.4
            line_y = int(gy + persp * (H - gy))
            a      = persp * 0.6
            lw     = int(persp * W)
            gc = self._blend(PINK, (8, 5, 15), a)
            self.create_line(vp_x - lw//2, line_y, vp_x + lw//2, line_y,
                             fill=gc, width=1, tags="sw")

        # horizon glow strip
        hc = self._blend(PINK, bg_rgb, 0.30)
        self.create_rectangle(0, gy-2, W, gy+2, fill=hc, outline="", tags="sw")

        # ── CRT scanlines ─────────────────────────────────────────────────────
        scan_col = self._blend("#000000", bg_rgb, 0.07)
        for row in range(0, H, 3):
            self.create_line(0, row, W, row,
                             fill=scan_col, width=1, tags="sw")

        # ── vignette (corner darkening via border) ────────────────────────────
        vc = self._blend("#000000", bg_rgb, 0.50)
        for inset in [0, 2, 5, 10, 18]:
            self.create_rectangle(inset, inset, W-inset, H-inset,
                                  fill="", outline=vc, width=3, tags="sw")

        self.after(33, self._animate)


# ── Typing indicator ───────────────────────────────────────────────────────────
class TypingDots(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=BOT_BG, **kw)
        self.dots = []
        for _ in range(3):
            d = tk.Label(self, text="◆", font=("Consolas", 9),
                         bg=BOT_BG, fg=TEXT_MUTED)
            d.pack(side=tk.LEFT, padx=2)
            self.dots.append(d)
        self.phase = 0
        self._blink()

    def _blink(self):
        colors = [TEXT_MUTED, TEXT_MUTED, TEXT_MUTED]
        colors[self.phase % 3] = PINK
        for i, d in enumerate(self.dots): d.config(fg=colors[i])
        self.phase += 1
        self._job = self.after(350, self._blink)

    def destroy(self):
        if hasattr(self, '_job'): self.after_cancel(self._job)
        super().destroy()


# ── Separator ──────────────────────────────────────────────────────────────────
class OrnateLineSeparator(tk.Canvas):
    def __init__(self, master, **kw):
        kw.setdefault('height', 18)
        kw.setdefault('bg', BG_PANEL)
        kw.setdefault('highlightthickness', 0)
        super().__init__(master, **kw)
        self.bind("<Configure>", self._draw)

    def _draw(self, e=None):
        self.delete("all")
        w = self.winfo_width() or 600
        cy = 9
        self.create_line(0, cy, w, cy, fill=TEXT_DIM, width=1)
        for xpos in [w//4, w//2, 3*w//4]:
            r = 4
            self.create_polygon(xpos, cy-r, xpos+r, cy,
                                xpos, cy+r, xpos-r, cy,
                                fill=PINK, outline=AMBER, width=1)


class NeonLine(tk.Canvas):
    def __init__(self, master, color=TEXT_DIM, **kw):
        kw.setdefault('height', 2)
        kw.setdefault('bg', BG_PANEL)
        kw.setdefault('highlightthickness', 0)
        super().__init__(master, **kw)
        self.color = color
        self.bind("<Configure>", self._draw)

    def _draw(self, e=None):
        self.delete("all")
        w = self.winfo_width()
        self.create_line(0, 1, w, 1, fill=self.color, width=1)


# ── Glitch title ───────────────────────────────────────────────────────────────
class GlitchLabel(tk.Label):
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789✦◆◈█▓░"
    def __init__(self, master, text, **kw):
        super().__init__(master, **kw)
        self._target   = text
        self._revealed = 0
        self._scramble_step()

    def _scramble_step(self):
        if self._revealed >= len(self._target):
            self.config(text=self._target); return
        scrambled = (
            self._target[:self._revealed]
            + random.choice(self.CHARS)
            + "".join(random.choice(self.CHARS)
                      for _ in range(min(4, len(self._target)-self._revealed-1)))
        )
        self.config(text=scrambled[:len(self._target)])
        self._revealed += 1
        self.after(55, self._scramble_step)


# ── Confidence bar ─────────────────────────────────────────────────────────────
class ConfBar(tk.Canvas):
    def __init__(self, master, value=0.0, **kw):
        kw.setdefault('height', 6)
        kw.setdefault('bg', BG_CARD)
        kw.setdefault('highlightthickness', 0)
        super().__init__(master, **kw)
        self._value  = 0
        self._target = value
        self._animate_to(value)
        self.bind("<Configure>", self._draw)

    def _animate_to(self, target):
        self._target = target; self._tick()

    def _tick(self):
        if abs(self._value - self._target) < 0.01:
            self._value = self._target; self._draw(); return
        self._value += (self._target - self._value) * 0.15
        self._draw()
        self.after(16, self._tick)

    def _draw(self, e=None):
        self.delete("all")
        w = self.winfo_width() or 200
        h = self.winfo_height() or 6
        self.create_rectangle(0, 0, w, h, fill=TEXT_DIM, outline="")
        fw = int(w * self._value)
        if fw > 0:
            color = PINK if self._value > 0.7 else (PURPLE_LIGHT if self._value > 0.4 else AMBER)
            self.create_rectangle(0, 0, fw, h, fill=color, outline="")
            gx = max(0, fw-8)
            self.create_rectangle(gx, 0, fw, h, fill=PINK_GLOW, outline="")


# ── Scrollable chat area ───────────────────────────────────────────────────────
class ChatArea(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=BG_PANEL, **kw)
        self.canvas = tk.Canvas(self, bg=BG_PANEL, highlightthickness=0, bd=0)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview,
                                bg=BG_CARD, troughcolor=BG_PANEL,
                                activebackground=PINK, width=6)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.inner = tk.Frame(self.canvas, bg=BG_PANEL)
        self.window_id = self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_frame_config)
        self.canvas.bind("<Configure>", self._on_canvas_config)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_config(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_config(self, e):
        self.canvas.itemconfig(self.window_id, width=e.width)

    def _on_mousewheel(self, e):
        self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    def scroll_bottom(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)


# ── Main App ───────────────────────────────────────────────────────────────────
class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ AURON — Synthwave | GenAI Oracle")
        self.geometry("1120x740")
        self.minsize(820, 580)
        self.configure(bg=BG_VOID)
        self.bot = FAQChatbot()
        self.msg_count = 0
        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = tk.Frame(self, bg=BG_PANEL, width=250)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        # Logo — Synthwave city canvas backdrop
        logo_canvas = SynthwaveCanvas(sb, height=140)
        logo_canvas.pack(fill=tk.X)

        tk.Label(logo_canvas, text="✦", font=("Courier New", 30),
                 fg=PINK, bg=BG_VOID).place(relx=0.5, rely=0.18, anchor="center")
        GlitchLabel(logo_canvas, text="AURON",
                    font=("Courier New", 18, "bold"),
                    fg=AMBER, bg=BG_VOID).place(relx=0.5, rely=0.58, anchor="center")
        tk.Label(logo_canvas, text="Generative AI & LLMs Oracle",
                 font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_VOID).place(
                     relx=0.5, rely=0.82, anchor="center")

        OrnateLineSeparator(sb).pack(fill=tk.X, padx=12, pady=4)

        # Status badge
        status = tk.Frame(sb, bg=BG_CARD,
                          highlightthickness=1, highlightbackground=TEXT_DIM,
                          padx=14, pady=8)
        status.pack(fill=tk.X, padx=14, pady=10)
        hdr_row = tk.Frame(status, bg=BG_CARD)
        hdr_row.pack()
        tk.Label(hdr_row, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_CARD).pack(side=tk.LEFT)
        dot = tk.Label(hdr_row, text="  ORACLE ONLINE  ", font=FONT_BADGE,
                       fg=PINK, bg=BG_CARD)
        dot.pack(side=tk.LEFT)
        tk.Label(hdr_row, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_CARD).pack(side=tk.LEFT)
        self._pulse_dot(dot)

        # Stats
        stats = tk.Frame(sb, bg=BG_PANEL, pady=6)
        stats.pack(fill=tk.X, padx=14)
        for label, value, color in [
            ("KNOWLEDGE BASE", "25 FAQ entries loaded",        PINK),
            ("ENGINE",         "TF-IDF + Cosine Similarity",   PURPLE_LIGHT),
            ("NLP PIPELINE",   "NLTK · Lemmatize · Bigrams",   AMBER),
        ]:
            tk.Label(stats, text=label, font=FONT_BADGE,
                     fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(6,0))
            tk.Label(stats, text=value, font=FONT_SMALL,
                     fg=color, bg=BG_PANEL).pack(anchor="w", pady=(1,0))

        OrnateLineSeparator(sb).pack(fill=tk.X, padx=12, pady=6)

        # ── Quick Topics header ───────────────────────────────────────────────
        hdr_frame = tk.Frame(sb, bg=BG_PANEL)
        hdr_frame.pack(fill=tk.X, padx=14, pady=(2, 6))
        tk.Label(hdr_frame, text="◈", font=("Courier New", 10, "bold"),
                 fg=AMBER, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr_frame, text="  QUICK TOPICS",
                 font=FONT_BADGE, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side=tk.LEFT)

        # colour-coded topic rows: (icon, label, icon_color, text_color, bg_card, border)
        topics = [
            ("✦", "What is an LLM?",             PINK,         "#FFB3D9", "#1A0A28", PINK),
            ("◈", "What is RAG?",                 AMBER,        "#FFD88A", "#1A1200", AMBER),
            ("▸", "Attention mechanism",           PURPLE_LIGHT, "#D4AAFF", "#160A2A", PURPLE_LIGHT),
            ("◆", "What is hallucination?",        "#FF6B6B",    "#FFAAAA", "#1A0808", "#FF6B6B"),
            ("✦", "Fine-tuning vs prompting",      CYAN_NEON,    "#A0FFFF", "#001A1A", CYAN_NEON),
            ("▸", "Transformer architecture",      PURPLE_LIGHT, "#D4AAFF", "#160A2A", PURPLE_LIGHT),
            ("◈", "What are AI agents?",           AMBER,        "#FFD88A", "#1A1200", AMBER),
            ("◆", "Chain of thought prompting",    PINK,         "#FFB3D9", "#1A0A28", PINK),
        ]

        for icon, q, icon_col, text_col, card_bg, border_col in topics:
            # outer card frame with colored left-border effect
            card = tk.Frame(sb, bg=card_bg,
                            highlightthickness=1,
                            highlightbackground=border_col)
            card.pack(fill=tk.X, padx=10, pady=2)

            # left color stripe
            stripe = tk.Frame(card, bg=border_col, width=3)
            stripe.pack(side=tk.LEFT, fill=tk.Y)

            # icon label
            ic_lbl = tk.Label(card, text=icon, font=("Courier New", 9, "bold"),
                              fg=icon_col, bg=card_bg, padx=6, pady=6)
            ic_lbl.pack(side=tk.LEFT)

            # topic text
            txt_lbl = tk.Label(card, text=q, font=FONT_SMALL,
                               fg=text_col, bg=card_bg,
                               anchor="w", cursor="hand2",
                               padx=2, pady=6)
            txt_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # hover: brighten the whole card
            def _enter(e, c=card, bg=card_bg, ic=ic_lbl, tx=txt_lbl,
                       ic_c=icon_col, tx_c=text_col, bdr=border_col):
                c.config(bg="#FFFFFF11", highlightbackground=bdr)
                ic.config(bg="#FFFFFF11", fg="#FFFFFF")
                tx.config(bg="#FFFFFF11", fg="#FFFFFF")

            def _leave(e, c=card, bg=card_bg, ic=ic_lbl, tx=txt_lbl,
                       ic_c=icon_col, tx_c=text_col, bdr=border_col):
                c.config(bg=bg, highlightbackground=bdr)
                ic.config(bg=bg, fg=ic_c)
                tx.config(bg=bg, fg=tx_c)

            # actually use a slightly lighter hover bg that works in tk
            hover_bg = "#251540"
            def _enter2(e, c=card, hbg=hover_bg, ic=ic_lbl, tx=txt_lbl,
                        ic_c=icon_col, tx_c="#FFFFFF", st=stripe, bdr=border_col):
                c.config(bg=hbg, highlightbackground=bdr)
                ic.config(bg=hbg, fg="#FFFFFF")
                tx.config(bg=hbg, fg="#FFFFFF")
                st.config(bg=bdr)

            def _leave2(e, c=card, obg=card_bg, ic=ic_lbl, tx=txt_lbl,
                        ic_c=icon_col, tx_c=text_col, st=stripe, bdr=border_col):
                c.config(bg=obg, highlightbackground=bdr)
                ic.config(bg=obg, fg=ic_c)
                tx.config(bg=obg, fg=tx_c)
                st.config(bg=bdr)

            for widget in [card, ic_lbl, txt_lbl, stripe]:
                widget.bind("<Enter>", _enter2)
                widget.bind("<Leave>", _leave2)
                widget.bind("<Button-1>", lambda e, q=q: self._quick_send(q))

        self.msg_counter = tk.Label(sb, text="0 messages",
                                    font=FONT_BADGE, fg=TEXT_DIM, bg=BG_PANEL)
        self.msg_counter.pack(side=tk.BOTTOM, pady=12)

    # ── Main area ──────────────────────────────────────────────────────────────
    def _build_main(self):
        main = tk.Frame(self, bg=BG_PANEL)
        main.grid(row=0, column=1, sticky="nsew")
        main.rowconfigure(2, weight=1)
        main.columnconfigure(0, weight=1)

        header = tk.Frame(main, bg=BG_PANEL, height=58, pady=10)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(header, text="◈  GENERATIVE AI & LLMs — KNOWLEDGE INTERFACE",
                 font=FONT_HEADING, fg=PINK, bg=BG_PANEL).pack(side=tk.LEFT, padx=18)

        self.conf_label = tk.Label(header, text="CONFIDENCE: —",
                                   font=FONT_BADGE, fg=TEXT_MUTED, bg=BG_PANEL)
        self.conf_label.pack(side=tk.RIGHT, padx=18)

        OrnateLineSeparator(main).grid(row=1, column=0, sticky="ew")

        self.chat = ChatArea(main)
        self.chat.grid(row=2, column=0, sticky="nsew")

        NeonLine(main, color=TEXT_DIM).grid(row=3, column=0, sticky="ew")

        conf_row = tk.Frame(main, bg=BG_PANEL, height=14, pady=2)
        conf_row.grid(row=4, column=0, sticky="ew", padx=18)
        conf_row.grid_propagate(False)
        tk.Label(conf_row, text="MATCH  ", font=FONT_BADGE,
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        self.conf_bar = ConfBar(conf_row, value=0)
        self.conf_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=4)

        input_row = tk.Frame(main, bg=BG_PANEL, pady=14)
        input_row.grid(row=5, column=0, sticky="ew", padx=18)
        input_row.columnconfigure(0, weight=1)

        input_wrap = tk.Frame(input_row, bg=BG_CARD,
                              highlightthickness=1, highlightbackground=TEXT_DIM)
        input_wrap.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        input_wrap.columnconfigure(0, weight=1)

        self.entry = tk.Entry(input_wrap, font=FONT_INPUT,
                              bg=BG_CARD, fg=TEXT_PRIMARY,
                              insertbackground=PINK,
                              relief="flat", bd=8)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_send)

        self._ph = True
        self.entry.insert(0, "Ask anything about Generative AI & LLMs…")
        self.entry.config(fg=TEXT_MUTED)
        self.entry.bind("<FocusIn>",  lambda e: self._clear_ph(e, input_wrap))
        self.entry.bind("<FocusOut>", lambda e: self._add_ph(e, input_wrap))

        send_btn = tk.Button(input_row, text="SEND  ▶",
                             font=FONT_BADGE,
                             bg=PINK, fg=BG_VOID,
                             activebackground=PINK_GLOW,
                             activeforeground=BG_VOID,
                             relief="flat", bd=0, padx=16, pady=10,
                             cursor="hand2", command=self._on_send)
        send_btn.grid(row=0, column=1)

        clear_btn = tk.Button(input_row, text="⟳",
                              font=("Consolas", 14),
                              bg=BG_CARD, fg=TEXT_MUTED,
                              activebackground=BG_GLASS,
                              relief="flat", bd=0, padx=10,
                              cursor="hand2", command=self._clear_chat)
        clear_btn.grid(row=0, column=2, padx=(4,0))

    # ── Welcome ────────────────────────────────────────────────────────────────
    def _show_welcome(self):
        welcome = (
            "AURON online. Synthwave grid active.\n\n"
            "I am your knowledge interface for Generative AI & Large Language Models — "
            "covering LLMs, transformers, attention, RAG, fine-tuning, hallucination, "
            "RLHF, embeddings, agents, and more.\n\n"
            "Select a topic from the sidebar, or transmit your query below."
        )
        self.after(200, lambda: self._add_bot_bubble(welcome, conf=None, delay=True))

    # ── Placeholder helpers ────────────────────────────────────────────────────
    def _clear_ph(self, e, wrap):
        wrap.config(highlightbackground=PINK)
        if self._ph:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_PRIMARY)
            self._ph = False

    def _add_ph(self, e, wrap):
        wrap.config(highlightbackground=TEXT_DIM)
        if not self.entry.get():
            self.entry.insert(0, "Ask anything about Generative AI & LLMs…")
            self.entry.config(fg=TEXT_MUTED)
            self._ph = True

    # ── Status pulse ───────────────────────────────────────────────────────────
    def _pulse_dot(self, dot, toggle=True):
        dot.config(fg=PINK if toggle else TEXT_DIM)
        self.after(900, lambda: self._pulse_dot(dot, not toggle))

    # ── Send logic ─────────────────────────────────────────────────────────────
    def _on_send(self, e=None):
        text = self.entry.get().strip()
        if not text or self._ph: return
        self.entry.delete(0, tk.END)
        self._ph = False
        self._add_user_bubble(text)
        threading.Thread(target=self._respond, args=(text,), daemon=True).start()

    def _quick_send(self, q):
        if self._ph:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_PRIMARY)
            self._ph = False
        self.entry.delete(0, tk.END)
        self.entry.insert(0, q)
        self._on_send()

    def _respond(self, text):
        typing = self._add_typing()
        time.sleep(0.7 + random.uniform(0, 0.4))
        answer, confidence = self.bot.get_answer(text)
        self.after(0, lambda: self._finish_response(typing, answer, confidence))

    def _finish_response(self, typing, answer, confidence):
        typing.destroy()
        self._add_bot_bubble(answer, conf=confidence, delay=True)
        self.conf_bar._animate_to(confidence if confidence else 0)
        pct   = f"{int((confidence or 0)*100)}%"
        color = PINK if (confidence or 0) > 0.6 else (PURPLE_LIGHT if (confidence or 0) > 0.3 else AMBER)
        self.conf_label.config(text=f"CONFIDENCE: {pct}", fg=color)

    # ── Bubble factories ───────────────────────────────────────────────────────
    def _add_user_bubble(self, text):
        self.msg_count += 1
        self.msg_counter.config(text=f"{self.msg_count} messages")
        row = tk.Frame(self.chat.inner, bg=BG_PANEL, pady=6)
        row.pack(fill=tk.X, padx=18)
        ts = time.strftime("%H:%M")
        tk.Label(row, text=f"YOU  {ts}", font=FONT_BADGE,
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="e", padx=4)
        bubble = tk.Frame(row, bg=USER_BG,
                          highlightthickness=1, highlightbackground=BG_GLASS)
        bubble.pack(anchor="e", padx=4)
        tk.Label(bubble, text=text, font=FONT_BODY,
                 fg=TEXT_PRIMARY, bg=USER_BG,
                 wraplength=520, justify="left",
                 padx=14, pady=10).pack()
        self.chat.scroll_bottom()
        self._fade_in(row)

    def _add_bot_bubble(self, text, conf=None, delay=False):
        self.msg_count += 1
        self.msg_counter.config(text=f"{self.msg_count} messages")
        row = tk.Frame(self.chat.inner, bg=BG_PANEL, pady=6)
        row.pack(fill=tk.X, padx=18)
        ts = time.strftime("%H:%M")

        hdr = tk.Frame(row, bg=BG_PANEL)
        hdr.pack(anchor="w", padx=4)
        tk.Label(hdr, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr, text="  AURON ", font=FONT_BADGE,
                 fg=PINK, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr, text=f"  {ts}  ", font=FONT_BADGE,
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_PANEL).pack(side=tk.LEFT)

        bubble = tk.Frame(row, bg=BOT_BG,
                          highlightthickness=1, highlightbackground=TEXT_DIM)
        bubble.pack(anchor="w", padx=4, fill=tk.X)
        tk.Frame(bubble, bg=TEXT_DIM, height=1).pack(fill=tk.X)

        self._text_label = tk.Label(bubble, text="", font=FONT_BODY,
                                    fg=TEXT_PRIMARY, bg=BOT_BG,
                                    wraplength=580, justify="left",
                                    padx=14, pady=10)
        self._text_label.pack(anchor="w", fill=tk.X)

        if conf is not None:
            topic = self._guess_topic(text)
            tk.Label(bubble,
                     text=f"— on: {topic}   ( confidence: {int(conf*100)}% )",
                     font=FONT_MONO, fg=TEXT_DIM, bg=BOT_BG,
                     anchor="e", padx=14, pady=4).pack(anchor="e", fill=tk.X)

        if delay:
            self._typewrite(self._text_label, text, 0)
        else:
            self._text_label.config(text=text)

        self.chat.scroll_bottom()
        self._fade_in(row)

    def _guess_topic(self, answer_text):
        keywords = {
            "Large Language Model": "LLMs",
            "Generative AI":        "Generative AI",
            "Transformer":          "Transformer Architecture",
            "attention":            "Attention Mechanism",
            "hallucination":        "AI Hallucination",
            "RAG":                  "RAG",
            "fine-tun":             "Fine-Tuning",
            "prompt":               "Prompt Engineering",
            "RLHF":                 "RLHF",
            "embedding":            "Embeddings",
            "GPT":                  "GPT vs BERT",
            "BERT":                 "GPT vs BERT",
            "token":                "Tokenisation",
            "context window":       "Context Window",
            "temperature":          "Temperature",
            "vector database":      "Vector Databases",
            "zero-shot":            "Zero/Few-Shot Learning",
            "agent":                "LLM Agents",
            "LoRA":                 "LoRA",
            "open-source":          "Open vs Closed LLMs",
            "multimodal":           "Multimodal AI",
            "inference":            "Inference vs Training",
            "quantis":              "Quantisation",
            "chain-of-thought":     "Chain of Thought",
            "system prompt":        "System Prompts",
            "Constitutional AI":    "Constitutional AI",
        }
        for kw, topic in keywords.items():
            if kw.lower() in answer_text.lower():
                return topic
        return "General AI"

    def _add_typing(self):
        row = tk.Frame(self.chat.inner, bg=BG_PANEL, pady=6)
        row.pack(fill=tk.X, padx=18)
        hdr2 = tk.Frame(row, bg=BG_PANEL)
        hdr2.pack(anchor="w", padx=4)
        tk.Label(hdr2, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr2, text="  AURON", font=FONT_BADGE,
                 fg=PINK, bg=BG_PANEL).pack(side=tk.LEFT)
        dots = TypingDots(row)
        dots.pack(anchor="w", padx=18, pady=6)
        self.chat.scroll_bottom()
        orig_destroy = row.destroy
        def destroy_all():
            dots.destroy(); orig_destroy()
        row.destroy = destroy_all
        return row

    def _typewrite(self, label, text, idx):
        if idx <= len(text):
            label.config(text=text[:idx])
            self.chat.scroll_bottom()
            speed = 10 if idx < len(text)*0.3 else 7
            self.after(speed, lambda: self._typewrite(label, text, idx+1))

    def _fade_in(self, widget):
        def step(n):
            if n > 8: return
            self.chat.scroll_bottom()
            self.after(30, lambda: step(n+1))
        step(0)

    def _clear_chat(self):
        for w in self.chat.inner.winfo_children(): w.destroy()
        self.msg_count = 0
        self.msg_counter.config(text="0 messages")
        self.conf_bar._animate_to(0)
        self.conf_label.config(text="CONFIDENCE: —", fg=TEXT_MUTED)
        self._show_welcome()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
