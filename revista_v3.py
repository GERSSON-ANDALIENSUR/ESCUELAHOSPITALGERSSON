"""
Raíces que nos unen — v3 · Diseño revista premium
Canvas directo · Liberation Serif/Sans · Ilustraciones atmosféricas
"""

import math, os
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

W, H = A4  # 595.28 × 841.89

# ── Fuentes ────────────────────────────────────────────────────────────────────
_LIB = "/usr/share/fonts/truetype/liberation"
_DEJ = "/usr/share/fonts/truetype/dejavu"

for name, path in [
    ("SR",  f"{_LIB}/LiberationSerif-Regular.ttf"),
    ("SB",  f"{_LIB}/LiberationSerif-Bold.ttf"),
    ("SI",  f"{_LIB}/LiberationSerif-Italic.ttf"),
    ("SBI", f"{_LIB}/LiberationSerif-BoldItalic.ttf"),
    ("NR",  f"{_LIB}/LiberationSans-Regular.ttf"),
    ("NB",  f"{_LIB}/LiberationSans-Bold.ttf"),
    ("NI",  f"{_LIB}/LiberationSans-Italic.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, path))

# ── Paleta global ──────────────────────────────────────────────────────────────
GOLD   = HexColor('#C08828')
CREAM  = HexColor('#FAF6EE')
DARK   = HexColor('#160E06')
MID    = HexColor('#4A3018')
RULE   = HexColor('#D8C8A0')
GREEN  = HexColor('#2A5A38')
BLUE   = HexColor('#1A4870')
WHITE  = white

# Cada pueblo: (dark_bg, mid_bg, accent, sky_top, sky_bot, name_display)
PUEBLOS = [
  { "nombre":    "Pueblo Aimara / Aymara",
    "zona":      "Norte Grande · Arica y Parinacota · Tarapacá · Antofagasta",
    "dark":      HexColor('#0C1A38'), "mid": HexColor('#1E3A78'),
    "accent":    HexColor('#C88028'), "num": "01",
    "sky_top":   HexColor('#0A1228'), "sky_bot": HexColor('#D04A18'),
    "territorio":"Altiplano, puna, sierra, precordillera, valles altos y bajos.",
    "clima":     "Frío y seco en altura; gran diferencia entre día y noche; lluvias estivales en el altiplano.",
    "relieve":   "Altiplano, cordillera, quebradas y valles de altura.",
    "agua":      "Bofedales, vegas, quebradas; terrazas agrícolas; ganadería de camélidos.",
    "vegetacion":"Pastos de altura, vegetación de bofedales y arbustos adaptados a la aridez.",
    "vida":      "Su vida se vincula a distintos pisos ecológicos. Desarrollaron agricultura en terrazas, pastoreo de camélidos, intercambio entre zonas y organización comunitaria profundamente ligada al territorio.",
    "cultura":   "Lengua aimara · Tejidos · Música · Festividades · Relación con la Pachamama",
    "museo":     "Mapa de pisos ecológicos · tejido andino · dibujo de bofedal · maqueta de terrazas agrícolas",
    "pregunta":  "¿Cómo influye la vida en altura en las actividades del pueblo Aimara/Aymara?",
    "ilufn":     "ilu_aimara",
  },
  { "nombre":    "Pueblo Atacameño o Lickanantay",
    "zona":      "Región de Antofagasta · Salar de Atacama · Río Loa · Oasis",
    "dark":      HexColor('#2A0E06'), "mid": HexColor('#6A2808'),
    "accent":    HexColor('#D08828'), "num": "02",
    "sky_top":   HexColor('#380C04'), "sky_bot": HexColor('#E8A030'),
    "territorio":"Desierto de Atacama, oasis, salares, vegas, bofedales y quebradas.",
    "clima":     "Desértico, de extrema aridez y gran oscilación térmica entre el día y la noche.",
    "relieve":   "Desierto, cordillera, salares, quebradas y oasis.",
    "agua":      "Ríos El Loa, El Salado y Vilama; vegas, bofedales y aguas de quebradas.",
    "vegetacion":"Tolar, pajonal, yareta, algarrobo, tamarugo, chañar y vegetación de oasis.",
    "vida":      "El agua fue la clave de su desarrollo: permitió la agricultura en oasis, el pastoreo y el asentamiento en un territorio de extrema aridez. Su conocimiento del desierto y sus recursos fue profundo.",
    "cultura":   "Lengua kunza · Alfarería · Arquitectura en adobe · Relación con montañas y agua",
    "museo":     "Maqueta de oasis · mapa del río Loa · dibujo de salar · ficha sobre el uso del agua",
    "pregunta":  "¿Por qué el agua es tan importante en la vida del pueblo Lickanantay?",
    "ilufn":     "ilu_lickanantay",
  },
  { "nombre":    "Pueblo Quechua",
    "zona":      "Norte · Antofagasta · Ollagüe · Alto Loa · Quebradas y Salares",
    "dark":      HexColor('#0A1830'), "mid": HexColor('#1E3A60'),
    "accent":    HexColor('#A870A0'), "num": "03",
    "sky_top":   HexColor('#080E20'), "sky_bot": HexColor('#3870B8'),
    "territorio":"Altiplano, salares, quebradas, vegas y sectores de pastoreo de altura.",
    "clima":     "Árido y frío de altura, con baja humedad y gran variación térmica entre el día y la noche.",
    "relieve":   "Cordillera, altiplano, salares, quebradas y volcanes.",
    "agua":      "Vegas, lagunas, ríos y campos de pastoreo.",
    "vegetacion":"Pajonales, tolares y plantas adaptadas a la altura y aridez.",
    "vida":      "Históricamente ligados a la agricultura, la ganadería y el pastoreo. Sus rutas comerciales conectaban distintas zonas del mundo andino, y su herencia cultural comparte raíces con otros pueblos del altiplano.",
    "cultura":   "Lengua quechua · Tradición oral · Tejidos · Pastoreo · Herencia andina",
    "museo":     "Mapa de rutas andinas · ficha de pastoreo · dibujo de salar · glosario quechua",
    "pregunta":  "¿Cómo se relacionan las quebradas y salares con la vida del pueblo Quechua?",
    "ilufn":     "ilu_quechua",
  },
  { "nombre":    "Pueblo Colla",
    "zona":      "Región de Atacama · Precordillera · Cordillera · Quebradas",
    "dark":      HexColor('#1A0A04'), "mid": HexColor('#4A2010'),
    "accent":    HexColor('#B06820'), "num": "04",
    "sky_top":   HexColor('#2A1004'), "sky_bot": HexColor('#D06820'),
    "territorio":"Precordillera y Cordillera de los Andes; sectores de Chañaral, Copiapó y Tierra Amarilla.",
    "clima":     "Árido en zonas bajas; frío de montaña en sectores altos.",
    "relieve":   "Cordillera, quebradas, campos de pastoreo de altura y fondos de valle.",
    "agua":      "Río Jorquera, río de La Sal, aguadas, vegas y quebradas.",
    "vegetacion":"Cachiyuyo, brea, algarrobo, tolar y pajonal.",
    "vida":      "Tradición de pastoreo y arriería en la cordillera. El uso de veranadas e invernadas marcó su movilidad estacional: subían a las alturas en verano y bajaban en invierno, siguiendo los pastos para sus animales.",
    "cultura":   "Arriería · Conocimiento de rutas cordilleranas · Relación con el paisaje de altura",
    "museo":     "Mapa de veranadas e invernadas · dibujo de arriería · ficha de pastoreo",
    "pregunta":  "¿Por qué la cordillera es tan importante para la vida del pueblo Colla?",
    "ilufn":     "ilu_colla",
  },
  { "nombre":    "Pueblo Diaguita",
    "zona":      "Norte Chico · Valles del Huasco y Choapa · Terrazas",
    "dark":      HexColor('#2A0808'), "mid": HexColor('#6A1E10'),
    "accent":    HexColor('#C83A20'), "num": "05",
    "sky_top":   HexColor('#1A2848'), "sky_bot": HexColor('#7898C8'),
    "territorio":"Valles transversales, precordillera, quebradas y terrazas agrícolas.",
    "clima":     "Semiárido, con sectores de desierto frío y desierto de montaña en altura.",
    "relieve":   "Valles encajonados, quebradas, montañas, precordillera y terrazas.",
    "agua":      "Ríos Huasco, Tránsito, Carmen, Choapa y afluentes cordilleranos.",
    "vegetacion":"Hierbas, cactáceas, arbustos, gramíneas y pastos de altura.",
    "vida":      "El acceso a valles y ríos favoreció la agricultura y el uso de terrazas. Su cerámica es uno de los referentes más reconocidos del arte precolombino chileno: diseños geométricos bicolores de gran precisión y belleza.",
    "cultura":   "Alfarería bicolor · Diseños geométricos · Agricultura en terrazas · Identidad de los valles",
    "museo":     "Dibujo de cerámica diaguita · mapa del valle · maqueta de terraza · patrón geométrico",
    "pregunta":  "¿Cómo ayudaron los ríos y valles al desarrollo del pueblo Diaguita?",
    "ilufn":     "ilu_diaguita",
  },
  { "nombre":    "Pueblo Chango",
    "zona":      "Costa Norte · Atacama a Coquimbo · Océano Pacífico",
    "dark":      HexColor('#061428'), "mid": HexColor('#123060'),
    "accent":    HexColor('#40A8D0'), "num": "06",
    "sky_top":   HexColor('#081828'), "sky_bot": HexColor('#4888B8'),
    "territorio":"Franja costera del norte, entre la Cordillera de la Costa, el desierto y el Océano Pacífico.",
    "clima":     "Costero desértico, con escasas lluvias y presencia frecuente de camanchaca.",
    "relieve":   "Costa, acantilados, playas, desierto costero y Cordillera de la Costa.",
    "agua":      "Océano Pacífico y Corriente de Humboldt: peces, mariscos, algas, aves y mamíferos marinos.",
    "vegetacion":"Vegetación costera escasa, favorecida por la humedad de la camanchaca.",
    "vida":      "Su vida giró en torno al mar. Desarrollaron embarcaciones de cuero de lobo marino (balsas), técnicas de pesca y buceo, y un profundo conocimiento de la corriente de Humboldt y sus recursos.",
    "cultura":   "Embarcaciones · Pesca y recolección · Navegación costera · Intercambio de productos marinos",
    "museo":     "Maqueta de costa · dibujo de balsa · ficha sobre la Corriente de Humboldt",
    "pregunta":  "¿Por qué el mar fue central para la vida del pueblo Chango?",
    "ilufn":     "ilu_chango",
  },
  { "nombre":    "Pueblo Rapa Nui",
    "zona":      "Isla Rapa Nui · Océano Pacífico Sur",
    "dark":      HexColor('#0A1020'), "mid": HexColor('#1A2848'),
    "accent":    HexColor('#E08030'), "num": "07",
    "sky_top":   HexColor('#080C18'), "sky_bot": HexColor('#E06020'),
    "territorio":"Isla de origen volcánico: costa, cráteres, cuevas, suelos volcánicos y mar abierto.",
    "clima":     "Subtropical, con temperatura media cercana a 21 °C.",
    "relieve":   "Volcanes, cráteres, laderas, costa rocosa y zonas interiores.",
    "agua":      "Sin cauces permanentes; aguas subterráneas y abundantes recursos marinos.",
    "vegetacion":"Actualmente sabana con matorrales; antiguamente tuvo mayor presencia de bosques.",
    "vida":      "El aislamiento en medio del Pacífico y el mar que la rodea moldearon todo: su navegación, alimentación, organización social y una cultura material extraordinaria. Los moái son expresión de una sociedad compleja.",
    "cultura":   "Lengua rapa nui · Moái · Ahu · Música · Danza · Tallado · Patrimonio arqueológico",
    "museo":     "Mapa de la isla · dibujo de moái · ficha de volcanes · audio musical · línea de tiempo",
    "pregunta":  "¿Cómo influye vivir en una isla en la cultura de un pueblo?",
    "ilufn":     "ilu_rapanui",
  },
  { "nombre":    "Pueblo Mapuche",
    "zona":      "Centro-sur y Sur · Wallmapu · Cordillera · Valle · Costa",
    "dark":      HexColor('#081808'), "mid": HexColor('#1A4020'),
    "accent":    HexColor('#70B858'), "num": "08",
    "sky_top":   HexColor('#101E28'), "sky_bot": HexColor('#7098A8'),
    "territorio":"Valles, bosques, ríos, lagos, costa, precordillera y cordillera.",
    "clima":     "Templado, con zonas lluviosas y frías hacia el sur.",
    "relieve":   "Cordillera, valle central, costa, ríos, lagos, bosques y zonas agrícolas.",
    "agua":      "Ríos, lagos, bosques nativos, suelos agrícolas y plantas medicinales.",
    "vegetacion":"Bosque nativo templado y plantas de uso alimenticio y medicinal.",
    "vida":      "Desarrollaron agricultura, recolección y crianza de animales con un fuerte vínculo comunitario. Su relación con el territorio —el Wallmapu— es parte central de su identidad, filosofía y formas de organización.",
    "cultura":   "Mapudungun · Platería · Tejidos · Relatos · Medicina tradicional · Ceremonias",
    "museo":     "Mapa del Wallmapu · glosario mapudungun · tejido · símbolo · ficha sobre bosque nativo",
    "pregunta":  "¿Cómo se relaciona el pueblo Mapuche con el territorio y la naturaleza?",
    "ilufn":     "ilu_mapuche",
  },
  { "nombre":    "Pueblo Kawashkar",
    "zona":      "Canales Australes · Golfo de Penas · Canal Cockburn · Magallanes",
    "dark":      HexColor('#060C14'), "mid": HexColor('#102030'),
    "accent":    HexColor('#5090B0'), "num": "09",
    "sky_top":   HexColor('#040810'), "sky_bot": HexColor('#304860'),
    "territorio":"Archipiélagos, islas, canales, fiordos y bosques magallánicos.",
    "clima":     "Frío, lluvioso y ventoso; inviernos de bajas temperaturas y veranos frescos.",
    "relieve":   "Canales, islas, montañas, costa irregular y bosques australes.",
    "agua":      "Canales navegables, mar, fauna marina, peces y moluscos costeros.",
    "vegetacion":"Bosque magallánico denso y vegetación austral.",
    "vida":      "Navegantes expertos de los canales del sur. Vivían en constante movimiento sobre sus canoas, moviéndose entre islas y canales en busca de recursos marinos. El mar era su hogar y su camino.",
    "cultura":   "Conocimiento de navegación · Canoas · Relatos · Campamentos costeros",
    "museo":     "Maqueta de canoa · mapa de canales australes · ficha sobre navegación · audio de lluvia y mar",
    "pregunta":  "¿Por qué la navegación fue fundamental para el pueblo Kawashkar?",
    "ilufn":     "ilu_kawashkar",
  },
  { "nombre":    "Pueblo Yámana o Yagán",
    "zona":      "Sur de Tierra del Fuego · Cabo de Hornos · Canales Fueguinos",
    "dark":      HexColor('#040810'), "mid": HexColor('#0C1820'),
    "accent":    HexColor('#4880A8'), "num": "10",
    "sky_top":   HexColor('#020608'), "sky_bot": HexColor('#203848'),
    "territorio":"Zona austral extrema: canales fueguinos, islas, costas y archipiélagos del Cabo de Hornos.",
    "clima":     "Frío, lluvioso y ventoso, con temperaturas bajas.",
    "relieve":   "Islas, canales, costa irregular, montañas y sectores boscosos.",
    "agua":      "Mar, canales, peces, moluscos, aves y mamíferos marinos.",
    "vegetacion":"Bosque austral y vegetación adaptada al frío y la humedad extremos.",
    "vida":      "Navegantes de los canales del extremo sur. Su vida se organizaba en torno a la canoa: la pesca, la recolección y el movimiento constante por los canales más australes del planeta.",
    "cultura":   "Lengua yagán · Relatos · Cestería · Navegación · Conocimiento del clima austral",
    "museo":     "Mapa del Cabo de Hornos · maqueta de canoa · ficha de recursos marinos · audio austral",
    "pregunta":  "¿Cómo influyó el clima frío y el mar en la vida del pueblo Yámana/Yagán?",
    "ilufn":     "ilu_yamana",
  },
  { "nombre":    "Pueblo Selk'nam",
    "zona":      "Isla Grande de Tierra del Fuego · Pampa · Bosques · Lagos",
    "dark":      HexColor('#120C1E'), "mid": HexColor('#2A1840'),
    "accent":    HexColor('#C04020'), "num": "11",
    "sky_top":   HexColor('#0E0818'), "sky_bot": HexColor('#706080'),
    "territorio":"Praderas ventosas al norte; bosques, montañas y lagos al sur de Tierra del Fuego.",
    "clima":     "Inhóspito: veranos cortos y frescos; inviernos largos, húmedos y fríos.",
    "relieve":   "Praderas, bosques, montañas, lagos, costa y pampa fueguina.",
    "agua":      "Lagos, costa, animales terrestres y marinos, moluscos y recursos de la pampa.",
    "vegetacion":"Pastizales, bosques australes y vegetación adaptada al frío.",
    "vida":      "Cazadores-recolectores terrestres que recorrían la isla Grande en busca de guanacos y otros recursos. Su conocimiento del territorio era preciso y profundo. Fueron los habitantes más australes del planeta.",
    "cultura":   "Relatos · Pintura corporal geométrica · Ceremonias · Conocimiento del territorio",
    "museo":     "Mapa de Tierra del Fuego · representación respetuosa de pintura corporal · ficha del guanaco",
    "pregunta":  "¿Cómo se adaptó el pueblo Selk'nam al clima y territorio de Tierra del Fuego?",
    "ilufn":     "ilu_selknam",
  },
]

# ══════════════════════════════════════════════════════════════════════════════
# UTILIDADES DE TEXTO
# ══════════════════════════════════════════════════════════════════════════════

def wrap(text, font, size, max_w):
    words = text.split()
    lines, cur, cw = [], [], 0
    sp = stringWidth(' ', font, size)
    for w in words:
        ww = stringWidth(w, font, size)
        if cur and cw + sp + ww > max_w:
            lines.append(' '.join(cur)); cur, cw = [w], ww
        else:
            cur.append(w); cw += (sp if cur[:-1] else 0) + ww
    if cur: lines.append(' '.join(cur))
    return lines

def put(c, text, x, y, font, size, color, max_w=None, leading=None, align='left'):
    """Draw (possibly wrapped) text. Returns bottom-left y after last line."""
    if leading is None: leading = size * 1.35
    c.setFillColor(color); c.setFont(font, size)
    lines = wrap(text, font, size, max_w) if max_w else [text]
    for i, ln in enumerate(lines):
        if align == 'center':
            c.drawCentredString(x, y - i*leading, ln)
        elif align == 'right':
            c.drawRightString(x, y - i*leading, ln)
        else:
            c.drawString(x, y - i*leading, ln)
    return y - (len(lines)-1)*leading - leading

def tracked(c, text, x, y, font, size, color, spacing=1.5):
    """Draw text with letter spacing."""
    c.setFillColor(color); c.setFont(font, size)
    cx = x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += stringWidth(ch, font, size) + spacing
    return cx

# ══════════════════════════════════════════════════════════════════════════════
# PRIMITIVAS DE DIBUJO
# ══════════════════════════════════════════════════════════════════════════════

def sky_gradient(c, x, y, w, h, col_top, col_bot, steps=18):
    for i in range(steps):
        t = i / steps
        r = col_top.red   + t*(col_bot.red   - col_top.red)
        g = col_top.green + t*(col_bot.green - col_top.green)
        b = col_top.blue  + t*(col_bot.blue  - col_top.blue)
        c.setFillColor(Color(r, g, b))
        sh = h / steps + 1
        c.rect(x, y + h - (i+1)*sh, w, sh+1, fill=1, stroke=0)

def dark_overlay(c, x, y, w, h, steps=14):
    """Dark gradient overlay from bottom (for text legibility)."""
    for i in range(steps):
        t = i / steps
        alpha = 0.72 * (1 - t*t)
        c.setFillColor(Color(0.06, 0.04, 0.02, alpha))
        c.rect(x, y + i*(h/steps), w, h/steps+2, fill=1, stroke=0)

def poly(c, pts, color, stroke_col=None, lw=0):
    c.setFillColor(color)
    if stroke_col: c.setStrokeColor(stroke_col); c.setLineWidth(lw)
    path = c.beginPath()
    path.moveTo(*pts[0])
    for pt in pts[1:]: path.lineTo(*pt)
    path.close()
    c.drawPath(path, fill=1, stroke=1 if stroke_col else 0)

def mountain_range(c, peaks_xy, base_y, color):
    pts = [(0, base_y)] + peaks_xy + [(W, base_y)]
    poly(c, pts, color)

def wave_strip(c, base_y, amp, freq, col, lw=1.2, n=120):
    c.setStrokeColor(col); c.setLineWidth(lw)
    p = c.beginPath()
    for i in range(n+1):
        x = W * i / n
        y = base_y + amp * math.sin(2*math.pi*freq*i/n)
        p.moveTo(x, y) if i==0 else p.lineTo(x, y)
    c.drawPath(p, stroke=1, fill=0)

def star(c, x, y, r=1.8):
    c.setFillColor(HexColor('#FFFFFF'))
    c.circle(x, y, r, fill=1, stroke=0)

def stars_field(c, positions):
    for sx, sy, sr in positions: star(c, sx, sy, sr)

def horiz_rule(c, x, y, w, col, lw=0.6):
    c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x, y, x+w, y)

def pill(c, x, y, w, h, col, radius=3):
    c.setFillColor(col)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

# ══════════════════════════════════════════════════════════════════════════════
# ILUSTRACIONES  (dibujan en zona: x=0..W, y=base..base+h)
# ══════════════════════════════════════════════════════════════════════════════

def ilu_aimara(c, base, h):
    sky_gradient(c, 0, base, W, h, HexColor('#080F28'), HexColor('#B83808'))
    # Estrellas
    stars_field(c, [(W*.06,base+h*.88,1.8),(W*.14,base+h*.94,1.4),(W*.22,base+h*.87,2.0),
                    (W*.38,base+h*.93,1.5),(W*.52,base+h*.90,1.8),(W*.65,base+h*.86,1.4),
                    (W*.78,base+h*.92,1.9),(W*.90,base+h*.89,1.4),(W*.45,base+h*.97,1.2)])
    # Luna
    c.setFillColor(HexColor('#F8E8C0')); c.circle(W*.82, base+h*.88, h*.035, fill=1, stroke=0)
    c.setFillColor(HexColor('#280A04')); c.circle(W*.825, base+h*.885, h*.026, fill=1, stroke=0)
    # Cordillera lejana (azul grisáceo claro)
    mountain_range(c,[(W*.00,base+h*.58),(W*.08,base+h*.72),(W*.18,base+h*.60),
                      (W*.30,base+h*.76),(W*.42,base+h*.63),(W*.55,base+h*.74),
                      (W*.68,base+h*.60),(W*.80,base+h*.70),(W*.92,base+h*.57),(W,base+h*.62)],
                   base+h*.30, HexColor('#3A4860'))
    # Nieve
    for mx,my in [(W*.08,h*.72),(W*.30,h*.76),(W*.55,h*.74),(W*.80,h*.70)]:
        c.setFillColor(HexColor('#C8D8EC'))
        pts=[(mx-W*.025,base+my),(mx,base+my+h*.05),(mx+W*.025,base+my)]
        poly(c, pts, HexColor('#D0DFF0'))
    # Cordillera media (café morado)
    mountain_range(c,[(W*.00,base+h*.48),(W*.12,base+h*.62),(W*.24,base+h*.50),
                      (W*.38,base+h*.64),(W*.52,base+h*.52),(W*.66,base+h*.62),
                      (W*.78,base+h*.48),(W*.90,base+h*.58),(W,base+h*.46)],
                   base+h*.28, HexColor('#3A2848'))
    # Altiplano base
    c.setFillColor(HexColor('#283820'))
    c.rect(0, base, W, h*.30, fill=1, stroke=0)
    # Bofedal (verde brillante)
    c.setFillColor(HexColor('#48784A'))
    c.ellipse(W*.05,base+h*.12, W*.48,base+h*.26, fill=1, stroke=0)
    c.setFillColor(HexColor('#5A9050'))
    c.ellipse(W*.08,base+h*.14, W*.44,base+h*.24, fill=1, stroke=0)
    # Agua del bofedal
    c.setFillColor(HexColor('#284868'))
    c.ellipse(W*.12,base+h*.155, W*.38,base+h*.215, fill=1, stroke=0)
    wave_strip(c, base+h*.185, h*.008, 5, HexColor('#4878A0'), 0.6)
    # Dos llamas
    for ox in [W*.62, W*.74]:
        s = h*.12
        c.setFillColor(HexColor('#C8A060'))
        c.ellipse(ox, base+h*.08, ox+s*1.8, base+h*.08+s*.9, fill=1, stroke=0)
        c.rect(ox+s*1.1, base+h*.08+s*.7, s*.4, s*.9, fill=1, stroke=0)
        c.ellipse(ox+s*.9, base+h*.08+s*1.4, ox+s*1.6, base+h*.08+s*1.9, fill=1, stroke=0)
        for px in [ox+s*.2,ox+s*.6,ox+s*1.0,ox+s*1.4]:
            c.rect(px, base, s*.15, s*.55, fill=1, stroke=0)
    # Chakana dorada en el cielo
    cx,cy,r = W*.88, base+h*.72, h*.07
    c.setFillColor(HexColor('#C8882040'))
    for ang in [0,90]:
        c.rect(cx-r*(0.33 if ang==90 else 1), cy-r*(1 if ang==90 else 0.33),
               r*(0.66 if ang==90 else 2), r*(2 if ang==90 else 0.66), fill=1, stroke=0)

def ilu_lickanantay(c, base, h):
    sky_gradient(c, 0, base, W, h, HexColor('#2E0A02'), HexColor('#F0A828'))
    # Sol naciente
    c.setFillColor(HexColor('#F8D060')); c.circle(W*.75, base+h*.85, h*.09, fill=1, stroke=0)
    c.setFillColor(HexColor('#FCE898')); c.circle(W*.75, base+h*.85, h*.06, fill=1, stroke=0)
    # Volcanes (conos simples, muy atmosféricos)
    for vx,vh,vc in [(W*.10,h*.72,HexColor('#5A2808')),(W*.32,h*.80,HexColor('#703010')),
                     (W*.60,h*.70,HexColor('#5A2808')),(W*.85,h*.75,HexColor('#6A3010'))]:
        pts=[(vx-vh*.45,base+h*.30),(vx,base+vh),(vx+vh*.45,base+h*.30)]
        poly(c, pts, vc)
        # Nieve
        pts2=[(vx-vh*.08,base+vh-h*.04),(vx,base+vh),(vx+vh*.08,base+vh-h*.04)]
        poly(c, pts2, HexColor('#F0E8D8'))
    # Desierto
    c.setFillColor(HexColor('#C89050')); c.rect(0,base,W,h*.32,fill=1,stroke=0)
    c.setFillColor(HexColor('#D8A868')); c.rect(0,base,W,h*.18,fill=1,stroke=0)
    # Salar (hexágonos)
    c.setFillColor(HexColor('#E8E0D0'))
    c.rect(0,base,W*.52,h*.22,fill=1,stroke=0)
    hs=h*.040
    for row in range(6):
        for col_i in range(14):
            hx=hs; ox=col_i*hx*1.74+(row%2)*hx*.87; oy=row*hx*1.52
            pts=[(ox+hx*math.cos(math.pi/6+math.pi/3*i),
                  base+oy+hx*math.sin(math.pi/6+math.pi/3*i)) for i in range(6)]
            c.setFillColor(HexColor('#C8C0B0'))
            c.setStrokeColor(HexColor('#B8B0A0')); c.setLineWidth(0.3)
            path=c.beginPath(); path.moveTo(*pts[0])
            [path.lineTo(*p) for p in pts[1:]]; path.close()
            c.drawPath(path,fill=1,stroke=1)
    # Oasis
    c.setFillColor(HexColor('#3A7030'))
    c.ellipse(W*.60,base+h*.12,W*.82,base+h*.28,fill=1,stroke=0)
    c.setFillColor(HexColor('#508A40'))
    c.ellipse(W*.63,base+h*.14,W*.79,base+h*.26,fill=1,stroke=0)
    # Palmera
    px,py_b=W*.695,base+h*.10; ph=h*.22
    c.setFillColor(HexColor('#6A4010')); c.rect(px,py_b,ph*.07,ph*.60,fill=1,stroke=0)
    for ang in [-55,-30,-5,20,45,70]:
        r=math.radians(ang+90); lx=px+ph*.035+ph*.38*math.cos(r); ly=py_b+ph*.60+ph*.38*math.sin(r)
        c.setStrokeColor(HexColor('#2A6818')); c.setLineWidth(2.5)
        p=c.beginPath(); p.moveTo(px+ph*.035,py_b+ph*.60); p.lineTo(lx,ly)
        c.drawPath(p,stroke=1,fill=0)
    # Río
    c.setStrokeColor(HexColor('#5898C8')); c.setLineWidth(3)
    p=c.beginPath(); p.moveTo(W*.15,base+h*.16)
    p.curveTo(W*.28,base+h*.12,W*.38,base+h*.18,W*.50,base+h*.15)
    c.drawPath(p,stroke=1,fill=0)

def ilu_quechua(c, base, h):
    sky_gradient(c, 0, base, W, h, HexColor('#060A18'), HexColor('#1A3060'))
    # Vía Láctea
    import random; random.seed(7)
    for _ in range(80):
        sx=random.random()*W; sy=base+h*.45+random.random()*h*.50
        r=random.random()*1.6+0.4
        c.setFillColor(HexColor('#FFFFFF' if random.random()>.5 else '#C8D8F0'))
        c.circle(sx,sy,r,fill=1,stroke=0)
    # Volcán nevado prominente (izquierda)
    pts=[(W*.08,base+h*.38),(W*.22,base+h*.82),(W*.36,base+h*.38)]
    poly(c,pts,HexColor('#3A3048'))
    poly(c,[(W*.18,base+h*.76),(W*.22,base+h*.82),(W*.26,base+h*.76)],HexColor('#E0E8F8'))
    # Cordillera derecha
    mountain_range(c,[(W*.40,base+h*.42),(W*.52,base+h*.64),(W*.62,base+h*.50),
                      (W*.72,base+h*.68),(W*.84,base+h*.52),(W*.94,base+h*.62),(W,base+h*.50)],
                   base+h*.32, HexColor('#2A2038'))
    # Salar reflectante (cielo reflejado)
    c.setFillColor(HexColor('#1028508A'))
    sky_gradient(c,0,base,W*.55,h*.34,HexColor('#102040'),HexColor('#3060A0'))
    wave_strip(c,base+h*.10,h*.012,4,HexColor('#3868A880'),0.7)
    wave_strip(c,base+h*.20,h*.009,3,HexColor('#2858A060'),0.5)
    # Altiplano
    c.setFillColor(HexColor('#282018')); c.rect(0,base,W,h*.34,fill=1,stroke=0)
    # Terrazas (izquierda)
    for i,ty in enumerate([h*.30,h*.26,h*.22,h*.18]):
        c.setFillColor(HexColor(f'#{0x40+i*0x0C:02x}{0x38+i*0x06:02x}10'))
        c.rect(0,base+ty,W*(0.22-i*.03),h*.04+1,fill=1,stroke=0)
    # Patrón textil (banda superior)
    bh=h*.062; by=base+h*(1-bh/h*1.5)
    cols=[HexColor('#A82810'),HexColor('#C87020'),HexColor('#8A1E08'),
          HexColor('#C87020'),HexColor('#A82810')]
    cw=W/len(cols)
    for i,col in enumerate(cols):
        c.setFillColor(col); c.rect(i*cw,base+h-bh,cw,bh,fill=1,stroke=0)
    rh=bh/2
    for i in range(int(W/(rh*1.6))+2):
        cx2=i*rh*1.6+rh*.8; cy2=base+h-bh+bh/2
        pts=[(cx2,cy2+rh*.45),(cx2+rh*.45,cy2),(cx2,cy2-rh*.45),(cx2-rh*.45,cy2)]
        poly(c,pts,HexColor('#F0E090'))

def ilu_colla(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#1E0802'),HexColor('#D86820'))
    # Cordillera abrupta
    mountain_range(c,[(W*.00,base+h*.50),(W*.10,base+h*.70),(W*.20,base+h*.56),
                      (W*.32,base+h*.74),(W*.44,base+h*.58),(W*.56,base+h*.72),
                      (W*.68,base+h*.54),(W*.80,base+h*.68),(W*.92,base+h*.52),(W,base+h*.58)],
                   base+h*.34, HexColor('#6A3A18'))
    mountain_range(c,[(W*.00,base+h*.42),(W*.14,base+h*.56),(W*.28,base+h*.46),
                      (W*.44,base+h*.58),(W*.60,base+h*.44),(W*.76,base+h*.56),(W,base+h*.42)],
                   base+h*.28, HexColor('#7E4E28'))
    # Quebrada central (sombra profunda)
    c.setFillColor(HexColor('#1A0C06'))
    pts=[(W*.42,base+h*.56),(W*.46,base+h*.28),(W*.54,base+h*.28),(W*.58,base+h*.56)]
    poly(c,pts,HexColor('#180A04'))
    # Río
    c.setStrokeColor(HexColor('#6898B8')); c.setLineWidth(2)
    p=c.beginPath(); p.moveTo(W*.50,base+h*.28)
    p.curveTo(W*.49,base+h*.14,W*.51,base+h*.08,W*.50,base)
    c.drawPath(p,stroke=1,fill=0)
    # Suelo
    c.setFillColor(HexColor('#B87840')); c.rect(0,base,W,h*.28,fill=1,stroke=0)
    c.setFillColor(HexColor('#A86830')); c.rect(0,base,W,h*.15,fill=1,stroke=0)
    # Cactus
    for cx2 in [W*.08,W*.18,W*.72,W*.84,W*.92]:
        ch=h*.18; c.setFillColor(HexColor('#507030'))
        c.rect(cx2,base+h*.06,ch*.12,ch,fill=1,stroke=0)
        c.rect(cx2-ch*.22,base+h*.06+ch*.45,ch*.22,ch*.12,fill=1,stroke=0)
        c.rect(cx2+ch*.12,base+h*.06+ch*.55,ch*.22,ch*.12,fill=1,stroke=0)
    # Camino de arriería
    c.setStrokeColor(HexColor('#8A5828')); c.setLineWidth(1.5)
    p=c.beginPath(); p.moveTo(0,base+h*.12)
    p.curveTo(W*.20,base+h*.16,W*.40,base+h*.10,W*.60,base+h*.13)
    p.curveTo(W*.75,base+h*.16,W*.88,base+h*.11,W,base+h*.14)
    c.drawPath(p,stroke=1,fill=0)

def ilu_diaguita(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#1A2848'),HexColor('#7898C0'))
    # Montañas al fondo (azul púrpura)
    mountain_range(c,[(W*.00,base+h*.50),(W*.12,base+h*.68),(W*.26,base+h*.54),
                      (W*.40,base+h*.70),(W*.54,base+h*.56),(W*.68,base+h*.66),
                      (W*.80,base+h*.52),(W*.92,base+h*.62),(W,base+h*.48)],
                   base+h*.32, HexColor('#6A5870'))
    # Valles (verde)
    pts=[(W*.24,base+h*.52),(W*.20,base),(W*.80,base),(W*.76,base+h*.52)]
    poly(c,pts,HexColor('#7A9050'))
    pts2=[(W*.32,base+h*.52),(W*.28,base),(W*.72,base),(W*.68,base+h*.52)]
    poly(c,pts2,HexColor('#8AA858'))
    # Río azul
    c.setFillColor(HexColor('#3A88D0'))
    pts3=[(W*.44,base+h*.52),(W*.42,base),(W*.58,base),(W*.56,base+h*.52)]
    poly(c,pts3,HexColor('#4898E0'))
    wave_strip(c,base+h*.10,h*.014,6,HexColor('#70B8E8'),0.8)
    # Terreno base
    c.setFillColor(HexColor('#9A8060')); c.rect(0,base,W,h*.32,fill=1,stroke=0)
    # PATRÓN CERÁMICA DIAGUITA (banda superior — reconocible)
    bh=h*.088; by=base+h-bh
    c.setFillColor(HexColor('#C02818')); c.rect(0,by,W,bh,fill=1,stroke=0)
    n=int(W/(bh*1.0)); tw=W/n
    for i in range(n+1):
        col=HexColor('#101008') if i%2==0 else HexColor('#F0E0A8')
        pts=[(i*tw,by),(i*tw+tw/2,by+bh),(i*tw+tw,by)]
        poly(c,pts,col)
    # Línea central blanca
    horiz_rule(c,0,by+bh/2,W,HexColor('#F8F0D8'),1.0)
    # Rombos
    for i in range(n):
        cx3=i*tw+tw/2; cy3=by+bh/2; r=bh*.28
        pts=[(cx3,cy3+r),(cx3+r,cy3),(cx3,cy3-r),(cx3-r,cy3)]
        poly(c,pts,HexColor('#F8F0D8'))

def ilu_chango(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#060E1A'),HexColor('#5898C8'))
    # Sol
    c.setFillColor(HexColor('#F8D060')); c.circle(W*.80,base+h*.85,h*.075,fill=1,stroke=0)
    c.setFillColor(HexColor('#FEF0A8')); c.circle(W*.80,base+h*.85,h*.050,fill=1,stroke=0)
    # Cordillera costera (silueta oscura)
    mountain_range(c,[(W*.00,base+h*.55),(W*.08,base+h*.68),(W*.18,base+h*.58),
                      (W*.30,base+h*.64),(W*.38,base+h*.54),(W*.46,base+h*.48)],
                   base, HexColor('#5A4030'))
    c.setFillColor(HexColor('#5A4030')); c.rect(0,base,W*.46,h*.48+2,fill=1,stroke=0)
    # Océano
    c.setFillColor(HexColor('#0D2E58')); c.rect(W*.26,base,W*.74,h*.44,fill=1,stroke=0)
    # Corriente Humboldt (banda de azul más claro)
    c.setFillColor(HexColor('#1848788A'))
    c.rect(W*.26,base+h*.10,W*.74,h*.14,fill=1,stroke=0)
    # Olas
    for i,(wy,amp,col) in enumerate([(h*.08,h*.018,HexColor('#3878B0')),
                                      (h*.18,h*.022,HexColor('#4888C0')),
                                      (h*.28,h*.026,HexColor('#5898D0')),
                                      (h*.38,h*.020,HexColor('#60A0D8'))]):
        wave_strip(c,base+wy,amp,3+i*.4,col,1.0+i*.2)
    # Crestas blancas
    wave_strip(c,base+h*.38,h*.020,3.4,HexColor('#FFFFFF60'),0.5)
    # Balsa (embarcación chango)
    bx,by2=W*.62,base+h*.34; bs=h*.10
    c.setFillColor(HexColor('#C09060')); c.ellipse(bx-bs,by2,bx+bs,by2+bs*.38,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#7A5020')); c.setLineWidth(1.5)
    c.line(bx,by2+bs*.38,bx,by2+bs*1.3)
    c.setFillColor(HexColor('#E8D8A070'))
    pts=[(bx,by2+bs*.42),(bx+bs*.9,by2+bs*.85),(bx,by2+bs*1.25)]
    poly(c,pts,HexColor('#E8D8A070'))
    # Pelícanos
    for bx2,by3 in [(W*.40,base+h*.52),(W*.48,base+h*.55),(W*.53,base+h*.51)]:
        c.setFillColor(HexColor('#1A2830'))
        c.ellipse(bx2,by3,bx2+h*.04,by3+h*.018,fill=1,stroke=0)
        c.setStrokeColor(HexColor('#1A2830')); c.setLineWidth(1.5)
        c.line(bx2+h*.005,by3+h*.009,bx2-h*.04,by3+h*.016)
        c.line(bx2+h*.035,by3+h*.009,bx2+h*.08,by3+h*.016)
    # Camanchaca
    c.setFillColor(HexColor('#98B8C83A'))
    c.rect(0,base+h*.42,W*.44,h*.12,fill=1,stroke=0)

def ilu_rapanui(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#080C14'),HexColor('#D84810'))
    # Estrellas
    stars_field(c,[(W*.05,base+h*.90,2.0),(W*.15,base+h*.94,1.5),(W*.28,base+h*.88,1.8),
                   (W*.42,base+h*.92,1.4),(W*.58,base+h*.86,2.2),(W*.70,base+h*.91,1.6),
                   (W*.82,base+h*.93,1.3),(W*.92,base+h*.87,1.8)])
    # Océano
    c.setFillColor(HexColor('#081828')); c.rect(0,base,W,h*.32,fill=1,stroke=0)
    wave_strip(c,base+h*.08,h*.016,3.5,HexColor('#1848788A'),1)
    wave_strip(c,base+h*.18,h*.014,3,HexColor('#204A808A'),0.8)
    # Isla (silueta)
    c.setFillColor(HexColor('#1E3A18'))
    pts=[(0,base+h*.30),(W*.06,base+h*.38),(W*.18,base+h*.42),(W*.35,base+h*.39),
         (W*.55,base+h*.43),(W*.72,base+h*.38),(W*.88,base+h*.40),(W,base+h*.32),(W,base+h*.30)]
    poly(c,pts,HexColor('#1E3A18'))
    c.setFillColor(HexColor('#1E3A18')); c.rect(0,base,W,h*.30+2,fill=1,stroke=0)
    # Volcán Rano Raraku
    pts2=[(W*.62,base+h*.38),(W*.72,base+h*.62),(W*.82,base+h*.38)]
    poly(c,pts2,HexColor('#2E5028'))
    c.setFillColor(HexColor('#2E5028')); c.rect(W*.62,base,W*.20,h*.38+2,fill=1,stroke=0)
    # AHU (plataforma de piedra)
    c.setFillColor(HexColor('#5A4028')); c.rect(W*.06,base+h*.36,W*.50,h*.038,fill=1,stroke=0)
    c.setFillColor(HexColor('#4A3018')); c.rect(W*.06,base+h*.34,W*.50,h*.025,fill=1,stroke=0)
    # Tres moái (siluetas majestuosas)
    for mx,mh,mw in [(W*.12,h*.36,h*.080),(W*.24,h*.42,h*.095),(W*.38,h*.32,h*.072)]:
        my=base+h*.375
        c.setFillColor(HexColor('#60483A'))
        # Cuerpo
        c.rect(mx,my,mw,mh*.55,fill=1,stroke=0)
        # Cabeza
        c.rect(mx+mw*.06,my+mh*.52,mw*.88,mh*.40,fill=1,stroke=0)
        # Nariz prominente
        c.setFillColor(HexColor('#504030'))
        c.rect(mx+mw*.30,my+mh*.63,mw*.30,mh*.16,fill=1,stroke=0)
        # Ojos
        c.setFillColor(HexColor('#181008'))
        c.rect(mx+mw*.14,my+mh*.80,mw*.25,mh*.08,fill=1,stroke=0)
        c.rect(mx+mw*.58,my+mh*.80,mw*.25,mh*.08,fill=1,stroke=0)
    # Sol/luna sobre el mar
    c.setFillColor(HexColor('#F07820'))
    c.circle(W*.82,base+h*.40,h*.10,fill=1,stroke=0)
    c.setFillColor(HexColor('#F8A840'))
    c.circle(W*.82,base+h*.40,h*.072,fill=1,stroke=0)
    # Reflejo del sol en el agua
    c.setFillColor(HexColor('#E0600808'))
    c.ellipse(W*.72,base+h*.10,W*.92,base+h*.30,fill=1,stroke=0)

def ilu_mapuche(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#101820'),HexColor('#8098A8'))
    # Nubes grises
    for nx,ny_r,nr in [(W*.15,h*.88,h*.06),(W*.38,h*.92,h*.08),(W*.62,h*.86,h*.07),(W*.85,h*.90,h*.055)]:
        c.setFillColor(HexColor('#6A7880'))
        for dx,dy,r in [(0,0,nr),(.7*nr,.05*h,.85*nr),(-.6*nr,-.02*h,.75*nr),(.35*nr,.08*h,.65*nr)]:
            c.circle(nx+dx,base+ny_r+dy,r,fill=1,stroke=0)
    # Cordillera nevada al fondo (derecha)
    mountain_range(c,[(W*.50,base+h*.40),(W*.58,base+h*.60),(W*.66,base+h*.44),
                      (W*.74,base+h*.64),(W*.82,base+h*.48),(W*.90,base+h*.58),(W,base+h*.44)],
                   base+h*.30, HexColor('#7888A0'))
    # Nieve en cimas
    for mx,my in [(W*.58,h*.60),(W*.74,h*.64)]:
        poly(c,[(mx-W*.03,base+my),(mx,base+my+h*.07),(mx+W*.03,base+my)],HexColor('#DDE4EE'))
    # Bosque nativo (oscuro, denso)
    c.setFillColor(HexColor('#1A3018')); c.rect(0,base,W,h*.38,fill=1,stroke=0)
    # Árboles (araucarias, coihues)
    for tx in range(0,int(W),int(W/16)):
        tx2=tx+int(W/32); th2=h*(0.18+0.08*((tx//int(W/16))%3)*.5)
        c.setFillColor(HexColor('#204020'))
        c.rect(tx2-th2*.06,base,th2*.12,th2*.40,fill=1,stroke=0)
        for lvl in range(3):
            c.setFillColor(HexColor(f'#{0x22+lvl*0x0C:02x}{0x48+lvl*0x08:02x}1{lvl*4:01x}'))
            pts=[(tx2-th2*(0.30-lvl*.04),base+th2*(0.25+lvl*.18)),
                 (tx2,base+th2*(0.72+lvl*.10)),
                 (tx2+th2*(0.30-lvl*.04),base+th2*(0.25+lvl*.18))]
            poly(c,pts,HexColor(f'#{0x22+lvl*0x0C:02x}{0x48+lvl*0x08:02x}10'))
    # Lago (izquierda)
    c.setFillColor(HexColor('#2858A0'))
    c.ellipse(W*.52,base+h*.06,W*.92,base+h*.25,fill=1,stroke=0)
    wave_strip(c,base+h*.155,h*.012,5,HexColor('#4878C0'),0.8)
    # Kultrun (símbolo central del cielo)
    kx,ky,kr = W*.88, base+h*.72, h*.082
    c.setFillColor(HexColor('#C89050')); c.circle(kx,ky,kr,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#7A4018')); c.setLineWidth(1.8)
    c.circle(kx,ky,kr,fill=0,stroke=1)
    c.line(kx-kr,ky,kx+kr,ky); c.line(kx,ky-kr,kx,ky+kr)
    for ang in [45,135,225,315]:
        r=math.radians(ang); c.setFillColor(HexColor('#7A4018'))
        c.circle(kx+kr*.60*math.cos(r),ky+kr*.60*math.sin(r),kr*.20,fill=1,stroke=0)
    c.setFillColor(HexColor('#F0C868')); c.setLineWidth(1)
    c.circle(kx,ky,kr*.80,fill=0,stroke=1)

def ilu_kawashkar(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#02060E'),HexColor('#283848'))
    # Nubes tormentosas densas
    for nx,ny_r,ns in [(W*.08,h*.82,1.0),(W*.25,h*.88,1.2),(W*.48,h*.84,1.1),
                       (W*.68,h*.90,1.0),(W*.88,h*.85,0.9)]:
        for dx,dy,r in [(0,0,h*.07*ns),(h*.08*ns,h*.02,h*.065*ns),
                        (-h*.07*ns,-h*.01,h*.06*ns),(h*.04*ns,h*.07*ns,h*.055*ns)]:
            c.setFillColor(HexColor('#1A2430')); c.circle(nx+dx,base+ny_r+dy,r,fill=1,stroke=0)
    # Lluvia
    import random; random.seed(42)
    c.setStrokeColor(HexColor('#4878A030')); c.setLineWidth(0.6)
    for _ in range(120):
        rx=random.random()*W; ry=random.random()*h*.72
        c.line(rx,base+ry,rx+h*.022,base+ry-h*.062)
    # Canales (agua oscura)
    c.setFillColor(HexColor('#0C1E2C')); c.rect(0,base,W,h*.36,fill=1,stroke=0)
    wave_strip(c,base+h*.10,h*.018,4,HexColor('#203848'),0.8)
    wave_strip(c,base+h*.22,h*.016,3.5,HexColor('#284858'),0.7)
    # Islas con bosque magallánico
    for ix,iw,ih2,iy in [(0,W*.24,h*.28,h*.33),(W*.30,W*.18,h*.32,h*.32),
                          (W*.54,W*.20,h*.24,h*.33),(W*.80,W*.20,h*.28,h*.32)]:
        c.setFillColor(HexColor('#0E1E10'))
        pts=[(ix,base+iy),(ix,base+iy+ih2),(ix+iw/2,base+iy+ih2+h*.04),(ix+iw,base+iy+ih2),(ix+iw,base+iy)]
        poly(c,pts,HexColor('#0E1E10'))
        c.setFillColor(HexColor('#0E1E10')); c.rect(ix,base,iw,iy+2,fill=1,stroke=0)
    # Canoa
    cx2,cy2,cs = W*.44, base+h*.28, h*.10
    c.setFillColor(HexColor('#5A3818'))
    pts=[(cx2,cy2+cs*.28),(cx2+cs*.28,cy2),(cx2+cs*1.78,cy2),(cx2+cs*1.96,cy2+cs*.28),
         (cx2+cs*1.78,cy2+cs*.56),(cx2+cs*.28,cy2+cs*.56)]
    poly(c,pts,HexColor('#5A3818'))

def ilu_yamana(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#020408'),HexColor('#182838'))
    # Aurora austral (verde tenue)
    for i in range(3):
        c.setFillColor(Color(0.08,0.35+i*.06,0.15,0.12+i*.04))
        pts=[(W*(0.05+i*.12),base+h),(W*(0.18+i*.12),base+h*.55),
             (W*(0.32+i*.12),base+h*.60),(W*(0.30+i*.12),base+h),(W*(0.03+i*.12),base+h)]
        poly(c,pts,Color(0.08,0.35+i*.06,0.15,0.12+i*.04))
    # Estrellas
    stars_field(c,[(W*.04,base+h*.92,2.0),(W*.12,base+h*.96,1.4),(W*.22,base+h*.90,1.7),
                   (W*.35,base+h*.94,2.2),(W*.48,base+h*.88,1.5),(W*.60,base+h*.93,1.9),
                   (W*.72,base+h*.89,1.4),(W*.85,base+h*.94,2.0),(W*.93,base+h*.90,1.6)])
    # Tierra / Cabo de Hornos (silueta izquierda)
    c.setFillColor(HexColor('#080E08'))
    pts=[(0,base+h*.38),(W*.05,base+h*.48),(W*.12,base+h*.52),(W*.20,base+h*.46),
         (W*.28,base+h*.50),(W*.35,base+h*.42),(W*.38,base),(0,base)]
    poly(c,pts,HexColor('#080E08'))
    # Tierra derecha
    pts2=[(W*.68,base+h*.36),(W*.75,base+h*.44),(W*.84,base+h*.40),
          (W*.92,base+h*.48),(W,base+h*.38),(W,base),(W*.68,base)]
    poly(c,pts2,HexColor('#0A1008'))
    # Mar embravecido
    c.setFillColor(HexColor('#0A1820')); c.rect(0,base,W,h*.38,fill=1,stroke=0)
    for wy,amp,col in [(h*.08,h*.024,HexColor('#203848')),(h*.18,h*.028,HexColor('#284858')),
                       (h*.28,h*.026,HexColor('#305868')),(h*.36,h*.018,HexColor('#FFFFFF30'))]:
        wave_strip(c,base+wy,amp,3,col,1.2)
    # Canoa
    bx,by2=W*.46,base+h*.30; bs=h*.09
    c.setFillColor(HexColor('#4A2E10'))
    pts3=[(bx,by2+bs*.28),(bx+bs*.28,by2),(bx+bs*1.72,by2),(bx+bs*2.0,by2+bs*.28),
          (bx+bs*1.72,by2+bs*.56),(bx+bs*.28,by2+bs*.56)]
    poly(c,pts3,HexColor('#4A2E10'))

def ilu_selknam(c, base, h):
    sky_gradient(c,0,base,W,h,HexColor('#0C0818'),HexColor('#786888'))
    # Cielo enorme — viento (líneas tenues)
    c.setStrokeColor(HexColor('#A090A820')); c.setLineWidth(0.6)
    for wy in [h*.55,h*.62,h*.69,h*.76,h*.83]:
        p=c.beginPath(); p.moveTo(0,base+wy)
        p.curveTo(W*.28,base+wy+h*.018,W*.52,base+wy-h*.018,W*.78,base+wy+h*.012)
        p.curveTo(W*.90,base+wy-h*.01,W,base+wy+h*.015,W,base+wy)
        c.drawPath(p,stroke=1,fill=0)
    # Horizonte lejano — franja boscosa
    c.setFillColor(HexColor('#1C2818')); c.rect(W*.55,base+h*.30,W*.45,h*.10,fill=1,stroke=0)
    for i in range(12):
        bx=W*(.56+i*.038); bh2=h*(.06+((i*7)%5)*.018)
        pts=[(bx,base+h*.30),(bx+h*.028,base+h*.30+bh2),(bx+h*.056,base+h*.30)]
        poly(c,pts,HexColor('#141E10'))
    # Pampa (enorme, luminosa)
    sky_gradient(c,0,base,W,h*.32,HexColor('#6A5830'),HexColor('#A08840'))
    # Pastos
    import random; random.seed(17)
    c.setStrokeColor(HexColor('#8A7830')); c.setLineWidth(0.7)
    for _ in range(200):
        gx=random.random()*W; gy=random.random()*h*.25
        c.line(gx,base+gy,gx+random.random()*4-2,base+gy+h*.022)
    # Guanaco (silueta elegante)
    gx2,gy2,gs = W*.32, base+h*.14, h*.18
    c.setFillColor(HexColor('#B89060'))
    c.ellipse(gx2,gy2+gs*.12,gx2+gs*1.10,gy2+gs*.52,fill=1,stroke=0)
    pts=[(gx2+gs*.82,gy2+gs*.38),(gx2+gs*.98,gy2+gs*.78),(gx2+gs*1.10,gy2+gs*.72),(gx2+gs*.96,gy2+gs*.34)]
    poly(c,pts,HexColor('#B89060'))
    c.ellipse(gx2+gs*.82,gy2+gs*.68,gx2+gs*1.20,gy2+gs*.92,fill=1,stroke=0)
    c.setFillColor(HexColor('#A07848'))
    for px in [gx2+gs*.10,gx2+gs*.38,gx2+gs*.65,gx2+gs*.90]:
        c.rect(px,gy2,gs*.12,gs*.14,fill=1,stroke=0)
    # Patrón geométrico Selk'nam (esquina superior derecha, decorativo)
    px2,py2,ps = W*.80, base+h*.52, h*.24
    c.setFillColor(HexColor('#B02810'))
    pts=[(px2,py2+ps*.50),(px2+ps*.28,py2),(px2-ps*.28,py2)]
    poly(c,pts,HexColor('#B02810'))
    c.setFillColor(HexColor('#180808'))
    pts2=[(px2,py2),(px2+ps*.28,py2+ps*.50),(px2-ps*.28,py2+ps*.50)]
    poly(c,pts2,HexColor('#180808'))
    c.setStrokeColor(HexColor('#D03020')); c.setLineWidth(2)
    for dy in [ps*.15,ps*.05,-ps*.15]: c.line(px2-ps*.32,py2+dy,px2+ps*.32,py2+dy)
    c.setFillColor(HexColor('#F8EEE0')); c.circle(px2,py2,ps*.06,fill=1,stroke=0)

ILU_FNS = {
    'ilu_aimara': ilu_aimara, 'ilu_lickanantay': ilu_lickanantay,
    'ilu_quechua': ilu_quechua, 'ilu_colla': ilu_colla,
    'ilu_diaguita': ilu_diaguita, 'ilu_chango': ilu_chango,
    'ilu_rapanui': ilu_rapanui, 'ilu_mapuche': ilu_mapuche,
    'ilu_kawashkar': ilu_kawashkar, 'ilu_yamana': ilu_yamana,
    'ilu_selknam': ilu_selknam,
}

# ══════════════════════════════════════════════════════════════════════════════
# ZONAS DE PÁGINA
# ══════════════════════════════════════════════════════════════════════════════
ILU_H   = 468   # ilustración
BAND_H  = 12    # banda decorativa
ILU_Y   = H - ILU_H          # =373.89
BAND_Y  = ILU_Y - BAND_H     # =361.89
CONT_H  = 252   # área de contenido
CONT_Y  = BAND_Y - CONT_H    # =109.89
FOOT_H  = 108   # pie
# CONT_Y debería coincidir con FOOT_H → ajustamos
# ILU_H = 468, BAND_H = 12, CONT_H = 252, FOOT_H = 108 → sum = 840 ≈ H ✓

M   = 20    # margen lateral
TW  = W - 2*M  # ancho de texto = 555.28
LCW = 254   # ancho columna izquierda
RCW = TW - LCW - 14  # ancho columna derecha (14 = gutter)
RCX = M + LCW + 14   # x inicio columna derecha

# ══════════════════════════════════════════════════════════════════════════════
# PORTADA
# ══════════════════════════════════════════════════════════════════════════════
def draw_cover(c):
    # Fondo oscuro
    c.setFillColor(HexColor('#0E0704')); c.rect(0,0,W,H,fill=1,stroke=0)
    # Franjas horizontales de color
    bands=[(HexColor('#1A0904'),0.00,0.18),(HexColor('#120604'),0.18,0.42),
           (HexColor('#0C0402'),0.42,0.70),(HexColor('#0A0302'),0.70,1.00)]
    for col,y0,y1 in bands:
        c.setFillColor(col); c.rect(0,H*y0,W,H*(y1-y0)+2,fill=1,stroke=0)
    # Círculos decorativos (derecha)
    for r,col in [(200,HexColor('#8A2A0C')),(155,HexColor('#6A2008')),
                  (108,HexColor('#4A1404')),(68,HexColor('#B03A18')),
                  (36,HexColor('#D04820'))]:
        c.setFillColor(col); c.circle(W*.87,H*.40,r,fill=1,stroke=0)
    # Silueta de Chile (abstracta — columna vertical)
    c.setFillColor(HexColor('#1E0806'))
    pts_chile=[
        (W*.44,H*.92),(W*.41,H*.88),(W*.39,H*.82),(W*.40,H*.76),(W*.38,H*.70),
        (W*.36,H*.64),(W*.37,H*.58),(W*.35,H*.52),(W*.34,H*.44),(W*.36,H*.38),
        (W*.38,H*.32),(W*.37,H*.26),(W*.39,H*.20),(W*.41,H*.14),(W*.44,H*.08),
        (W*.47,H*.08),(W*.49,H*.14),(W*.50,H*.20),(W*.49,H*.26),(W*.50,H*.32),
        (W*.52,H*.38),(W*.53,H*.44),(W*.51,H*.52),(W*.53,H*.58),(W*.52,H*.64),
        (W*.54,H*.70),(W*.53,H*.76),(W*.55,H*.82),(W*.53,H*.88),(W*.50,H*.92),
    ]
    poly(c, pts_chile, HexColor('#C8481888'))
    # Banda superior — patrón Diaguita
    bh=22; c.setFillColor(HexColor('#A82810')); c.rect(0,H-bh,W,bh,fill=1,stroke=0)
    n=32; tw2=W/n
    for i in range(n+1):
        col=HexColor('#0E0602') if i%2==0 else HexColor('#E8C050')
        pts=[(i*tw2,H),(i*tw2+tw2/2,H-bh),((i+1)*tw2,H)]
        poly(c,pts,col)
    # Banda inferior
    c.setFillColor(HexColor('#7A1C08')); c.rect(0,0,W,20,fill=1,stroke=0)
    for i in range(n+1):
        col=HexColor('#0E0602') if i%2==0 else HexColor('#C08020')
        pts=[(i*tw2,0),(i*tw2+tw2/2,20),((i+1)*tw2,0)]
        poly(c,pts,col)
    # Líneas doradas decorativas
    horiz_rule(c,M,H*.565,TW,GOLD,2.2)
    horiz_rule(c,M,H*.560,TW,GOLD,0.6)
    # Label pequeño
    tracked(c,"REVISTA EDUCATIVA  ·  7° Y 8° BÁSICO  ·  ABP",
            M, H*.920, 'NB', 7.5, HexColor('#C8A060'), 1.8)
    # Título principal
    c.setFillColor(WHITE); c.setFont('SB',56)
    c.drawString(M, H*.832, "Raíces")
    c.setFont('SI',56); c.drawString(M+stringWidth("Raíces",'SB',56)+4, H*.832, "  que nos unen")
    # Subtítulo
    put(c,"Pueblos originarios de Chile, territorio e identidad",
        M, H*.784,'SI',15,HexColor('#E8C880'),TW)
    # Descripción
    desc=("Revista de consulta para conocer la relación entre pueblos originarios, "
          "territorio, clima, relieve, agua, vegetación, recursos naturales, cultura e identidad.")
    put(c, desc, M, H*.748, 'SR', 10, HexColor('#C8B898'), TW, leading=16)
    # Caja pueblos
    by_caja=H*.230; bh_caja=H*.295
    c.setFillColor(HexColor('#18080408'))
    c.roundRect(M,by_caja,TW,bh_caja,8,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#8A4818')); c.setLineWidth(1)
    c.roundRect(M,by_caja,TW,bh_caja,8,fill=0,stroke=1)
    horiz_rule(c,M+12,by_caja+bh_caja-22,TW-24,HexColor('#8A481860'),0.5)
    tracked(c,"PUEBLOS ORIGINARIOS INCLUIDOS",M+16,by_caja+bh_caja-13,'NB',8,GOLD,1.6)
    pueblos_txt=[
        "Aimara / Aymara   ·   Atacameño / Lickanantay   ·   Quechua",
        "Colla   ·   Diaguita   ·   Chango   ·   Rapa Nui",
        "Mapuche   ·   Kawashkar   ·   Yámana / Yagán   ·   Selk'nam",
    ]
    for i,ln in enumerate(pueblos_txt):
        c.setFillColor(HexColor('#E8D8C0')); c.setFont('SR',10.5)
        c.drawCentredString(W/2, by_caja+bh_caja-50-i*22, ln)
    # Caja ABP
    c.setFillColor(HexColor('#2A5038'))
    c.roundRect(M,by_caja-28,TW,22,5,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('NB',8.5)
    c.drawCentredString(W/2,by_caja-20,
        "Recurso ABP  ·  Lengua y Literatura   |   Historia, Geografía y Ciencias Sociales")
    # Pie
    c.setFillColor(HexColor('#A06020')); c.setFont('NI',7.5)
    c.drawCentredString(W/2,10,"Uso exclusivamente educativo · Sin fines comerciales")

# ══════════════════════════════════════════════════════════════════════════════
# ENCABEZADO INTERNO (páginas 2, glosario, fuentes)
# ══════════════════════════════════════════════════════════════════════════════
def draw_inner_header(c, page_num):
    c.setFillColor(HexColor('#F8F4EC')); c.rect(0,H-26,W,26,fill=1,stroke=0)
    horiz_rule(c,0,H-26,W,RULE,1.0)
    c.setFillColor(GOLD); c.setFont('NB',7); c.drawString(M,H-17,"RAÍCES QUE NOS UNEN")
    c.setFillColor(MID); c.setFont('NI',7)
    c.drawString(M+stringWidth("RAÍCES QUE NOS UNEN",'NB',7)+12, H-17,
                 "Pueblos originarios de Chile · Uso educativo")
    c.setFillColor(MID); c.setFont('NB',8)
    c.drawRightString(W-M, H-17, f"{page_num}")
    # Fondo de página
    c.setFillColor(CREAM); c.rect(0,0,W,H-27,fill=1,stroke=0)

# ══════════════════════════════════════════════════════════════════════════════
# PRESENTACIÓN
# ══════════════════════════════════════════════════════════════════════════════
def draw_presentation(c):
    draw_inner_header(c, 2)
    cy = H - 54
    # Título sección
    c.setFillColor(DARK); c.setFont('SB',20)
    c.drawString(M, cy, "¿Para qué usaremos esta revista?")
    horiz_rule(c, M, cy-6, TW, GOLD, 1.5)
    cy -= 28
    # Cuerpo intro
    intro=("Esta revista es una fuente de consulta para conocer algunos pueblos "
           "originarios de Chile y comprender cómo el territorio influye en sus formas "
           "de vida, actividades, cultura e identidad. A través de la lectura, los "
           "estudiantes podrán obtener información para completar fichas de Lenguaje "
           "e Historia, y preparar producciones para el museo intercultural "
           "«Raíces que nos unen».")
    lines=wrap(intro,'SR',10.5,TW)
    c.setFillColor(DARK); c.setFont('SR',10.5)
    for ln in lines: c.drawString(M,cy,ln); cy-=16
    cy -= 14
    # Dos columnas
    col1=[("📍","Zona donde habita o habitó"),("🌤","Clima del territorio"),
          ("🏔","Relieve del territorio"),("💧","Agua: ríos, lagos, mar o canales"),
          ("🌿","Vegetación y recursos naturales"),("🏡","Forma de vida"),
          ("🎭","Expresiones culturales"),("🏛","Ideas para el museo")]
    col2=[("📚","¿Para quiénes?","Estudiantes de 7° y 8° básico en ABP."),
          ("📖","¿Para qué asignaturas?","Lengua y Literatura · Historia, Geografía y CC.SS."),
          ("✏️","¿Cómo usarlo?","Lee cada ficha, extrae los datos del territorio y responde la pregunta de investigación."),
          ("🏛","¿Qué produciremos?","Fichas de investigación y producciones para el museo intercultural «Raíces que nos unen».")]
    cx1=M; cx2=M+LCW+14; bw=LCW; bw2=RCW
    # Encabezados de columna
    c.setFillColor(HexColor('#B83010')); c.roundRect(cx1,cy-12,bw,18,3,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('NB',8)
    c.drawString(cx1+8,cy-4,"OBSERVAREMOS EN CADA PUEBLO:")
    c.setFillColor(BLUE); c.roundRect(cx2,cy-12,bw2,18,3,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('NB',8)
    c.drawString(cx2+8,cy-4,"¿CÓMO TRABAJAREMOS?")
    cy -= 22
    cy1 = cy
    # Col izquierda
    c.setFillColor(HexColor('#FDF8F2'))
    c.roundRect(cx1,cy1-len(col1)*24-4,bw,len(col1)*24+10,3,fill=1,stroke=0)
    c.setStrokeColor(RULE); c.setLineWidth(0.8)
    c.roundRect(cx1,cy1-len(col1)*24-4,bw,len(col1)*24+10,3,fill=0,stroke=1)
    ty=cy1-4
    for ico,txt in col1:
        c.setFillColor(HexColor('#B83010')); c.setFont('NR',8.5)
        c.drawString(cx1+8,ty,f"{ico}  {txt}"); ty-=24
    # Col derecha
    ty2=cy1
    for ico,lbl,val in col2:
        c.setFillColor(HexColor('#E8F4FF'))
        c.roundRect(cx2,ty2-38,bw2,38,3,fill=1,stroke=0)
        c.setStrokeColor(HexColor('#A8C8E0')); c.setLineWidth(0.6)
        c.roundRect(cx2,ty2-38,bw2,38,3,fill=0,stroke=1)
        c.setFillColor(BLUE); c.setFont('NB',8.5)
        c.drawString(cx2+8,ty2-12,f"{ico}  {lbl}")
        val_lines=wrap(val,'SR',9,bw2-14)
        c.setFillColor(DARK); c.setFont('SR',9)
        for i,vl in enumerate(val_lines):
            c.drawString(cx2+18,ty2-26-i*12,vl)
        ty2-=46
    # Nota de respeto
    note_y = min(ty-12, ty2-12) - 8
    c.setFillColor(HexColor('#EEF8F0'))
    c.roundRect(M, note_y-40, TW, 38, 5, fill=1, stroke=0)
    c.setStrokeColor(GREEN); c.setLineWidth(1.5)
    c.line(M, note_y-40, M, note_y-2)
    note_txt=("Los pueblos originarios presentados en esta revista son comunidades "
              "vivas con identidad, lengua y cultura propias. Esta revista los reconoce "
              "como pueblos con historia, presencia actual y derechos vigentes en Chile.")
    put(c,note_txt,M+10,note_y-10,'SR',9,DARK,TW-14,leading=14)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA DE PUEBLO
# ══════════════════════════════════════════════════════════════════════════════
def draw_pueblo(c, d, page_num):
    # ── Fondo base de la página ──
    c.setFillColor(WHITE); c.rect(0,0,W,H,fill=1,stroke=0)

    # ── ILUSTRACIÓN (zona superior) ──
    ilu_base = H - ILU_H
    ILU_FNS[d['ilufn']](c, ilu_base, ILU_H)

    # ── Overlay oscuro en la parte baja de la ilustración (para texto) ──
    dark_overlay(c, 0, ilu_base, W, ILU_H*.45)

    # ── Número de pueblo (esquina superior derecha) ──
    c.setFillColor(d['accent'])
    c.roundRect(W-M-34, H-46, 34, 28, 4, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('NB',9)
    c.drawCentredString(W-M-17, H-36, d['num'])

    # ── Nombre del pueblo ──
    py_nombre = ilu_base + ILU_H*.42
    c.setFillColor(WHITE); c.setFont('SB',36)
    nm = d['nombre']
    # Sombra
    c.setFillColor(Color(0,0,0,0.4))
    c.drawString(M+2, py_nombre-2, nm)
    c.setFillColor(WHITE)
    c.drawString(M, py_nombre, nm)

    # ── Zona / territorio ──
    horiz_rule(c, M, py_nombre-12, min(stringWidth(nm,'SB',36)+20, TW), d['accent'], 1.5)
    put(c, d['zona'], M, py_nombre-24, 'NI', 9.5, HexColor('#E8E0D0'), TW)

    # ── BANDA decorativa ──
    c.setFillColor(d['accent']); c.rect(0, BAND_Y, W, BAND_H, fill=1, stroke=0)

    # ── ÁREA DE CONTENIDO ──
    # Fondo blanco cálido
    c.setFillColor(HexColor('#FFFDF8')); c.rect(0, CONT_Y, W, CONT_H, fill=1, stroke=0)
    # Separador de columnas
    c.setStrokeColor(RULE); c.setLineWidth(0.7)
    c.line(M+LCW+7, CONT_Y+10, M+LCW+7, CONT_Y+CONT_H-10)

    # ── Etiquetas de sección ──
    def section_tag(x, y, text, col):
        tw3 = stringWidth(text,'NB',6.5)+10
        c.setFillColor(col); c.roundRect(x,y,tw3,13,2,fill=1,stroke=0)
        tracked(c,text,x+5,y+4,'NB',6.5,WHITE,1.2)

    section_tag(M, CONT_Y+CONT_H-16, "GEOGRAFÍA Y TERRITORIO", HexColor('#8A3010'))
    section_tag(RCX, CONT_Y+CONT_H-16, "VIDA Y CULTURA", GREEN)

    # ── Columna izquierda: 5 datos geográficos ──
    items_geo=[
        ("Territorio",    d['territorio']),
        ("Clima",         d['clima']),
        ("Relieve",       d['relieve']),
        ("Agua y recursos", d['agua']),
        ("Vegetación",    d['vegetacion']),
    ]
    ty = CONT_Y + CONT_H - 26
    for lbl,val in items_geo:
        # Label
        c.setFillColor(d['accent']); c.setFont('NB',7.5)
        c.drawString(M, ty, lbl.upper())
        ty -= 13
        # Valor
        vlines = wrap(val,'SR',8.8,LCW)
        c.setFillColor(DARK); c.setFont('SR',8.8)
        for vl in vlines:
            c.drawString(M, ty, vl); ty -= 12.5
        ty -= 5
        # Regla fina
        horiz_rule(c, M, ty+2, LCW, RULE, 0.4)
        ty -= 4

    # ── Columna derecha: Vida y Cultura ──
    ry = CONT_Y + CONT_H - 26

    # Forma de vida (texto más prominente)
    c.setFillColor(GREEN); c.setFont('NB',7.5)
    c.drawString(RCX, ry, "FORMA DE VIDA")
    ry -= 14
    vida_lines = wrap(d['vida'],'SR',9.2,RCW)
    c.setFillColor(DARK); c.setFont('SR',9.2)
    for vl in vida_lines:
        c.drawString(RCX, ry, vl); ry -= 13.5
    ry -= 8

    # Expresiones culturales (caja)
    exp_lines = wrap(d['cultura'],'NI',9,RCW-16)
    exp_h = len(exp_lines)*13 + 28
    c.setFillColor(HexColor('#F0F8F2'))
    c.roundRect(RCX, ry-exp_h, RCW, exp_h, 4, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#8ABA8A')); c.setLineWidth(0.8)
    c.roundRect(RCX, ry-exp_h, RCW, exp_h, 4, fill=0, stroke=1)
    c.setFillColor(GREEN); c.setFont('NB',7.5)
    c.drawString(RCX+8, ry-10, "EXPRESIONES CULTURALES")
    c.setFillColor(HexColor('#1A3820')); c.setFont('NI',9)
    ey = ry-23
    for vl in exp_lines:
        c.drawString(RCX+8, ey, vl); ey -= 13

    # ── PIE: Museo + Pregunta ──
    foot_mid = W / 2 - 1
    # Fondo izquierdo (museo)
    c.setFillColor(HexColor('#162A1C'))
    c.rect(0, 0, foot_mid, FOOT_H, fill=1, stroke=0)
    # Fondo derecho (pregunta)
    c.setFillColor(HexColor('#0E1E34'))
    c.rect(foot_mid+2, 0, W-foot_mid-2, FOOT_H, fill=1, stroke=0)
    # Separador dorado
    c.setFillColor(GOLD); c.rect(foot_mid, 0, 2, FOOT_H, fill=1, stroke=0)

    # Contenido museo
    tracked(c,"▸  MUSEO INTERCULTURAL",M, FOOT_H-16,'NB',7,HexColor('#80C888'),1.4)
    museum_lines=wrap(d['museo'],'SR',8.8,foot_mid-M*2)
    c.setFillColor(HexColor('#C8E8D0')); c.setFont('SR',8.8)
    my=FOOT_H-30
    for ml in museum_lines:
        c.drawString(M,my,ml); my-=13

    # Contenido pregunta
    qx = foot_mid+14
    tracked(c,"❓  PREGUNTA INVESTIGADORA",qx, FOOT_H-16,'NB',7,HexColor('#80A8D8'),1.4)
    q_lines=wrap(d['pregunta'],'SBI',9.5,W-qx-M)
    c.setFillColor(HexColor('#D8E8F8')); c.setFont('SBI',9.5)
    qy=FOOT_H-30
    for ql in q_lines:
        c.drawString(qx,qy,ql); qy-=14

    # Número de página (dentro del pie)
    c.setFillColor(HexColor('#60504840')); c.setFont('NB',8)
    c.drawCentredString(W/2, 8, f"— {page_num} —")

# ══════════════════════════════════════════════════════════════════════════════
# GLOSARIO
# ══════════════════════════════════════════════════════════════════════════════
GLOSARIO=[
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
    ("Vegetación",  "Conjunto de plantas que crecen en un territorio."),
    ("Recursos naturales",
     "Elementos de la naturaleza que las comunidades utilizan: agua, tierra, "
     "animales, plantas, minerales o productos del mar."),
    ("Identidad cultural",
     "Conjunto de costumbres, lengua, relatos, símbolos, valores y formas de vida "
     "que caracterizan a un pueblo o comunidad."),
    ("Medioambiente",
     "Conjunto de elementos naturales y sociales que rodean a los seres vivos."),
    ("Interculturalidad",
     "Relación respetuosa entre distintas culturas, reconociendo sus saberes, "
     "derechos e identidades."),
    ("Patrimonio",
     "Bienes, conocimientos, expresiones, tradiciones o lugares que tienen valor "
     "para una comunidad y deben ser transmitidos."),
]

def draw_glossary(c, page_num):
    draw_inner_header(c, page_num)
    cy = H - 56
    c.setFillColor(DARK); c.setFont('SB',20); c.drawString(M, cy,"Palabras clave para investigar")
    horiz_rule(c, M, cy-8, TW, GOLD, 1.5); cy -= 26
    c.setFillColor(MID); c.setFont('SR',9.5)
    desc="Conceptos fundamentales para comprender los contenidos de esta revista y completar las fichas de investigación."
    put(c,desc,M,cy,'SR',9.5,MID,TW,leading=15); cy -= 30

    col_w = TW/2 - 8
    col2_x = M + TW/2 + 8
    half = len(GLOSARIO)//2 + len(GLOSARIO)%2
    cy1, cy2 = cy, cy

    def draw_term(cx,y,term,defn,col_w):
        c.setFillColor(HexColor('#F8F4EC'))
        c.setStrokeColor(d_accent:=HexColor('#C08828'))
        lines_d=wrap(defn,'SR',9,col_w-20)
        box_h = len(lines_d)*13+32
        c.roundRect(cx,y-box_h,col_w,box_h,4,fill=1,stroke=0)
        c.setStrokeColor(RULE); c.setLineWidth(0.6)
        c.roundRect(cx,y-box_h,col_w,box_h,4,fill=0,stroke=1)
        # Left accent bar
        c.setFillColor(GOLD); c.rect(cx,y-box_h,3,box_h,fill=1,stroke=0)
        c.setFillColor(HexColor('#8A4018')); c.setFont('SB',10)
        c.drawString(cx+10,y-14,term)
        c.setFillColor(DARK); c.setFont('SR',9)
        dy=y-27
        for dl in lines_d: c.drawString(cx+10,dy,dl); dy-=13
        return y-box_h-8

    for i,(term,defn) in enumerate(GLOSARIO):
        if i < half:
            cy1 = draw_term(M, cy1, term, defn, col_w)
        else:
            cy2 = draw_term(col2_x, cy2, term, defn, col_w)

# ══════════════════════════════════════════════════════════════════════════════
# FUENTES
# ══════════════════════════════════════════════════════════════════════════════
FUENTES=[
    ("01","Biblioteca del Congreso Nacional de Chile.",
          "Ley N° 19.253 sobre protección, fomento y desarrollo de los indígenas."),
    ("02","Biblioteca del Congreso Nacional de Chile.",
          "Informe «Los pueblos indígenas y sus comunidades en Chile: reconocimiento y distribución geográfica»."),
    ("03","Ministerio de las Culturas, las Artes y el Patrimonio.",
          "«Recomendaciones para nombrar y escribir sobre pueblos indígenas y Tribal Afrodescendiente chileno»."),
    ("04","Museo Chileno de Arte Precolombino / Chile Precolombino.",
          "Secciones de ambiente, localización, historia, economía, arte y lengua de los pueblos originarios."),
    ("05","Biblioteca Nacional de Chile / Memoria Chilena.", ""),
    ("06","Chile Para Niños / Biblioteca Nacional de Chile.", ""),
]

def draw_sources(c, page_num):
    draw_inner_header(c, page_num)
    cy = H - 56
    c.setFillColor(DARK); c.setFont('SB',20)
    c.drawString(M, cy,"Fuentes consultadas")
    horiz_rule(c, M, cy-8, TW, GOLD, 1.5); cy -= 28
    sub="Fuentes oficiales e institucionales utilizadas en la elaboración de esta revista."
    put(c,sub,M,cy,'SR',9.5,MID,TW); cy-=30

    for num,inst,titulo in FUENTES:
        # Caja
        has_tit = bool(titulo)
        bh=52 if has_tit else 38
        c.setFillColor(HexColor('#F8F6F0'))
        c.roundRect(M,cy-bh,TW,bh,5,fill=1,stroke=0)
        c.setStrokeColor(RULE); c.setLineWidth(0.6)
        c.roundRect(M,cy-bh,TW,bh,5,fill=0,stroke=1)
        # Número
        c.setFillColor(GOLD); c.roundRect(M,cy-bh,30,bh,5,fill=1,stroke=0)
        c.setFillColor(DARK); c.setFont('SB',11)
        c.drawCentredString(M+15, cy-bh/2-5, num)
        # Texto
        c.setFillColor(HexColor('#5A3018')); c.setFont('SB',9.5)
        c.drawString(M+38, cy-16, inst)
        if has_tit:
            put(c,titulo,M+38,cy-30,'SI',9,DARK,TW-44,leading=13)
        cy -= bh+10

    cy -= 12
    # Nota final
    c.setFillColor(HexColor('#EEF8F0'))
    c.roundRect(M,cy-46,TW,44,6,fill=1,stroke=0)
    c.setFillColor(GREEN); c.rect(M,cy-46,4,44,fill=1,stroke=0)
    nota=("Esta revista fue elaborada con fines educativos. La información está resumida y "
          "adaptada para estudiantes de 7° y 8° básico. No está destinada a usos comerciales. "
          "Los pueblos originarios presentados son comunidades con historia, identidad y derechos vigentes en Chile.")
    put(c,nota,M+14,cy-10,'SI',8.5,DARK,TW-20,leading=13)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    out = "/home/user/ESCUELAHOSPITALGERSSON/Raices_que_nos_unen.pdf"
    c = rl_canvas.Canvas(out, pagesize=A4)
    c.setTitle("Raíces que nos unen")
    c.setAuthor("Recurso educativo ABP")
    c.setSubject("Pueblos originarios de Chile · 7° y 8° básico")

    # Pág 1: Portada
    draw_cover(c); c.showPage()

    # Pág 2: Presentación
    draw_presentation(c); c.showPage()

    # Págs 3-13: Pueblos
    for i, d in enumerate(PUEBLOS):
        draw_pueblo(c, d, i+3); c.showPage()

    # Pág 14: Glosario
    draw_glossary(c, 14); c.showPage()

    # Pág 15: Fuentes
    draw_sources(c, 15); c.showPage()

    c.save()
    print(f"✓  PDF generado: {out}")
    import os; print(f"   Tamaño: {os.path.getsize(out)/1024:.0f} KB  ·  15 páginas")

if __name__ == '__main__':
    main()
