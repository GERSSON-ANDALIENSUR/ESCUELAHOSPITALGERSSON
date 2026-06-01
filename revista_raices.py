"""
Revista educativa "Raíces que nos unen" — versión 2
Pueblos originarios de Chile · A4 vertical
"""

import math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

W, H = A4

# ── Registro de fuentes ────────────────────────────────────────────────────────
FONT_DIR_LIB  = "/usr/share/fonts/truetype/liberation"
FONT_DIR_DEJA = "/usr/share/fonts/truetype/dejavu"

pdfmetrics.registerFont(TTFont("Serif",     f"{FONT_DIR_LIB}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SerifB",    f"{FONT_DIR_LIB}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SerifI",    f"{FONT_DIR_LIB}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("SerifBI",   f"{FONT_DIR_LIB}/LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Sans",      f"{FONT_DIR_LIB}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SansB",     f"{FONT_DIR_LIB}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SansI",     f"{FONT_DIR_LIB}/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("SansBI",    f"{FONT_DIR_LIB}/LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Deja",      f"{FONT_DIR_DEJA}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaB",     f"{FONT_DIR_DEJA}/DejaVuSans-Bold.ttf"))

pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="SerifB",
                               italic="SerifI", boldItalic="SerifBI")
pdfmetrics.registerFontFamily("Sans",  normal="Sans",  bold="SansB",
                               italic="SansI",  boldItalic="SansBI")

# ── Paleta ─────────────────────────────────────────────────────────────────────
TERRACOTA   = HexColor('#B84A28')
ARENA       = HexColor('#E8D5A3')
ARENA_CLARO = HexColor('#F7F0E0')
TIERRA      = HexColor('#7A5030')
VERDE       = HexColor('#3D6B48')
VERDE_CLARO = HexColor('#9DC49A')
AZUL        = HexColor('#1E5F82')
AZUL_CLARO  = HexColor('#A8CEDE')
OCRE        = HexColor('#C87820')
MARRON      = HexColor('#4A2810')
SALMON      = HexColor('#D8896A')
GRIS_CLARO  = HexColor('#EDE8E0')
BLANCO      = colors.white
NEGRO       = HexColor('#1E1208')
CREMA       = HexColor('#FBF5E8')

# ── Estilos ────────────────────────────────────────────────────────────────────
def S(name, font, size, color=NEGRO, leading=None, align=TA_LEFT,
      after=4, before=0, leftI=0, bold=False):
    return ParagraphStyle(
        name, fontName=font, fontSize=size,
        textColor=color, leading=leading or size*1.35,
        alignment=align, spaceAfter=after, spaceBefore=before,
        leftIndent=leftI
    )

ST = {
    # Portada
    'port_titulo':    S('pt', 'SerifB',  42, BLANCO,  50,  TA_CENTER, 6),
    'port_sub':       S('ps', 'SerifI',  17, ARENA,   24,  TA_CENTER, 8),
    'port_cuerpo':    S('pc', 'Sans',    11, ARENA_CLARO, 17, TA_CENTER),
    # Encabezados de sección
    'banner_titulo':  S('bt', 'SerifB',  20, BLANCO,  26,  TA_LEFT),
    'banner_zona':    S('bz', 'SansI',   10, ARENA,   14,  TA_LEFT),
    # Contenido
    'label':          S('lb', 'SansB',    9, TIERRA,  13,  TA_LEFT, 1),
    'valor':          S('vl', 'Sans',     9, NEGRO,   13,  TA_LEFT, 3),
    'cuerpo':         S('cu', 'Serif',   10, NEGRO,   16,  TA_JUSTIFY, 4),
    'cuerpo_b':       S('cb', 'SerifB',  10, NEGRO,   15,  TA_LEFT, 4),
    'seccion':        S('sc', 'SerifB',  12, TERRACOTA,17, TA_LEFT, 4),
    # Cajas especiales
    'museo_lbl':      S('ml', 'SansB',    9, VERDE,   13,  TA_LEFT, 1),
    'museo_val':      S('mv', 'SansI',    9, HexColor('#2A5A38'), 14, TA_LEFT),
    'pregunta':       S('pr', 'SerifBI', 11, AZUL,    16,  TA_CENTER, 4),
    # Glosario
    'glos_term':      S('gt', 'SerifB',  11, TERRACOTA, 15, TA_LEFT, 2),
    'glos_def':       S('gd', 'Serif',    9.5, NEGRO,  14,  TA_LEFT, 6, leftI=10),
    # Fuentes
    'fuente_num':     S('fn', 'SansB',   10, OCRE,    14,  TA_LEFT),
    'fuente_txt':     S('ft', 'Serif',    9, NEGRO,   14,  TA_LEFT, 5),
    'nota':           S('no', 'SansI',    8, TIERRA,  12,  TA_CENTER),
    # Presentación
    'pres_titulo':    S('prt','SerifB',  15, TIERRA,  20,  TA_LEFT, 6),
    'pres_cuerpo':    S('prc','Serif',   10.5, NEGRO, 17, TA_JUSTIFY, 5),
    'pres_item':      S('pri','Serif',   10,  NEGRO,  15,  TA_LEFT, 3, leftI=6),
}

AN = W - 3*cm   # ancho neto de texto

# ══════════════════════════════════════════════════════════════════════════════
# ILUSTRACIONES — una por pueblo
# ══════════════════════════════════════════════════════════════════════════════

class IlustracionBase(Flowable):
    """Ilustración vectorial de cabecera para cada pueblo."""
    def __init__(self, ancho=AN, alto=7.2*cm):
        super().__init__()
        self.ancho = ancho
        self.alto  = alto

    def wrap(self, aw, ah):
        return self.ancho, self.alto

    # Helpers
    def _sky(self, c, col_top, col_bot):
        """Degradado de cielo simulado con franjas."""
        n = 12
        for i in range(n):
            f = i / n
            r = col_top.red   + f*(col_bot.red   - col_top.red)
            g = col_top.green + f*(col_bot.green - col_top.green)
            b = col_top.blue  + f*(col_bot.blue  - col_top.blue)
            c.setFillColor(HexColor(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'))
            c.rect(0, self.alto*(1 - (i+1)/n), self.ancho, self.alto/n+1, fill=1, stroke=0)

    def _mountain(self, c, peaks, color, base_y=0):
        """Cadena montañosa poligonal."""
        c.setFillColor(color)
        path = c.beginPath()
        path.moveTo(0, base_y)
        for x, y in peaks:
            path.lineTo(x, y)
        path.lineTo(self.ancho, base_y)
        path.close()
        c.drawPath(path, fill=1, stroke=0)

    def _wave(self, c, y, amp, freq, color, lw=1.5):
        """Ola sinusoidal."""
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        path = c.beginPath()
        path.moveTo(0, y)
        steps = 80
        for i in range(steps+1):
            x = self.ancho * i / steps
            yy = y + amp * math.sin(freq * i / steps * 2 * math.pi)
            if i == 0:
                path.moveTo(x, yy)
            else:
                path.lineTo(x, yy)
        c.drawPath(path, stroke=1, fill=0)

    def _stars(self, c, positions, r=1.5):
        c.setFillColor(BLANCO)
        for sx, sy in positions:
            c.circle(sx, sy, r, fill=1, stroke=0)

    def _text_overlay(self, c, zona_texto, color=ARENA_CLARO):
        """Texto de zona superpuesto en esquina inferior."""
        c.setFillColor(HexColor('#00000060'))
        c.roundRect(8, 6, self.ancho*0.6, 18, 3, fill=1, stroke=0)
        c.setFillColor(color)
        c.setFont('SansI', 8)
        c.drawString(13, 11, zona_texto)


# ─── Aimara ────────────────────────────────────────────────────────────────────
class IluAimara(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo noche-amanecer
        self._sky(c, HexColor('#0D1B3E'), HexColor('#C05828'))
        # Estrellas
        self._stars(c, [(aw*.05,ah*.88),(aw*.15,ah*.95),(aw*.28,ah*.90),
                        (aw*.42,ah*.93),(aw*.60,ah*.88),(aw*.75,ah*.94),
                        (aw*.88,ah*.90),(aw*.50,ah*.97),(aw*.33,ah*.82)])
        # Nieve cumbres
        self._mountain(c,
            [(0,ah*.45),(aw*.08,ah*.70),(aw*.18,ah*.55),(aw*.30,ah*.78),
             (aw*.42,ah*.62),(aw*.55,ah*.80),(aw*.68,ah*.58),(aw*.80,ah*.72),
             (aw*.92,ah*.54),(aw,ah*.45)],
            HexColor('#8898AA'))
        # Nieve blanca en cimas
        self._mountain(c,
            [(aw*.06,ah*.70),(aw*.08,ah*.74),(aw*.10,ah*.70)],
            HexColor('#E8EEF4'))
        self._mountain(c,
            [(aw*.28,ah*.78),(aw*.30,ah*.83),(aw*.32,ah*.78)],
            HexColor('#E8EEF4'))
        self._mountain(c,
            [(aw*.65,ah*.80),(aw*.68,ah*.85),(aw*.71,ah*.80)],
            HexColor('#E8EEF4'))
        # Altiplano / bofedal
        c.setFillColor(HexColor('#4A7848'))
        c.rect(0, 0, aw, ah*.28, fill=1, stroke=0)
        # Agua bofedal
        c.setFillColor(HexColor('#3A6888'))
        c.ellipse(aw*.10, ah*.06, aw*.38, ah*.18, fill=1, stroke=0)
        c.ellipse(aw*.55, ah*.08, aw*.82, ah*.16, fill=1, stroke=0)
        # Llamas silueta (dos)
        for ox, oy in [(aw*.68, ah*.10), (aw*.80, ah*.08)]:
            self._llama(c, ox, oy, ah*.14)
        # Chakana (cruz andina) decorativa
        self._chakana(c, aw*.88, ah*.72, 18, HexColor('#D4882888'))
        self._text_overlay(c, "Norte Grande · Altiplano · Cordillera")

    def _llama(self, c, x, y, h):
        s = h/3.5
        c.setFillColor(HexColor('#C8A870'))
        # cuerpo
        c.ellipse(x, y+s, x+s*2, y+s*2.2, fill=1, stroke=0)
        # cuello
        c.rect(x+s*1.2, y+s*1.8, s*0.45, s*1.2, fill=1, stroke=0)
        # cabeza
        c.ellipse(x+s*1.0, y+s*2.8, x+s*1.8, y+s*3.4, fill=1, stroke=0)
        # patas
        for px in [x+s*0.3, x+s*0.8, x+s*1.2, x+s*1.6]:
            c.rect(px, y, s*0.18, s*1.1, fill=1, stroke=0)

    def _chakana(self, c, cx, cy, r, col):
        c.setFillColor(col)
        c.setStrokeColor(HexColor('#D48828'))
        c.setLineWidth(0.8)
        # Cruz andina simplificada
        c.rect(cx-r, cy-r/3, r*2, r*2/3, fill=1, stroke=1)
        c.rect(cx-r/3, cy-r, r*2/3, r*2, fill=1, stroke=1)
        c.circle(cx, cy, r/3, fill=1, stroke=1)


# ─── Lickanantay ──────────────────────────────────────────────────────────────
class IluLickanantay(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo desértico cálido
        self._sky(c, HexColor('#8B4A10'), HexColor('#F0C868'))
        # Volcanoes / cordillera
        self._mountain(c,
            [(0,ah*.40),(aw*.12,ah*.68),(aw*.22,ah*.52),(aw*.35,ah*.72),
             (aw*.48,ah*.56),(aw*.60,ah*.65),(aw*.72,ah*.48),(aw*.85,ah*.62),(aw,ah*.42)],
            HexColor('#7A5030'))
        # Salar (hexágonos)
        c.setFillColor(HexColor('#E8E0D0'))
        c.rect(0, 0, aw, ah*.28, fill=1, stroke=0)
        hx_col  = HexColor('#C8C0B0')
        hx_size = ah*.055
        for row in range(4):
            for col_i in range(12):
                hx = hx_size
                ox = col_i * hx * 1.78 + (row % 2) * hx * 0.89
                oy = row * hx * 1.54
                self._hexagono(c, ox, oy, hx*0.82, hx_col)
        # Oasis (elipse verde con palmera)
        c.setFillColor(HexColor('#4A8040'))
        c.ellipse(aw*.60, ah*.12, aw*.82, ah*.26, fill=1, stroke=0)
        c.setFillColor(HexColor('#3A6030'))
        c.ellipse(aw*.63, ah*.14, aw*.79, ah*.24, fill=1, stroke=0)
        # Palmera
        self._palmera(c, aw*.70, ah*.10, ah*.20)
        # Río (línea sinuosa)
        c.setStrokeColor(HexColor('#5898C0'))
        c.setLineWidth(2.5)
        p = c.beginPath()
        p.moveTo(aw*.15, ah*.22)
        p.curveTo(aw*.25,ah*.18, aw*.35,ah*.24, aw*.45,ah*.20)
        p.curveTo(aw*.55,ah*.16, aw*.62,ah*.22, aw*.68,ah*.19)
        c.drawPath(p, stroke=1, fill=0)
        self._text_overlay(c, "Región de Antofagasta · Salar de Atacama · Oasis")

    def _hexagono(self, c, cx, cy, r, col):
        c.setFillColor(col)
        c.setStrokeColor(HexColor('#B0A898'))
        c.setLineWidth(0.4)
        pts = [(cx + r*math.cos(math.pi/6 + math.pi/3*i),
                cy + r*math.sin(math.pi/6 + math.pi/3*i)) for i in range(6)]
        path = c.beginPath()
        path.moveTo(*pts[0])
        for pt in pts[1:]: path.lineTo(*pt)
        path.close()
        c.drawPath(path, fill=1, stroke=1)

    def _palmera(self, c, x, y, h):
        c.setFillColor(HexColor('#6A4010'))
        c.rect(x, y, h*0.08, h*0.65, fill=1, stroke=0)
        c.setFillColor(HexColor('#2A7020'))
        for angle in [-50,-25,0,25,50]:
            rad = math.radians(angle+90)
            lx = x + h*0.04 + h*0.35*math.cos(rad)
            ly = y + h*0.65 + h*0.35*math.sin(rad)
            path = c.beginPath()
            path.moveTo(x+h*0.04, y+h*0.65)
            path.lineTo(lx, ly)
            c.setStrokeColor(HexColor('#2A7020'))
            c.setLineWidth(3)
            c.drawPath(path, stroke=1, fill=0)


# ─── Quechua ──────────────────────────────────────────────────────────────────
class IluQuechua(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo
        self._sky(c, HexColor('#1A2848'), HexColor('#5888B8'))
        self._stars(c, [(aw*.1,ah*.90),(aw*.2,ah*.85),(aw*.5,ah*.92),
                        (aw*.7,ah*.88),(aw*.85,ah*.93)])
        # Volcanes (conos)
        for vx, vh, vc in [(aw*.15,ah*.78,HexColor('#6A5848')),
                           (aw*.42,ah*.85,HexColor('#5A4838')),
                           (aw*.70,ah*.76,HexColor('#6A5848')),
                           (aw*.88,ah*.80,HexColor('#5A4838'))]:
            self._cono(c, vx, ah*.25, vh-ah*.25, vc)
        # Salar reflectante
        c.setFillColor(HexColor('#A8C8D8'))
        path = c.beginPath()
        path.moveTo(0, ah*.25)
        path.lineTo(aw, ah*.25)
        path.lineTo(aw, 0)
        path.lineTo(0, 0)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # Reflejos
        for ry in [ah*.05, ah*.13, ah*.20]:
            self._wave(c, ry, ah*.012, 2.5, HexColor('#88B0C888'), 0.8)
        # Terrazas
        for i, ty in enumerate([ah*.22, ah*.18, ah*.14]):
            c.setFillColor(HexColor(f'#{0x5A+i*0x10:02x}{0x40+i*0x08:02x}20'))
            c.rect(0, ty, aw*(0.3 - i*0.05), ah*.04, fill=1, stroke=0)
        # Patrón textil andino (borde superior)
        self._patron_textil(c, 0, ah*.93, aw, ah*.07)
        self._text_overlay(c, "Norte · Ollagüe · Alto Loa · Quebradas · Salares")

    def _cono(self, c, cx, base_y, height, color):
        c.setFillColor(color)
        path = c.beginPath()
        path.moveTo(cx - height*0.55, base_y)
        path.lineTo(cx, base_y + height)
        path.lineTo(cx + height*0.55, base_y)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # Nieve
        c.setFillColor(HexColor('#E8EEFF'))
        path2 = c.beginPath()
        path2.moveTo(cx - height*0.12, base_y + height*0.82)
        path2.lineTo(cx, base_y + height)
        path2.lineTo(cx + height*0.12, base_y + height*0.82)
        path2.close()
        c.drawPath(path2, fill=1, stroke=0)

    def _patron_textil(self, c, x, y, w, h):
        colors_pat = [TERRACOTA, OCRE, HexColor('#C83820'), OCRE, TERRACOTA]
        cw = w / len(colors_pat)
        for i, col in enumerate(colors_pat):
            c.setFillColor(col)
            c.rect(x + i*cw, y, cw, h, fill=1, stroke=0)
        # Rombo
        for i in range(int(w/(h*2))+1):
            cx2 = x + i * h*2 + h
            cy2 = y + h/2
            c.setFillColor(HexColor('#F0E0A0'))
            path = c.beginPath()
            path.moveTo(cx2, cy2+h*.4)
            path.lineTo(cx2+h*.4, cy2)
            path.lineTo(cx2, cy2-h*.4)
            path.lineTo(cx2-h*.4, cy2)
            path.close()
            c.drawPath(path, fill=1, stroke=0)


# ─── Colla ─────────────────────────────────────────────────────────────────────
class IluColla(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo árido
        self._sky(c, HexColor('#7A5028'), HexColor('#E8B870'))
        # Cordillera
        self._mountain(c,
            [(0,ah*.38),(aw*.10,ah*.60),(aw*.22,ah*.48),(aw*.34,ah*.65),
             (aw*.46,ah*.52),(aw*.58,ah*.68),(aw*.70,ah*.50),(aw*.82,ah*.62),(aw,ah*.40)],
            HexColor('#8A6848'))
        self._mountain(c,
            [(0,ah*.30),(aw*.15,ah*.45),(aw*.30,ah*.35),(aw*.48,ah*.50),
             (aw*.62,ah*.38),(aw*.78,ah*.48),(aw,ah*.32)],
            HexColor('#A88060'))
        # Quebrada / valle
        c.setFillColor(HexColor('#5A7840'))
        path = c.beginPath()
        path.moveTo(aw*.35, ah*.30)
        path.lineTo(aw*.42, 0)
        path.lineTo(aw*.58, 0)
        path.lineTo(aw*.65, ah*.30)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # Río en la quebrada
        c.setStrokeColor(HexColor('#5890B8'))
        c.setLineWidth(2)
        p = c.beginPath()
        p.moveTo(aw*.50, 0)
        p.curveTo(aw*.48,ah*.10, aw*.52,ah*.20, aw*.50,ah*.30)
        c.drawPath(p, stroke=1, fill=0)
        # Suelo / pampa
        c.setFillColor(HexColor('#C8A870'))
        c.rect(0, 0, aw, ah*.18, fill=1, stroke=0)
        # Cactus
        for cx2 in [aw*.10, aw*.20, aw*.75, aw*.85]:
            self._cactus(c, cx2, ah*.04, ah*.14)
        # Arriería: camino sinuoso
        c.setStrokeColor(HexColor('#8A6030'))
        c.setLineWidth(1.5)
        p2 = c.beginPath()
        p2.moveTo(0, ah*.10)
        p2.curveTo(aw*.20,ah*.14, aw*.40,ah*.08, aw*.60,ah*.12)
        p2.curveTo(aw*.75,ah*.15, aw*.88,ah*.10, aw,ah*.13)
        c.drawPath(p2, stroke=1, fill=0)
        self._text_overlay(c, "Región de Atacama · Precordillera · Cordillera · Quebradas")

    def _cactus(self, c, x, y, h):
        c.setFillColor(HexColor('#5A8030'))
        c.rect(x, y, h*0.18, h, fill=1, stroke=0)
        c.rect(x-h*0.28, y+h*0.45, h*0.28, h*0.14, fill=1, stroke=0)
        c.rect(x+h*0.18, y+h*0.55, h*0.28, h*0.14, fill=1, stroke=0)


# ─── Diaguita ─────────────────────────────────────────────────────────────────
class IluDiaguita(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo semiárido
        self._sky(c, HexColor('#5878A0'), HexColor('#B8C8D8'))
        # Sierra/montañas
        self._mountain(c,
            [(0,ah*.40),(aw*.12,ah*.65),(aw*.28,ah*.50),(aw*.40,ah*.70),
             (aw*.52,ah*.55),(aw*.65,ah*.68),(aw*.78,ah*.52),(aw*.90,ah*.62),(aw,ah*.42)],
            HexColor('#887060'))
        # Valle con río
        c.setFillColor(HexColor('#7A9850'))
        path = c.beginPath()
        path.moveTo(aw*.25, ah*.42)
        path.lineTo(aw*.20, 0)
        path.lineTo(aw*.80, 0)
        path.lineTo(aw*.75, ah*.42)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # Río (azul)
        c.setFillColor(HexColor('#4888C0'))
        path2 = c.beginPath()
        path2.moveTo(aw*.44, ah*.42)
        path2.lineTo(aw*.42, 0)
        path2.lineTo(aw*.58, 0)
        path2.lineTo(aw*.56, ah*.42)
        path2.close()
        c.drawPath(path2, fill=1, stroke=0)
        # Franja de cerámica Diaguita (parte superior) — patron bicolor
        self._patron_diaguita(c, 0, ah*.86, aw, ah*.14)
        self._text_overlay(c, "Norte Chico · Ríos Huasco y Choapa · Valles Transversales")

    def _patron_diaguita(self, c, x, y, w, h):
        """Patrón geométrico inspirado en cerámica Diaguita (bicolor)."""
        c.setFillColor(HexColor('#C83820'))
        c.rect(x, y, w, h, fill=1, stroke=0)
        n = int(w / (h*0.9))
        for i in range(n+1):
            cx2 = x + i * (w/n)
            # Triángulo negro alternado
            c.setFillColor(HexColor('#1A1008') if i%2==0 else HexColor('#E8D8A0'))
            path = c.beginPath()
            path.moveTo(cx2, y)
            path.lineTo(cx2 + w/n/2, y+h)
            path.lineTo(cx2 + w/n, y)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
        # Línea blanca central
        c.setStrokeColor(HexColor('#F0E8C8'))
        c.setLineWidth(1.2)
        c.line(x, y+h/2, x+w, y+h/2)
        # Rombos
        for i in range(n):
            cx3 = x + (i+0.5)*(w/n)
            cy3 = y + h/2
            r = h*0.22
            c.setFillColor(HexColor('#F0E8C8'))
            path = c.beginPath()
            path.moveTo(cx3, cy3+r); path.lineTo(cx3+r, cy3)
            path.lineTo(cx3, cy3-r); path.lineTo(cx3-r, cy3)
            path.close()
            c.drawPath(path, fill=1, stroke=0)


# ─── Chango ────────────────────────────────────────────────────────────────────
class IluChango(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo costero
        self._sky(c, HexColor('#204868'), HexColor('#88B8D8'))
        # Sol
        c.setFillColor(HexColor('#F8D060'))
        c.circle(aw*.80, ah*.82, ah*.10, fill=1, stroke=0)
        c.setFillColor(HexColor('#F8E890'))
        c.circle(aw*.80, ah*.82, ah*.07, fill=1, stroke=0)
        # Acantilado / cordillera costera
        self._mountain(c,
            [(0,ah*.48),(aw*.10,ah*.60),(aw*.20,ah*.50),(aw*.30,ah*.56),
             (aw*.38,ah*.44),(aw*.50,ah*.38)],
            HexColor('#8A7058'))
        c.setFillColor(HexColor('#8A7058'))
        c.rect(0, 0, aw*.50, ah*.38, fill=1, stroke=0)
        # Mar (Pacífico)
        c.setFillColor(HexColor('#1E5888'))
        c.rect(aw*.28, 0, aw, ah*.40, fill=1, stroke=0)
        # Olas
        for i, wy in enumerate([ah*.08, ah*.18, ah*.28, ah*.36]):
            self._wave(c, wy, ah*.025, 2+i*0.3, HexColor('#60A8D0'), 1.2+i*0.3)
        # Balsa (embarcación tradicional chango)
        self._balsa(c, aw*.62, ah*.30, ah*.10)
        # Pelícano silueta
        self._pelicano(c, aw*.45, ah*.52, ah*.10)
        # Camanchaca (bruma)
        c.setFillColor(HexColor('#A8C8D840'))
        c.rect(0, ah*.38, aw*.40, ah*.18, fill=1, stroke=0)
        self._text_overlay(c, "Costa Norte · Océano Pacífico · Corriente de Humboldt")

    def _balsa(self, c, x, y, size):
        c.setFillColor(HexColor('#C0906040'))
        c.setStrokeColor(HexColor('#8A6030'))
        c.setLineWidth(1)
        # cuerpo (elipse inflada)
        c.ellipse(x-size, y, x+size, y+size*0.4, fill=1, stroke=1)
        # mástil
        c.setStrokeColor(HexColor('#8A6030'))
        c.setLineWidth(1.5)
        c.line(x, y+size*0.4, x, y+size*1.4)
        # vela
        c.setFillColor(HexColor('#E8D8A080'))
        path = c.beginPath()
        path.moveTo(x, y+size*0.45)
        path.lineTo(x+size*0.9, y+size*0.9)
        path.lineTo(x, y+size*1.35)
        path.close()
        c.drawPath(path, fill=1, stroke=0)

    def _pelicano(self, c, x, y, size):
        c.setFillColor(HexColor('#2A3840'))
        c.ellipse(x, y+size*.3, x+size*.8, y+size*.7, fill=1, stroke=0)
        c.ellipse(x+size*.65, y+size*.55, x+size*1.0, y+size*.75, fill=1, stroke=0)
        # Alas
        c.setStrokeColor(HexColor('#2A3840'))
        c.setLineWidth(2)
        c.line(x+size*.15, y+size*.5, x-size*.5, y+size*.7)
        c.line(x+size*.65, y+size*.5, x+size*1.4, y+size*.65)


# ─── Rapa Nui ──────────────────────────────────────────────────────────────────
class IluRapaNui(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Atardecer Pacífico
        self._sky(c, HexColor('#1A3050'), HexColor('#E87830'))
        # Reflejo en el agua
        c.setFillColor(HexColor('#1A4870'))
        c.rect(0, 0, aw, ah*.28, fill=1, stroke=0)
        self._wave(c, ah*.12, ah*.018, 3, HexColor('#2868A8'), 1)
        self._wave(c, ah*.22, ah*.015, 2.5, HexColor('#3878B8'), 0.8)
        # Isla (silueta)
        c.setFillColor(HexColor('#2A5020'))
        path = c.beginPath()
        path.moveTo(0, ah*.28)
        path.curveTo(aw*.05,ah*.38, aw*.15,ah*.42, aw*.25,ah*.38)
        path.curveTo(aw*.38,ah*.34, aw*.50,ah*.40, aw*.65,ah*.36)
        path.curveTo(aw*.80,ah*.32, aw*.92,ah*.36, aw,ah*.30)
        path.lineTo(aw, ah*.28)
        path.lineTo(0, ah*.28)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # Volcán Rano Raraku
        self._mountain(c,
            [(aw*.55,ah*.28),(aw*.60,ah*.50),(aw*.70,ah*.28)],
            HexColor('#3A6030'))
        # AHU (plataforma)
        c.setFillColor(HexColor('#6A5040'))
        c.rect(aw*.08, ah*.28, aw*.50, ah*.04, fill=1, stroke=0)
        # Tres Moái
        for mx, mh in [(aw*.14, ah*.32),(aw*.24, ah*.36),(aw*.36, ah*.30)]:
            self._moai(c, mx, ah*.28, mh - ah*.28)
        # Sol sobre el océano
        c.setFillColor(HexColor('#F8A030'))
        c.circle(aw*.80, ah*.35, ah*.12, fill=1, stroke=0)
        c.setFillColor(HexColor('#F8C860'))
        c.circle(aw*.80, ah*.35, ah*.09, fill=1, stroke=0)
        self._text_overlay(c, "Isla Rapa Nui · Océano Pacífico Sur")

    def _moai(self, c, x, base_y, height):
        h = height
        w = h * 0.42
        c.setFillColor(HexColor('#887060'))
        # cuerpo
        c.rect(x, base_y, w, h*.60, fill=1, stroke=0)
        # cabeza
        c.rect(x+w*.05, base_y+h*.55, w*.9, h*.38, fill=1, stroke=0)
        # nariz
        c.setFillColor(HexColor('#706050'))
        c.rect(x+w*.35, base_y+h*.65, w*.22, h*.15, fill=1, stroke=0)
        # ojos
        c.setFillColor(HexColor('#1A1008'))
        c.rect(x+w*.18, base_y+h*.82, w*.20, h*.07, fill=1, stroke=0)
        c.rect(x+w*.58, base_y+h*.82, w*.20, h*.07, fill=1, stroke=0)


# ─── Mapuche ───────────────────────────────────────────────────────────────────
class IluMapuche(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo templado del sur
        self._sky(c, HexColor('#203848'), HexColor('#88B0C8'))
        # Cordillera nevada al fondo
        self._mountain(c,
            [(aw*.55,ah*.25),(aw*.62,ah*.55),(aw*.70,ah*.38),(aw*.80,ah*.58),
             (aw*.90,ah*.44),(aw,ah*.50)],
            HexColor('#9090A8'))
        # Nieve
        for mx, my in [(aw*.62,ah*.55),(aw*.80,ah*.58)]:
            c.setFillColor(HexColor('#EEF0F8'))
            c.circle(mx, my, ah*.04, fill=1, stroke=0)
        # Bosque nativo (araucarias + coihues)
        c.setFillColor(HexColor('#3A6030'))
        c.rect(0, 0, aw, ah*.30, fill=1, stroke=0)
        for tx in range(0, int(aw), int(aw/14)):
            self._arbol(c, tx + aw/28, ah*.04, ah*.28)
        # Lago
        c.setFillColor(HexColor('#3868A0'))
        c.ellipse(aw*.50, ah*.06, aw*.92, ah*.22, fill=1, stroke=0)
        self._wave(c, ah*.14, ah*.014, 4, HexColor('#5888C0'), 0.8)
        # Kultrun (tamboril sagrado) — círculo dividido
        self._kultrun(c, aw*.20, ah*.65, ah*.20)
        # Canelo (árbol sagrado)
        self._arbol_canelo(c, aw*.05, ah*.30, ah*.38)
        self._text_overlay(c, "Centro-sur y Sur · Wallmapu · Bosque Nativo · Lagos")

    def _arbol(self, c, x, y, h):
        # Tronco
        c.setFillColor(HexColor('#5A3820'))
        c.rect(x-h*.04, y, h*.08, h*.35, fill=1, stroke=0)
        # Copa triangular
        for i in range(3):
            c.setFillColor(HexColor(f'#{0x28+i*0x10:02x}{0x50+i*0x08:02x}20'))
            path = c.beginPath()
            path.moveTo(x - h*(0.22-i*0.04), y+h*(0.20+i*0.15))
            path.lineTo(x, y+h*(0.70+i*0.10))
            path.lineTo(x + h*(0.22-i*0.04), y+h*(0.20+i*0.15))
            path.close()
            c.drawPath(path, fill=1, stroke=0)

    def _arbol_canelo(self, c, x, y, h):
        c.setFillColor(HexColor('#5A3820'))
        c.rect(x, y, h*.10, h*.40, fill=1, stroke=0)
        c.setFillColor(HexColor('#3A7030'))
        c.ellipse(x-h*.15, y+h*.35, x+h*.25, y+h*.70, fill=1, stroke=0)
        c.setFillColor(HexColor('#488038'))
        c.ellipse(x-h*.10, y+h*.50, x+h*.20, y+h*.80, fill=1, stroke=0)
        c.setFillColor(HexColor('#5A9040'))
        c.ellipse(x-h*.06, y+h*.65, x+h*.16, y+h*.88, fill=1, stroke=0)

    def _kultrun(self, c, cx, cy, r):
        # Base
        c.setFillColor(HexColor('#C89058'))
        c.setStrokeColor(HexColor('#8A5828'))
        c.setLineWidth(1.5)
        c.circle(cx, cy, r, fill=1, stroke=1)
        # Cruz (cuatro mundos)
        c.setStrokeColor(HexColor('#8A3818'))
        c.setLineWidth(2)
        c.line(cx-r, cy, cx+r, cy)
        c.line(cx, cy-r, cx, cy+r)
        # Semicírculos en cada cuadrante
        for angle in [0, 90, 180, 270]:
            c.setFillColor(HexColor('#8A3818'))
            rad = math.radians(angle)
            c.circle(cx + r*.55*math.cos(rad), cy + r*.55*math.sin(rad),
                     r*.22, fill=1, stroke=0)
        # Borde decorativo
        c.setStrokeColor(HexColor('#F0D080'))
        c.setLineWidth(1)
        c.circle(cx, cy, r*.85, fill=0, stroke=1)


# ─── Kawashkar ────────────────────────────────────────────────────────────────
class IluKawashkar(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo tormentoso
        self._sky(c, HexColor('#181E28'), HexColor('#3A5060'))
        # Nubes de lluvia
        for nx, ny in [(aw*.10,ah*.72),(aw*.35,ah*.80),(aw*.60,ah*.75),(aw*.85,ah*.70)]:
            self._nube(c, nx, ny, ah*.14)
        # Lluvia
        c.setStrokeColor(HexColor('#6898B840'))
        c.setLineWidth(0.7)
        import random
        random.seed(42)
        for _ in range(60):
            rx = random.random()*aw
            ry = random.random()*ah*.70
            c.line(rx, ry, rx+ah*.02, ry-ah*.06)
        # Canal / agua
        c.setFillColor(HexColor('#203848'))
        c.rect(0, 0, aw, ah*.35, fill=1, stroke=0)
        for wy in [ah*.08, ah*.18, ah*.28]:
            self._wave(c, wy, ah*.022, 3, HexColor('#385870'), 1)
        # Islas / bosque magallánico
        for ix, iw, ih in [(0,aw*.25,ah*.22),(aw*.30,aw*.20,ah*.28),
                           (aw*.55,aw*.22,ah*.18),(aw*.82,aw*.18,ah*.24)]:
            c.setFillColor(HexColor('#1E3A20'))
            path = c.beginPath()
            path.moveTo(ix, ah*.35)
            path.curveTo(ix, ah*.35+ih, ix+iw/2, ah*.35+ih*1.1, ix+iw, ah*.35+ih)
            path.curveTo(ix+iw, ah*.35+ih, ix+iw, ah*.35, ix+iw, ah*.35)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
        # Canoa
        self._canoa(c, aw*.42, ah*.28, ah*.12)
        self._text_overlay(c, "Canales Australes · Archipiélagos · Magallanes")

    def _nube(self, c, x, y, size):
        c.setFillColor(HexColor('#3A4A58'))
        for dx, dy, r in [(0,0,size*.40),(size*.35,size*.05,size*.38),
                          (size*.68,size*-.02,size*.32),(size*-.25,size*-.05,size*.28)]:
            c.circle(x+dx, y+dy, r, fill=1, stroke=0)

    def _canoa(self, c, x, y, size):
        c.setFillColor(HexColor('#6A4820'))
        path = c.beginPath()
        path.moveTo(x, y + size*.25)
        path.curveTo(x+size*.2, y, x+size*1.6, y, x+size*2, y+size*.25)
        path.curveTo(x+size*1.6, y+size*.50, x+size*.2, y+size*.50, x, y+size*.25)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # remos
        c.setStrokeColor(HexColor('#4A3010'))
        c.setLineWidth(1.2)
        c.line(x+size*.55, y+size*.25, x+size*.40, y+size*.60)
        c.line(x+size*1.45, y+size*.25, x+size*1.60, y+size*.60)


# ─── Yámana/Yagán ──────────────────────────────────────────────────────────────
class IluYamana(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo muy austral
        self._sky(c, HexColor('#0A1218'), HexColor('#1A3048'))
        # Aurora (tenues)
        for i, acol in enumerate([HexColor('#18603040'), HexColor('#20804040'),
                                   HexColor('#18504020')]):
            c.setFillColor(acol)
            path = c.beginPath()
            path.moveTo(aw*(0.1+i*0.15), ah)
            path.curveTo(aw*(0.2+i*0.15), ah*.65, aw*(0.30+i*0.15), ah*.70,
                         aw*(0.40+i*0.15), ah*.55)
            path.lineTo(aw*(0.38+i*0.15), ah*.55)
            path.curveTo(aw*(0.28+i*0.15), ah*.70, aw*(0.18+i*0.15), ah*.65,
                         aw*(0.08+i*0.15), ah)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
        self._stars(c, [(aw*.05,ah*.90),(aw*.15,ah*.96),(aw*.30,ah*.88),
                        (aw*.50,ah*.94),(aw*.68,ah*.89),(aw*.82,ah*.96),(aw*.92,ah*.84)])
        # Silueta del Cabo de Hornos (icónica)
        c.setFillColor(HexColor('#0E1E10'))
        path = c.beginPath()
        path.moveTo(0, ah*.45)
        path.curveTo(aw*.05,ah*.52, aw*.12,ah*.55, aw*.18,ah*.50)
        path.curveTo(aw*.25,ah*.44, aw*.30,ah*.48, aw*.35,ah*.43)
        path.lineTo(aw*.38, 0)
        path.lineTo(0, 0)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        c.setFillColor(HexColor('#0E1E10'))
        path2 = c.beginPath()
        path2.moveTo(aw*.60, ah*.40)
        path2.curveTo(aw*.70,ah*.48, aw*.80,ah*.44, aw*.90,ah*.50)
        path2.lineTo(aw, ah*.46)
        path2.lineTo(aw, 0)
        path2.lineTo(aw*.65, 0)
        path2.close()
        c.drawPath(path2, fill=1, stroke=0)
        # Mar embravecido
        c.setFillColor(HexColor('#0A2838'))
        c.rect(0, 0, aw, ah*.30, fill=1, stroke=0)
        for wy in [ah*.06, ah*.14, ah*.22, ah*.28]:
            self._wave(c, wy, ah*.030, 2.5+wy/ah, HexColor('#2060A0'), 1.5)
        # Canoa en el canal
        self._canoa_yamana(c, aw*.44, ah*.22, ah*.09)
        self._text_overlay(c, "Canales Fueguinos · Cabo de Hornos · Archipiélago")

    def _canoa_yamana(self, c, x, y, size):
        c.setFillColor(HexColor('#5A3818'))
        path = c.beginPath()
        path.moveTo(x, y+size*.3)
        path.curveTo(x+size*.3,y, x+size*1.5,y, x+size*1.8,y+size*.3)
        path.curveTo(x+size*1.5,y+size*.60, x+size*.3,y+size*.60, x,y+size*.3)
        path.close()
        c.drawPath(path, fill=1, stroke=0)


# ─── Selk'nam ─────────────────────────────────────────────────────────────────
class IluSelknam(IlustracionBase):
    def draw(self):
        c = self.canv
        aw, ah = self.ancho, self.alto
        # Cielo pampa fueguina
        self._sky(c, HexColor('#1A2A3A'), HexColor('#607090'))
        # Viento (líneas)
        c.setStrokeColor(HexColor('#8098B030'))
        c.setLineWidth(0.8)
        for wy in [ah*.55,ah*.62,ah*.69,ah*.76,ah*.82]:
            p = c.beginPath()
            p.moveTo(0, wy)
            p.curveTo(aw*.25,wy+ah*.02, aw*.50,wy-ah*.02, aw*.75,wy+ah*.015)
            p.curveTo(aw*.88,wy-ah*.01, aw,wy+ah*.02, aw,wy)
            c.drawPath(p, stroke=1, fill=0)
        # Pampa (planicie inmensa)
        c.setFillColor(HexColor('#5A6840'))
        c.rect(0, 0, aw, ah*.30, fill=1, stroke=0)
        c.setFillColor(HexColor('#4A5830'))
        c.rect(0, 0, aw, ah*.18, fill=1, stroke=0)
        # Bosque austral al fondo (derecha)
        for i in range(8):
            bx = aw*(.60 + i*.05)
            bh = ah*(.12 + (i%3)*.04)
            c.setFillColor(HexColor('#1E3020'))
            path = c.beginPath()
            path.moveTo(bx - ah*.04, ah*.18)
            path.lineTo(bx, ah*.18 + bh)
            path.lineTo(bx + ah*.04, ah*.18)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
        # Guanaco silueta
        self._guanaco(c, aw*.20, ah*.12, ah*.20)
        # Patrón de pintura corporal Selk'nam (geométrico, decorativo)
        self._patron_selknam(c, aw*.55, ah*.38, ah*.42)
        self._text_overlay(c, "Isla Grande de Tierra del Fuego · Pampa · Bosques")

    def _guanaco(self, c, x, y, h):
        c.setFillColor(HexColor('#C8A060'))
        s = h/4
        c.ellipse(x, y+s, x+s*2.8, y+s*2.0, fill=1, stroke=0)
        # cuello
        path = c.beginPath()
        path.moveTo(x+s*2.2, y+s*1.6)
        path.lineTo(x+s*2.8, y+s*3.0)
        path.lineTo(x+s*3.2, y+s*2.8)
        path.lineTo(x+s*2.6, y+s*1.5)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # cabeza
        c.ellipse(x+s*2.7, y+s*2.8, x+s*3.4, y+s*3.4, fill=1, stroke=0)
        # orejas
        c.setFillColor(HexColor('#D0B070'))
        for ex, ey in [(x+s*2.8, y+s*3.35),(x+s*3.1, y+s*3.35)]:
            c.ellipse(ex-s*.10, ey, ex+s*.10, ey+s*.28, fill=1, stroke=0)
        # patas
        c.setFillColor(HexColor('#A87848'))
        for px in [x+s*.3, x+s*.8, x+s*1.6, x+s*2.2]:
            c.rect(px, y, s*.22, s*1.1, fill=1, stroke=0)

    def _patron_selknam(self, c, cx, cy, size):
        """Patrón geométrico inspirado en pintura corporal Selk'nam."""
        s = size
        # Triángulos y líneas
        c.setFillColor(HexColor('#D04020'))
        # Triángulo rojo
        path = c.beginPath()
        path.moveTo(cx, cy+s*.50)
        path.lineTo(cx+s*.30, cy)
        path.lineTo(cx-s*.30, cy)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        c.setFillColor(HexColor('#1A1008'))
        # Triángulo negro
        path = c.beginPath()
        path.moveTo(cx, cy)
        path.lineTo(cx+s*.30, cy-s*.50)
        path.lineTo(cx-s*.30, cy-s*.50)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        # Líneas horizontales
        c.setStrokeColor(HexColor('#D04020'))
        c.setLineWidth(2)
        for dy in [s*.15, s*.05, -s*.15]:
            c.line(cx-s*.35, cy+dy, cx+s*.35, cy+dy)
        # Punto central
        c.setFillColor(BLANCO)
        c.circle(cx, cy, s*.06, fill=1, stroke=0)


# ══════════════════════════════════════════════════════════════════════════════
# PORTADA (dibujada directamente en canvas)
# ══════════════════════════════════════════════════════════════════════════════

def portada(cv, doc):
    cv.saveState()

    # Fondo base
    cv.setFillColor(HexColor('#1A0C04'))
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    # Franjas de color degradadas
    franjas = [
        (HexColor('#C05020'), 0.00, 0.22),
        (HexColor('#8A3A10'), 0.22, 0.45),
        (HexColor('#3D1A08'), 0.45, 0.70),
        (HexColor('#1A0C04'), 0.70, 1.00),
    ]
    for col, y0, y1 in franjas:
        cv.setFillColor(col)
        cv.rect(0, H*y0, W, H*(y1-y0)+2, fill=1, stroke=0)

    # Círculos concéntricos decorativos (derecha)
    for r, col in [(200,HexColor('#8A3010')),(155,HexColor('#6A2008')),
                   (105,HexColor('#4A1205')),(60,HexColor('#C05020'))]:
        cv.setFillColor(col)
        cv.circle(W*.88, H*.38, r, fill=1, stroke=0)

    # Patrón geométrico Diaguita en banda superior
    bh = 1.8*cm
    cv.setFillColor(HexColor('#C05020'))
    cv.rect(0, H-bh, W, bh, fill=1, stroke=0)
    n_tri = 30
    tw = W/n_tri
    for i in range(n_tri+1):
        cv.setFillColor(HexColor('#1A0C04') if i%2==0 else HexColor('#E8C870'))
        path = cv.beginPath()
        path.moveTo(i*tw, H)
        path.lineTo(i*tw + tw/2, H - bh)
        path.lineTo((i+1)*tw, H)
        path.close()
        cv.drawPath(path, fill=1, stroke=0)

    # Patrón inferior
    cv.setFillColor(HexColor('#8A3010'))
    cv.rect(0, 0, W, 2*cm, fill=1, stroke=0)
    for i in range(n_tri+1):
        cv.setFillColor(HexColor('#1A0C04') if i%2==0 else HexColor('#C87020'))
        path = cv.beginPath()
        path.moveTo(i*tw, 0)
        path.lineTo(i*tw+tw/2, 2*cm)
        path.lineTo((i+1)*tw, 0)
        path.close()
        cv.drawPath(path, fill=1, stroke=0)

    # Chakana grande
    cv.setFillColor(HexColor('#8A301080'))
    r_ch = 60
    for angle in [0, 90]:
        rad = math.radians(angle)
        cv.rect(W*.14 - r_ch*math.cos(rad+math.pi/2),
                H*.62 - r_ch*math.sin(rad+math.pi/2),
                r_ch*2*abs(math.cos(rad)) + r_ch*0.66*abs(math.sin(rad)),
                r_ch*2*abs(math.sin(rad)) + r_ch*0.66*abs(math.cos(rad)),
                fill=1, stroke=0)

    # Línea dorada decorativa
    cv.setStrokeColor(HexColor('#C88030'))
    cv.setLineWidth(2.5)
    cv.line(1.5*cm, H*0.545, W-1.5*cm, H*0.545)
    cv.line(1.5*cm, H*0.540, W-1.5*cm, H*0.540)

    # ── Textos ──
    cv.setFillColor(ARENA)
    cv.setFont('SansB', 8.5)
    cv.drawCentredString(W/2, H-1.3*cm, "REVISTA EDUCATIVA · 7° y 8° BÁSICO · APRENDIZAJE BASADO EN PROYECTOS")

    # Título
    cv.setFillColor(BLANCO)
    cv.setFont('SerifB', 44)
    cv.drawCentredString(W/2, H*0.740, "Raíces que nos unen")

    # Subtítulo
    cv.setFillColor(HexColor('#E8C870'))
    cv.setFont('SerifI', 16)
    cv.drawCentredString(W/2, H*0.700,
        "Pueblos originarios de Chile, territorio e identidad")

    # Descripción
    cv.setFillColor(ARENA_CLARO)
    cv.setFont('Serif', 10.5)
    lineas = [
        "Revista de consulta para conocer la relación entre pueblos originarios,",
        "territorio, clima, relieve, agua, vegetación, recursos naturales,",
        "cultura e identidad."
    ]
    for i, ln in enumerate(lineas):
        cv.drawCentredString(W/2, H*0.645 - i*15, ln)

    # Caja de pueblos incluidos
    cv.setFillColor(HexColor('#2A100430'))
    cv.roundRect(1.5*cm, H*0.235, W-3*cm, H*0.28, 10, fill=1, stroke=0)
    cv.setStrokeColor(HexColor('#C88030'))
    cv.setLineWidth(1.5)
    cv.roundRect(1.5*cm, H*0.235, W-3*cm, H*0.28, 10, fill=0, stroke=1)

    cv.setFillColor(HexColor('#E8C870'))
    cv.setFont('SansB', 9.5)
    cv.drawCentredString(W/2, H*0.496, "Pueblos originarios incluidos en esta revista:")

    pueblos_txt = [
        "Aimara / Aymara   ·   Atacameño / Lickanantay   ·   Quechua",
        "Colla   ·   Diaguita   ·   Chango   ·   Rapa Nui",
        "Mapuche   ·   Kawashkar   ·   Yámana / Yagán   ·   Selk'nam"
    ]
    cv.setFillColor(ARENA_CLARO)
    cv.setFont('Serif', 10)
    for i, ln in enumerate(pueblos_txt):
        cv.drawCentredString(W/2, H*0.462 - i*16, ln)

    # Nota ABP
    cv.setFillColor(HexColor('#3D6B48'))
    cv.roundRect(1.5*cm, H*0.175, W-3*cm, 1.0*cm, 6, fill=1, stroke=0)
    cv.setFillColor(BLANCO)
    cv.setFont('SansB', 9)
    cv.drawCentredString(W/2, H*0.198,
        "Recurso ABP · Lengua y Literatura  |  Historia, Geografía y Ciencias Sociales")

    # Pie
    cv.setFillColor(HexColor('#C88030'))
    cv.setFont('SansI', 7.5)
    cv.drawCentredString(W/2, 0.8*cm, "Uso exclusivamente educativo · Sin fines comerciales")

    cv.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# ENCABEZADO Y PIE PÁGINAS INTERNAS
# ══════════════════════════════════════════════════════════════════════════════

def header_footer(cv, doc):
    cv.saveState()

    # Header
    cv.setFillColor(MARRON)
    cv.rect(0, H-1.0*cm, W, 1.0*cm, fill=1, stroke=0)
    cv.setFillColor(OCRE)
    cv.rect(0, H-1.08*cm, W, 0.08*cm, fill=1, stroke=0)
    cv.setFillColor(BLANCO)
    cv.setFont('SerifB', 9)
    cv.drawString(1.5*cm, H-0.68*cm, "RAÍCES QUE NOS UNEN")
    cv.setFont('SansI', 7.5)
    cv.drawRightString(W-1.5*cm, H-0.68*cm,
                       "Pueblos originarios de Chile · Uso educativo")

    # Footer
    cv.setFillColor(ARENA)
    cv.rect(0, 0, W, 0.85*cm, fill=1, stroke=0)
    cv.setFillColor(OCRE)
    cv.rect(0, 0.85*cm, W, 0.07*cm, fill=1, stroke=0)
    cv.setFillColor(TIERRA)
    cv.setFont('SansI', 7.5)
    cv.drawString(1.5*cm, 0.30*cm,
                  "Revista educativa para 7° y 8° básico · ABP")
    cv.setFont('SansB', 8)
    cv.drawRightString(W-1.5*cm, 0.28*cm, f"Pág. {doc.page}")
    cv.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS DE CONTENIDO
# ══════════════════════════════════════════════════════════════════════════════

def banner_pueblo(nombre, zona, color_bg, color_acento):
    """Banner título + zona para páginas de pueblo."""
    p_nombre = Paragraph(nombre, ST['banner_titulo'])
    p_zona   = Paragraph(zona,   ST['banner_zona'])
    ancho = AN
    t = Table([[p_nombre],[p_zona]], colWidths=[ancho])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_bg),
        ('BACKGROUND', (0,0), (0,0),  color_bg),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0),(0,0), 0.5, color_acento),
        ('LINEAFTER', (0,0),(-1,-1), 4, color_acento),
    ]))
    return t


def grilla_datos(campos, color_bg, color_borde, color_label):
    """
    campos: lista de (icono, etiqueta, valor) — dos columnas por fila.
    """
    ancho_col = AN / 2 - 0.15*cm

    filas = []
    # Agrupar de dos en dos
    for i in range(0, len(campos), 2):
        celdas = []
        for j in range(2):
            if i+j < len(campos):
                ico, lbl, val = campos[i+j]
                header = Paragraph(f"{ico}  {lbl}", ST['label'])
                body   = Paragraph(val, ST['valor'])
                inner  = Table([[header],[body]], colWidths=[ancho_col-0.4*cm])
                inner.setStyle(TableStyle([
                    ('TOPPADDING',    (0,0),(-1,-1), 3),
                    ('BOTTOMPADDING', (0,0),(-1,-1), 3),
                    ('LEFTPADDING',   (0,0),(-1,-1), 0),
                    ('RIGHTPADDING',  (0,0),(-1,-1), 0),
                ]))
                celdas.append(inner)
            else:
                celdas.append(Paragraph('', ST['valor']))
        filas.append(celdas)

    t = Table(filas, colWidths=[ancho_col, ancho_col])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), color_bg),
        ('ROWBACKGROUNDS',(0,0),(-1,-1), [color_bg, CREMA]),
        ('BOX',           (0,0),(-1,-1), 1.5, color_borde),
        ('INNERGRID',     (0,0),(-1,-1), 0.5, HexColor('#C8B89A')),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 7),
        ('RIGHTPADDING',  (0,0),(-1,-1), 7),
    ]))
    return t


def caja_expresiones(texto, color_bg, color_borde):
    lbl = Paragraph("✦  Expresiones culturales", ST['seccion'])
    txt = Paragraph(texto, ST['cuerpo'])
    t = Table([[lbl],[txt]], colWidths=[AN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), HexColor('#FBF5E8')),
        ('BACKGROUND', (0,0),(0,0),   color_bg),
        ('BOX',        (0,0),(-1,-1), 1.5, color_borde),
        ('LINEBELOW',  (0,0),(0,0),   0.5, color_borde),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ]))
    return t


def fila_museo_pregunta(museo_txt, pregunta_txt, color_museo, color_preg):
    # Caja museo
    m_lbl = Paragraph("🏛  Idea para el museo", ST['museo_lbl'])
    m_txt = Paragraph(museo_txt, ST['museo_val'])
    t_m = Table([[m_lbl],[m_txt]], colWidths=[AN/2 - 0.15*cm])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), HexColor('#E8F4E8')),
        ('BOX',        (0,0),(-1,-1), 1.2, VERDE),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))
    # Caja pregunta
    q_lbl = Paragraph("❓ Pregunta para investigar", ST['museo_lbl'])
    q_txt = Paragraph(pregunta_txt, ST['pregunta'])
    t_q = Table([[q_lbl],[q_txt]], colWidths=[AN/2 - 0.15*cm])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), AZUL_CLARO),
        ('BOX',        (0,0),(-1,-1), 1.2, AZUL),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))
    # Fila con ambas cajas
    fila = Table([[t_m, t_q]], colWidths=[AN/2-0.15*cm, AN/2+0.15*cm])
    fila.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 0),
    ]))
    return fila


def pagina_pueblo(ilu, nombre, zona, color_banner, color_acento,
                  campos, expresiones, museo_txt, pregunta_txt):
    elems = []
    elems.append(banner_pueblo(nombre, zona, color_banner, color_acento))
    elems.append(Spacer(1, 0.18*cm))
    elems.append(ilu)
    elems.append(Spacer(1, 0.18*cm))
    elems.append(grilla_datos(campos, ARENA_CLARO, color_banner, color_banner))
    elems.append(Spacer(1, 0.18*cm))
    elems.append(caja_expresiones(expresiones, color_banner, color_banner))
    elems.append(Spacer(1, 0.18*cm))
    elems.append(fila_museo_pregunta(museo_txt, pregunta_txt, VERDE, AZUL))
    elems.append(PageBreak())
    return elems


# ══════════════════════════════════════════════════════════════════════════════
# CONSTRUCCIÓN DE LA REVISTA
# ══════════════════════════════════════════════════════════════════════════════

def construir():
    story = []

    # ── PÁG 2: PRESENTACIÓN ──────────────────────────────────────────────────
    # Banner
    p_title = Paragraph("¿Para qué usaremos esta revista?", ST['pres_titulo'])
    t_banner = Table([[p_title]], colWidths=[AN])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), TIERRA),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('LINEAFTER', (0,0),(-1,-1), 5, OCRE),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 0.35*cm))

    story.append(Paragraph(
        "Esta revista es una fuente de consulta para conocer algunos pueblos "
        "originarios de Chile y comprender cómo el territorio influye en sus "
        "formas de vida, actividades, cultura e identidad. A través de la "
        "lectura, los estudiantes podrán obtener información para completar "
        "fichas de Lenguaje e Historia, y preparar producciones para el museo "
        "intercultural <b>«Raíces que nos unen»</b>.",
        ST['pres_cuerpo']
    ))
    story.append(Spacer(1, 0.28*cm))

    # Tabla de dos columnas: qué observaremos + para qué
    obs_items = [
        ("📍", "Zona donde habita o habitó"),
        ("🌤", "Clima del territorio"),
        ("🏔", "Relieve del territorio"),
        ("💧", "Agua: ríos, lagos, mar o canales"),
        ("🌿", "Vegetación y recursos naturales"),
        ("🏡", "Forma de vida relacionada con el territorio"),
        ("🎭", "Expresiones culturales"),
        ("🏛", "Ideas para el museo intercultural"),
    ]
    uso_items = [
        ("📚", "¿Para quiénes?",
         "Estudiantes de 7° y 8° básico en ABP."),
        ("📖", "¿Para qué asignaturas?",
         "Lengua y Literatura · Historia, Geografía y CC.SS."),
        ("✏️",  "¿Cómo usarlo?",
         "Lee cada ficha, extrae los datos del territorio y responde "
         "la pregunta de investigación."),
        ("🏛",  "¿Qué produciremos?",
         "Fichas de investigación y producciones para el museo "
         "intercultural «Raíces que nos unen»."),
    ]

    # Col izquierda: observaremos
    left_rows = [[Paragraph("Observaremos en cada pueblo:", ST['seccion'])]]
    for ico, txt in obs_items:
        left_rows.append([Paragraph(f"{ico}  {txt}", ST['pres_item'])])
    t_left = Table(left_rows, colWidths=[AN/2-0.2*cm])
    t_left.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), ARENA_CLARO),
        ('BACKGROUND', (0,0),(0,0),   HexColor('#C05020')),
        ('TEXTCOLOR',  (0,0),(0,0),   BLANCO),
        ('BOX',        (0,0),(-1,-1), 1.5, TERRACOTA),
        ('LINEBELOW',  (0,0),(0,0),   1,   TERRACOTA),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))

    # Col derecha: instrucciones
    right_rows = [[Paragraph("¿Cómo trabajaremos?", ST['seccion'])]]
    for ico, lbl, val in uso_items:
        right_rows.append([Paragraph(f"{ico}  <b>{lbl}</b>", ST['pres_item'])])
        right_rows.append([Paragraph(f"     {val}", ST['pres_item'])])
    t_right = Table(right_rows, colWidths=[AN/2-0.2*cm])
    t_right.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), HexColor('#EEF6FF')),
        ('BACKGROUND', (0,0),(0,0),   AZUL),
        ('TEXTCOLOR',  (0,0),(0,0),   BLANCO),
        ('BOX',        (0,0),(-1,-1), 1.5, AZUL),
        ('LINEBELOW',  (0,0),(0,0),   1,   AZUL),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))

    t_dos_col = Table([[t_left, t_right]], colWidths=[AN/2-0.2*cm, AN/2+0.2*cm])
    t_dos_col.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0),(-1,-1), 0),
        ('RIGHTPADDING',  (0,0),(-1,-1), 0),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 0),
    ]))
    story.append(t_dos_col)
    story.append(Spacer(1, 0.3*cm))

    # Nota de respeto
    p_nota = Paragraph(
        "Los pueblos originarios presentados en esta revista son comunidades "
        "vivas que mantienen su identidad, lengua y cultura. Esta revista "
        "los reconoce como pueblos con historia propia, presencia actual "
        "y derechos vigentes en Chile.",
        ST['pres_cuerpo']
    )
    t_nota = Table([[p_nota]], colWidths=[AN])
    t_nota.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), HexColor('#EEF8F0')),
        ('BOX',        (0,0),(-1,-1), 2,   VERDE),
        ('LINEAFTER',  (0,0),(-1,-1), 5,   VERDE),
        ('TOPPADDING',    (0,0),(-1,-1), 9),
        ('BOTTOMPADDING', (0,0),(-1,-1), 9),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ]))
    story.append(t_nota)
    story.append(PageBreak())

    # ══ PÁGINAS DE PUEBLOS ════════════════════════════════════════════════════

    # ── AIMARA ────────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluAimara(AN, 7.2*cm),
        nombre="Pueblo Aimara / Aymara",
        zona="Norte Grande · Arica y Parinacota · Tarapacá · Antofagasta",
        color_banner=HexColor('#8A3010'),
        color_acento=HexColor('#C87820'),
        campos=[
            ("🏔","Territorio",
             "Altiplano, puna, sierra, precordillera, valles altos y bajos."),
            ("🌤","Clima",
             "Frío y seco en altura; gran diferencia de temperatura entre el día y la noche; lluvias estivales en sectores altiplánicos."),
            ("⛰","Relieve",
             "Altiplano, cordillera, quebradas y valles de altura."),
            ("💧","Agua y recursos",
             "Bofedales, vegas, quebradas; agricultura en terrazas; ganadería de camélidos."),
            ("🌿","Vegetación",
             "Pastos de altura, vegetación de bofedales y arbustos adaptados a la aridez."),
            ("🏡","Forma de vida",
             "Vida vinculada a distintos pisos ecológicos: agricultura, pastoreo, intercambio y organización comunitaria."),
        ],
        expresiones=(
            "Lengua aimara · Tejidos · Música · Festividades · "
            "Relación con la Pachamama · Vida comunitaria."
        ),
        museo_txt=(
            "Mapa de pisos ecológicos · Tejido andino · "
            "Dibujo de bofedal · Ficha sobre pastoreo · "
            "Maqueta de terrazas agrícolas."
        ),
        pregunta_txt="¿Cómo influye la vida en altura en las actividades del pueblo Aimara/Aymara?",
    )

    # ── LICKANANTAY ───────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluLickanantay(AN, 7.2*cm),
        nombre="Pueblo Atacameño o Lickanantay",
        zona="Región de Antofagasta · Salar de Atacama · Río Loa · Oasis",
        color_banner=HexColor('#6A3010'),
        color_acento=HexColor('#B07828'),
        campos=[
            ("🏜","Territorio",
             "Desierto de Atacama, oasis, salares, vegas, bofedales y quebradas."),
            ("🌡","Clima",
             "Desértico, de extrema aridez y gran oscilación térmica entre el día y la noche."),
            ("⛰","Relieve",
             "Desierto, cordillera, salares, quebradas y oasis."),
            ("💧","Agua y recursos",
             "Ríos El Loa, El Salado y Vilama; vegas, bofedales y aguas de quebradas."),
            ("🌿","Vegetación",
             "Tolar, pajonal, yareta, algarrobo, tamarugo, chañar y vegetación de oasis."),
            ("🏡","Forma de vida",
             "El agua permitió la agricultura, el pastoreo y la vida en oasis. El desierto influyó en sus asentamientos y relación con los recursos."),
        ],
        expresiones=(
            "Lengua kunza · Agricultura · Alfarería · "
            "Arquitectura en adobe · Relación con montañas, agua y territorio."
        ),
        museo_txt=(
            "Maqueta de oasis · Mapa del río Loa · "
            "Dibujo de salar · Ficha sobre uso del agua · "
            "Muestra de símbolos andinos."
        ),
        pregunta_txt="¿Por qué el agua es tan importante en la vida del pueblo Lickanantay?",
    )

    # ── QUECHUA ───────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluQuechua(AN, 7.2*cm),
        nombre="Pueblo Quechua",
        zona="Norte · Antofagasta · Ollagüe · Alto Loa · Quebradas y Salares",
        color_banner=HexColor('#7A4A20'),
        color_acento=HexColor('#C89040'),
        campos=[
            ("🏔","Territorio",
             "Altiplano, salares, quebradas, vegas y sectores de pastoreo."),
            ("🌡","Clima",
             "Árido y frío de altura, con baja humedad y gran variación térmica."),
            ("⛰","Relieve",
             "Cordillera, altiplano, salares, quebradas y volcanes."),
            ("💧","Agua y recursos",
             "Vegas, lagunas, ríos y campos de pastoreo."),
            ("🌿","Vegetación",
             "Pajonales, tolares y plantas adaptadas a la altura y aridez."),
            ("🏡","Forma de vida",
             "Agricultura, ganadería, pastoreo y vínculos con rutas andinas."),
        ],
        expresiones=(
            "Lengua quechua · Tradición oral · Tejidos · "
            "Agricultura · Pastoreo · Herencia cultural andina."
        ),
        museo_txt=(
            "Mapa de rutas andinas · Ficha de pastoreo · "
            "Dibujo de salar · Glosario de palabras quechuas."
        ),
        pregunta_txt="¿Cómo se relacionan las quebradas y salares con la vida del pueblo Quechua?",
    )

    # ── COLLA ─────────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluColla(AN, 7.2*cm),
        nombre="Pueblo Colla",
        zona="Región de Atacama · Precordillera · Cordillera · Quebradas",
        color_banner=HexColor('#5A3018'),
        color_acento=HexColor('#9A6828'),
        campos=[
            ("🏔","Territorio",
             "Precordillera y Cordillera de los Andes."),
            ("🌡","Clima",
             "Árido en zonas bajas; frío de montaña en zonas altas."),
            ("⛰","Relieve",
             "Cordillera, quebradas, campos de pastoreo de altura y fondos de valle."),
            ("💧","Agua y recursos",
             "Río Jorquera, río de La Sal, aguadas, vegas y quebradas."),
            ("🌿","Vegetación",
             "Cachiyuyo, brea, algarrobo, tolar y pajonal."),
            ("🏡","Forma de vida",
             "Pastoreo, agricultura, recolección y uso de veranadas e invernadas."),
        ],
        expresiones=(
            "Vida de arriería · Relación con animales · "
            "Conocimiento de rutas cordilleranas · Prácticas campesinas de altura."
        ),
        museo_txt=(
            "Mapa de veranadas e invernadas · Dibujo de arriería · "
            "Ficha sobre pastoreo · Maqueta de quebrada."
        ),
        pregunta_txt="¿Por qué la cordillera es importante para la vida del pueblo Colla?",
    )

    # ── DIAGUITA ──────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluDiaguita(AN, 7.2*cm),
        nombre="Pueblo Diaguita",
        zona="Norte Chico · Valles del Huasco y Choapa · Terrazas Agrícolas",
        color_banner=HexColor('#8A4A18'),
        color_acento=HexColor('#C87838'),
        campos=[
            ("🌄","Territorio",
             "Valles transversales, precordillera, quebradas y terrazas agrícolas."),
            ("🌡","Clima",
             "Semiárido, con sectores de desierto frío y desierto de montaña en altura."),
            ("⛰","Relieve",
             "Valles encajonados, quebradas, montañas, precordillera y terrazas."),
            ("💧","Agua y recursos",
             "Ríos Huasco, Tránsito, Carmen, Choapa y afluentes cordilleranos."),
            ("🌿","Vegetación",
             "Hierbas, cactáceas, arbustos, gramíneas y pastos de altura."),
            ("🏡","Forma de vida",
             "El acceso a valles y ríos favoreció la agricultura, los asentamientos y el uso de terrazas."),
        ],
        expresiones=(
            "Alfarería · Diseños geométricos bicolores · "
            "Trabajo agrícola · Identidad territorial · Relación con los valles."
        ),
        museo_txt=(
            "Dibujo de cerámica diaguita · Mapa del valle · "
            "Maqueta de terraza agrícola · Patrón geométrico."
        ),
        pregunta_txt="¿Cómo ayudaron los ríos y valles al desarrollo del pueblo Diaguita?",
    )

    # ── CHANGO ────────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluChango(AN, 7.2*cm),
        nombre="Pueblo Chango",
        zona="Costa Norte · Desierto de Atacama a Coquimbo · Océano Pacífico",
        color_banner=HexColor('#1A4A6A'),
        color_acento=HexColor('#4888A8'),
        campos=[
            ("🌊","Territorio",
             "Franja costera del norte, entre la Cordillera de la Costa, el desierto y el Océano Pacífico."),
            ("🌤","Clima",
             "Costero desértico, con escasas lluvias y presencia de camanchaca."),
            ("⛰","Relieve",
             "Costa, acantilados, playas, desierto costero y Cordillera de la Costa."),
            ("💧","Agua y recursos",
             "Océano Pacífico, Corriente de Humboldt; peces, mariscos, algas, aves y mamíferos marinos."),
            ("🌿","Vegetación",
             "Vegetación costera asociada a la humedad de la camanchaca."),
            ("🏡","Forma de vida",
             "Pesca, recolección de mariscos, navegación y aprovechamiento de recursos marinos."),
        ],
        expresiones=(
            "Embarcaciones · Pesca · Recolección · "
            "Intercambio de productos marinos · Conocimientos del litoral."
        ),
        museo_txt=(
            "Maqueta de costa · Dibujo de embarcación · "
            "Ficha sobre Corriente de Humboldt · "
            "Muestra visual de recursos marinos."
        ),
        pregunta_txt="¿Por qué el mar fue central para la vida del pueblo Chango?",
    )

    # ── RAPA NUI ──────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluRapaNui(AN, 7.2*cm),
        nombre="Pueblo Rapa Nui",
        zona="Isla Rapa Nui · Océano Pacífico Sur",
        color_banner=HexColor('#1A5878'),
        color_acento=HexColor('#4898B8'),
        campos=[
            ("🌋","Territorio",
             "Isla de origen volcánico: costa, cráteres, cuevas, suelos volcánicos y mar abierto."),
            ("🌤","Clima",
             "Subtropical, con temperatura media cercana a 21 °C."),
            ("⛰","Relieve",
             "Volcanes, cráteres, laderas, costa rocosa y zonas interiores."),
            ("💧","Agua y recursos",
             "Sin cauces permanentes; aguas subterráneas y recursos marinos."),
            ("🌿","Vegetación",
             "Actualmente sabana con matorrales; antiguamente mayor presencia de bosques."),
            ("🏡","Forma de vida",
             "El aislamiento insular y el mar influyeron en su organización, navegación, agricultura y cultura."),
        ],
        expresiones=(
            "Lengua rapa nui · Moai · Ahu · Música · "
            "Danza · Relatos · Tallado · Patrimonio arqueológico."
        ),
        museo_txt=(
            "Mapa de la isla · Dibujo de moai · Ficha de volcanes · "
            "Audio musical · Línea de tiempo cultural."
        ),
        pregunta_txt="¿Cómo influye vivir en una isla en la cultura de un pueblo?",
    )

    # ── MAPUCHE ───────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluMapuche(AN, 7.2*cm),
        nombre="Pueblo Mapuche",
        zona="Centro-sur y Sur · Wallmapu · Cordillera · Valle · Costa",
        color_banner=HexColor('#2A5038'),
        color_acento=HexColor('#5A9870'),
        campos=[
            ("🌲","Territorio",
             "Valles, bosques, ríos, lagos, costa, precordillera y cordillera."),
            ("🌧","Clima",
             "Templado, con zonas lluviosas y frías hacia el sur."),
            ("⛰","Relieve",
             "Cordillera, valle central, costa, ríos, lagos, bosques y zonas agrícolas."),
            ("💧","Agua y recursos",
             "Ríos, lagos, bosques, suelos agrícolas y plantas medicinales."),
            ("🌿","Vegetación",
             "Bosque nativo, vegetación templada y plantas de uso alimenticio y medicinal."),
            ("🏡","Forma de vida",
             "Agricultura, recolección, crianza de animales y fuerte vínculo comunitario con el territorio."),
        ],
        expresiones=(
            "Mapudungun · Platería · Tejidos · Relatos · "
            "Música · Medicina tradicional · Ceremonias · Organización comunitaria."
        ),
        museo_txt=(
            "Mapa del Wallmapu · Glosario mapudungun · "
            "Tejido · Símbolo cultural · Relato breve · "
            "Ficha sobre bosque nativo."
        ),
        pregunta_txt="¿Cómo se relaciona el pueblo Mapuche con el territorio y la naturaleza?",
    )

    # ── KAWASHKAR ─────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluKawashkar(AN, 7.2*cm),
        nombre="Pueblo Kawashkar",
        zona="Canales Australes · Golfo de Penas · Canal Cockburn · Magallanes",
        color_banner=HexColor('#102838'),
        color_acento=HexColor('#305878'),
        campos=[
            ("🏝","Territorio",
             "Archipiélagos, islas, canales, fiordos y bosques magallánicos."),
            ("🌧","Clima",
             "Frío, lluvioso y ventoso; inviernos de bajas temperaturas y veranos frescos."),
            ("⛰","Relieve",
             "Canales, islas, montañas, costa irregular y bosques australes."),
            ("💧","Agua y recursos",
             "Canales navegables, mar, fauna marina, peces y moluscos."),
            ("🌿","Vegetación",
             "Bosque magallánico denso y vegetación austral."),
            ("🏡","Forma de vida",
             "Navegación en canoas, movilidad por canales y uso de recursos marinos."),
        ],
        expresiones=(
            "Conocimiento de navegación · Canoas · Relatos · "
            "Campamentos costeros · Relación con el mar austral."
        ),
        museo_txt=(
            "Maqueta de canoa · Mapa de canales australes · "
            "Ficha sobre navegación · "
            "Ambientación sonora de lluvia y mar."
        ),
        pregunta_txt="¿Por qué la navegación fue fundamental para el pueblo Kawashkar?",
    )

    # ── YÁMANA / YAGÁN ────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluYamana(AN, 7.2*cm),
        nombre="Pueblo Yámana o Yagán",
        zona="Sur de Tierra del Fuego · Cabo de Hornos · Canales Fueguinos",
        color_banner=HexColor('#0E2030'),
        color_acento=HexColor('#285070'),
        campos=[
            ("🏝","Territorio",
             "Zona austral extrema: canales fueguinos, islas, costas y archipiélagos."),
            ("❄","Clima",
             "Frío, lluvioso y ventoso, con temperaturas bajas."),
            ("⛰","Relieve",
             "Islas, canales, costa irregular, montañas y sectores boscosos."),
            ("💧","Agua y recursos",
             "Mar, canales, peces, moluscos, aves y mamíferos marinos."),
            ("🌿","Vegetación",
             "Bosque austral y vegetación adaptada al frío y la humedad."),
            ("🏡","Forma de vida",
             "Navegantes de los canales australes: canoa, pesca, recolección y movilidad costera."),
        ],
        expresiones=(
            "Lengua yagán · Relatos · Navegación · Cestería · "
            "Vida familiar en campamentos · Conocimiento del clima austral."
        ),
        museo_txt=(
            "Mapa del Cabo de Hornos · Maqueta de canoa · "
            "Ficha sobre recursos marinos · Audio de paisaje austral."
        ),
        pregunta_txt="¿Cómo influyó el clima frío y el mar en la vida del pueblo Yámana/Yagán?",
    )

    # ── SELK'NAM ──────────────────────────────────────────────────────────────
    story += pagina_pueblo(
        ilu=IluSelknam(AN, 7.2*cm),
        nombre="Pueblo Selk'nam",
        zona="Isla Grande de Tierra del Fuego · Pampa · Bosques · Lagos",
        color_banner=HexColor('#3A1A50'),
        color_acento=HexColor('#7A5A98'),
        campos=[
            ("🏝","Territorio",
             "Praderas ventosas al norte; bosques, montañas y lagos al sur de Tierra del Fuego."),
            ("❄","Clima",
             "Inhóspito: veranos cortos y frescos; inviernos largos, húmedos y fríos."),
            ("⛰","Relieve",
             "Praderas, bosques, montañas, lagos, costa y pampa fueguina."),
            ("💧","Agua y recursos",
             "Lagos, costa, animales terrestres y marinos, moluscos y recursos de la pampa."),
            ("🌿","Vegetación",
             "Pastizales, bosques australes y vegetación adaptada al frío."),
            ("🏡","Forma de vida",
             "Cazadores-recolectores terrestres; movilidad vinculada a guanacos y recursos del territorio."),
        ],
        expresiones=(
            "Relatos · Pintura corporal geométrica · Ceremonias · "
            "Conocimiento del territorio · Sistema de creencias."
        ),
        museo_txt=(
            "Mapa de Tierra del Fuego · Representación respetuosa de pintura corporal · "
            "Ficha sobre guanaco · Paisaje de pampa fueguina."
        ),
        pregunta_txt="¿Cómo se adaptó el pueblo Selk'nam al clima y territorio de Tierra del Fuego?",
    )

    # ── GLOSARIO ──────────────────────────────────────────────────────────────
    # Banner
    t_glos_banner = Table([[Paragraph("Palabras clave para investigar", ST['pres_titulo'])]],
                           colWidths=[AN])
    t_glos_banner.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), HexColor('#5A3018')),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('LINEAFTER',     (0,0),(-1,-1), 5, OCRE),
    ]))
    story.append(t_glos_banner)
    story.append(Spacer(1, 0.3*cm))

    terminos = [
        ("Pueblo originario",
         "Grupo humano que habitaba un territorio antes de la formación del Estado actual "
         "y que mantiene identidad, historia, cultura y formas propias de vida."),
        ("Territorio",
         "Espacio geográfico donde vive o ha vivido una comunidad, incluyendo naturaleza, "
         "recursos, historia y significado cultural."),
        ("Clima",
         "Conjunto de condiciones atmosféricas habituales de un lugar: "
         "temperatura, lluvia, humedad y viento."),
        ("Relieve",
         "Formas de la superficie terrestre: montañas, valles, desiertos, "
         "islas, costas, lagos o cordilleras."),
        ("Vegetación",
         "Conjunto de plantas que crecen en un territorio."),
        ("Recursos naturales",
         "Elementos de la naturaleza que las comunidades utilizan: agua, tierra, "
         "animales, plantas, minerales o productos del mar."),
        ("Identidad cultural",
         "Conjunto de costumbres, lengua, relatos, símbolos, valores y formas de vida "
         "que caracterizan a un pueblo."),
        ("Medioambiente",
         "Conjunto de elementos naturales y sociales que rodean a los seres vivos."),
        ("Interculturalidad",
         "Relación respetuosa entre distintas culturas, reconociendo sus saberes, "
         "derechos e identidades."),
        ("Patrimonio",
         "Bienes, conocimientos, expresiones, tradiciones o lugares que tienen valor "
         "para una comunidad y deben ser transmitidos."),
    ]

    # Distribuir en 2 columnas
    col_izq = terminos[:5]
    col_der = terminos[5:]
    max_r = max(len(col_izq), len(col_der))
    ancho_c = AN/2 - 0.15*cm

    filas_glos = []
    for i in range(max_r):
        celdas = []
        for lst in [col_izq, col_der]:
            if i < len(lst):
                term, defn = lst[i]
                inner = Table([
                    [Paragraph(term, ST['glos_term'])],
                    [Paragraph(defn, ST['glos_def'])],
                ], colWidths=[ancho_c - 0.4*cm])
                inner.setStyle(TableStyle([
                    ('BACKGROUND',    (0,0),(-1,-1), CREMA),
                    ('BOX',           (0,0),(-1,-1), 1, HexColor('#C8A870')),
                    ('LINEBELOW',     (0,0),(0,0),   0.5, TERRACOTA),
                    ('TOPPADDING',    (0,0),(-1,-1), 5),
                    ('BOTTOMPADDING', (0,0),(-1,-1), 5),
                    ('LEFTPADDING',   (0,0),(-1,-1), 8),
                    ('RIGHTPADDING',  (0,0),(-1,-1), 6),
                ]))
                celdas.append(inner)
            else:
                celdas.append(Paragraph('', ST['glos_def']))
        filas_glos.append(celdas)

    t_glos_grid = Table(filas_glos, colWidths=[ancho_c, ancho_c])
    t_glos_grid.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 2),
        ('RIGHTPADDING',  (0,0),(-1,-1), 2),
    ]))
    story.append(t_glos_grid)
    story.append(PageBreak())

    # ── FUENTES CONSULTADAS ───────────────────────────────────────────────────
    t_fuentes_banner = Table(
        [[Paragraph("Fuentes oficiales e institucionales consultadas", ST['pres_titulo'])]],
        colWidths=[AN])
    t_fuentes_banner.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), MARRON),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('LINEAFTER',     (0,0),(-1,-1), 5, OCRE),
    ]))
    story.append(t_fuentes_banner)
    story.append(Spacer(1, 0.4*cm))

    fuentes = [
        ("1", "Biblioteca del Congreso Nacional de Chile. "
              "<i>Ley N° 19.253 sobre protección, fomento y desarrollo de los indígenas.</i>"),
        ("2", "Biblioteca del Congreso Nacional de Chile. Informe: "
              "<i>«Los pueblos indígenas y sus comunidades en Chile: "
              "reconocimiento y distribución geográfica».</i>"),
        ("3", "Ministerio de las Culturas, las Artes y el Patrimonio. "
              "<i>«Recomendaciones para nombrar y escribir sobre pueblos indígenas "
              "y Tribal Afrodescendiente chileno».</i>"),
        ("4", "Museo Chileno de Arte Precolombino / Chile Precolombino. "
              "Secciones de ambiente, localización, historia, economía, "
              "arte y lengua de los pueblos originarios."),
        ("5", "Biblioteca Nacional de Chile / Memoria Chilena."),
        ("6", "Chile Para Niños / Biblioteca Nacional de Chile."),
    ]

    for num, txt in fuentes:
        n_p = Paragraph(num, ST['fuente_num'])
        t_p = Paragraph(txt, ST['fuente_txt'])
        row = Table([[n_p, t_p]], colWidths=[0.7*cm, AN-0.7*cm])
        row.setStyle(TableStyle([
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
            ('LEFTPADDING',   (0,0),(-1,-1), 0),
            ('RIGHTPADDING',  (0,0),(-1,-1), 0),
            ('TOPPADDING',    (0,0),(-1,-1), 4),
            ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ]))
        story.append(row)
        story.append(HRFlowable(width=AN, thickness=0.5,
                                color=HexColor('#C8A870'), spaceAfter=4))

    story.append(Spacer(1, 0.6*cm))

    # Nota final con caja elegante
    nota_txt = (
        "Esta revista fue elaborada con fines educativos. La información está "
        "resumida y adaptada para estudiantes de 7° y 8° básico. "
        "No está destinada a usos comerciales. "
        "Los pueblos originarios presentados son comunidades con historia, "
        "identidad y derechos vigentes en Chile."
    )
    t_nota_final = Table(
        [[Paragraph(nota_txt, ST['nota'])]], colWidths=[AN])
    t_nota_final.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), HexColor('#F5EDD6')),
        ('BOX',           (0,0),(-1,-1), 2, TIERRA),
        ('LINEAFTER',     (0,0),(-1,-1), 5, OCRE),
        ('TOPPADDING',    (0,0),(-1,-1), 12),
        ('BOTTOMPADDING', (0,0),(-1,-1), 12),
        ('LEFTPADDING',   (0,0),(-1,-1), 14),
        ('RIGHTPADDING',  (0,0),(-1,-1), 14),
    ]))
    story.append(t_nota_final)

    return story


# ══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

def main():
    output = "/home/user/ESCUELAHOSPITALGERSSON/Raices_que_nos_unen.pdf"
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.15*cm,
        bottomMargin=1.0*cm,
        title="Raíces que nos unen",
        author="Recurso educativo ABP",
        subject="Pueblos originarios de Chile",
    )
    doc.build(
        construir(),
        onFirstPage=portada,
        onLaterPages=header_footer,
    )
    print(f"PDF generado: {output}")


if __name__ == '__main__':
    main()
