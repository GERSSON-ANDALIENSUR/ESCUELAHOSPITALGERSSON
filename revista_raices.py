"""
Revista educativa "Raíces que nos unen"
Pueblos originarios de Chile, territorio e identidad
Formato A4 vertical - para estudiantes 7° y 8° básico
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import (
    Drawing, Rect, Circle, Line, Polygon, String, Group,
    Wedge, Ellipse, Path
)
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
import os

# ── Paleta de colores ──────────────────────────────────────────────────────────
TERRACOTA   = HexColor('#C0522A')
ARENA       = HexColor('#E8D5A3')
ARENA_CLARO = HexColor('#F5EDD6')
TIERRA      = HexColor('#8B5E3C')
VERDE       = HexColor('#4A7C59')
VERDE_CLARO = HexColor('#A8C5A0')
AZUL        = HexColor('#2E6B8A')
AZUL_CLARO  = HexColor('#B0D4E8')
OCRE        = HexColor('#D4842A')
MARRON      = HexColor('#6B3A2A')
BLANCO      = colors.white
NEGRO       = HexColor('#2A1F14')
GRIS_CLARO  = HexColor('#F0EBE3')
SALMON      = HexColor('#E8A882')

W, H = A4  # 595.27 x 841.89 pt

# ── Estilos tipográficos ───────────────────────────────────────────────────────
def make_styles():
    s = {}
    base = ParagraphStyle(
        'base', fontName='Helvetica', fontSize=10,
        leading=14, textColor=NEGRO, spaceAfter=4
    )
    s['titulo_portada'] = ParagraphStyle(
        'titulo_portada', parent=base,
        fontName='Helvetica-Bold', fontSize=34,
        textColor=BLANCO, leading=40, alignment=TA_CENTER, spaceAfter=8
    )
    s['subtitulo_portada'] = ParagraphStyle(
        'subtitulo_portada', parent=base,
        fontName='Helvetica-BoldOblique', fontSize=16,
        textColor=ARENA, leading=20, alignment=TA_CENTER, spaceAfter=10
    )
    s['texto_portada'] = ParagraphStyle(
        'texto_portada', parent=base,
        fontName='Helvetica', fontSize=11,
        textColor=ARENA_CLARO, leading=16, alignment=TA_CENTER
    )
    s['titulo_pagina'] = ParagraphStyle(
        'titulo_pagina', parent=base,
        fontName='Helvetica-Bold', fontSize=20,
        textColor=BLANCO, leading=24, alignment=TA_LEFT, spaceAfter=0
    )
    s['subtitulo_seccion'] = ParagraphStyle(
        'subtitulo_seccion', parent=base,
        fontName='Helvetica-Bold', fontSize=13,
        textColor=TERRACOTA, leading=17, spaceAfter=4
    )
    s['campo_label'] = ParagraphStyle(
        'campo_label', parent=base,
        fontName='Helvetica-Bold', fontSize=9,
        textColor=TIERRA, leading=12, spaceAfter=1
    )
    s['campo_valor'] = ParagraphStyle(
        'campo_valor', parent=base,
        fontName='Helvetica', fontSize=9,
        textColor=NEGRO, leading=13, spaceAfter=3
    )
    s['cuerpo'] = ParagraphStyle(
        'cuerpo', parent=base,
        fontName='Helvetica', fontSize=10,
        textColor=NEGRO, leading=15, alignment=TA_JUSTIFY, spaceAfter=5
    )
    s['cuerpo_bold'] = ParagraphStyle(
        'cuerpo_bold', parent=base,
        fontName='Helvetica-Bold', fontSize=10,
        textColor=NEGRO, leading=15, spaceAfter=5
    )
    s['pregunta'] = ParagraphStyle(
        'pregunta', parent=base,
        fontName='Helvetica-BoldOblique', fontSize=10,
        textColor=AZUL, leading=15, alignment=TA_CENTER, spaceAfter=4
    )
    s['museo'] = ParagraphStyle(
        'museo', parent=base,
        fontName='Helvetica-Oblique', fontSize=9,
        textColor=VERDE, leading=13, spaceAfter=3
    )
    s['glosario_term'] = ParagraphStyle(
        'glosario_term', parent=base,
        fontName='Helvetica-Bold', fontSize=10,
        textColor=TERRACOTA, leading=14, spaceAfter=1
    )
    s['glosario_def'] = ParagraphStyle(
        'glosario_def', parent=base,
        fontName='Helvetica', fontSize=9,
        textColor=NEGRO, leading=13, spaceAfter=6, leftIndent=10
    )
    s['fuente'] = ParagraphStyle(
        'fuente', parent=base,
        fontName='Helvetica', fontSize=9,
        textColor=NEGRO, leading=13, spaceAfter=5, leftIndent=14, firstLineIndent=-14
    )
    s['nota'] = ParagraphStyle(
        'nota', parent=base,
        fontName='Helvetica-Oblique', fontSize=8,
        textColor=TIERRA, leading=12, alignment=TA_CENTER
    )
    s['titulo_seccion'] = ParagraphStyle(
        'titulo_seccion', parent=base,
        fontName='Helvetica-Bold', fontSize=14,
        textColor=TIERRA, leading=18, spaceAfter=6
    )
    return s

ST = make_styles()

# ── Flowables decorativos ──────────────────────────────────────────────────────

class BannerHeader(Flowable):
    """Banda de color con título para cada página de pueblo."""
    def __init__(self, titulo, color_fondo=None, color_acento=None, ancho=None):
        super().__init__()
        self.titulo = titulo
        self.color_fondo = color_fondo or TERRACOTA
        self.color_acento = color_acento or OCRE
        self.ancho = ancho or (W - 3*cm)
        self.altura = 1.6*cm

    def wrap(self, aw, ah):
        return self.ancho, self.altura

    def draw(self):
        c = self.canv
        # Fondo principal
        c.setFillColor(self.color_fondo)
        c.roundRect(0, 0, self.ancho, self.altura, 6, fill=1, stroke=0)
        # Franja decorativa lateral
        c.setFillColor(self.color_acento)
        c.roundRect(0, 0, 10, self.altura, 3, fill=1, stroke=0)
        # Título
        c.setFillColor(BLANCO)
        c.setFont('Helvetica-Bold', 17)
        c.drawString(20, self.altura/2 - 6, self.titulo)


class LineaDecorativa(Flowable):
    def __init__(self, ancho=None, color=None, grosor=2):
        super().__init__()
        self.ancho = ancho or (W - 3*cm)
        self.color = color or TERRACOTA
        self.grosor = grosor

    def wrap(self, aw, ah):
        return self.ancho, self.grosor + 4

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.grosor)
        c.line(0, self.grosor/2, self.ancho, self.grosor/2)


class CajaInfo(Flowable):
    """Caja rectangular con etiqueta y contenido."""
    def __init__(self, etiqueta, contenido, ancho=None, color_borde=None,
                 color_fondo=None, color_label=None):
        super().__init__()
        self.etiqueta = etiqueta
        self.contenido = contenido
        self.ancho = ancho or (W - 3*cm)
        self.color_borde = color_borde or TERRACOTA
        self.color_fondo = color_fondo or ARENA_CLARO
        self.color_label = color_label or TERRACOTA

    def wrap(self, aw, ah):
        return self.ancho, 0.1  # medida dinámica real via tabla

    def draw(self):
        pass


def tabla_campos(campos, ancho=None, color_fondo=None, color_borde=None):
    """
    campos: lista de (etiqueta, valor)
    Devuelve una Table con estilo visual de caja de datos.
    """
    ancho = ancho or (W - 3*cm)
    color_fondo = color_fondo or ARENA_CLARO
    color_borde = color_borde or TERRACOTA

    data = []
    for label, val in campos:
        lbl = Paragraph(label, ST['campo_label'])
        txt = Paragraph(val, ST['campo_valor'])
        data.append([lbl, txt])

    col1 = ancho * 0.30
    col2 = ancho * 0.70

    t = Table(data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_fondo),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [color_fondo, GRIS_CLARO]),
        ('BOX', (0,0), (-1,-1), 1.5, color_borde),
        ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor('#C8B89A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t


def caja_destacada(texto, color_fondo=None, color_borde=None, estilo=None):
    """Caja simple con texto destacado."""
    color_fondo = color_fondo or AZUL_CLARO
    color_borde = color_borde or AZUL
    estilo = estilo or ST['pregunta']
    p = Paragraph(texto, estilo)
    ancho = W - 3*cm
    t = Table([[p]], colWidths=[ancho])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_fondo),
        ('BOX', (0,0), (-1,-1), 2, color_borde),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [6]),
    ]))
    return t


def caja_museo(texto_museo, color_fondo=None):
    color_fondo = color_fondo or HexColor('#E8F4E8')
    icon = Paragraph("🏛  Idea para el museo intercultural:", ST['campo_label'])
    txt  = Paragraph(texto_museo, ST['museo'])
    ancho = W - 3*cm
    t = Table([[icon], [txt]], colWidths=[ancho])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_fondo),
        ('BOX', (0,0), (-1,-1), 1.5, VERDE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


# ── Mapa esquemático de Chile ──────────────────────────────────────────────────

class MapaChile(Flowable):
    """Mapa simplificado de Chile con puntos de pueblos originarios."""
    def __init__(self, ancho=7*cm, alto=15*cm):
        super().__init__()
        self.ancho = ancho
        self.alto  = alto

    def wrap(self, aw, ah):
        return self.ancho, self.alto

    def draw(self):
        c = self.canv
        ax, ay = self.ancho, self.alto

        # Silueta muy simplificada de Chile (continental + isla)
        # Coordenadas normalizadas [0..1] → escala a (ax, ay)
        def pt(nx, ny):
            return nx * ax * 0.7 + ax*0.12, (1 - ny) * ay + 6

        # Fondo
        c.setFillColor(HexColor('#D6EAF8'))
        c.rect(0, 0, ax, ay, fill=1, stroke=0)

        # Silueta de Chile - polígono muy simplificado
        puntos_chile = [
            (0.25, 0.02), (0.55, 0.02), (0.60, 0.05), (0.58, 0.10),
            (0.62, 0.14), (0.60, 0.18), (0.65, 0.22), (0.62, 0.27),
            (0.66, 0.32), (0.63, 0.38), (0.68, 0.44), (0.65, 0.50),
            (0.70, 0.55), (0.67, 0.60), (0.72, 0.65), (0.68, 0.70),
            (0.65, 0.75), (0.60, 0.80), (0.55, 0.84), (0.50, 0.88),
            (0.45, 0.92), (0.40, 0.96), (0.30, 0.98), (0.20, 0.96),
            (0.15, 0.92), (0.18, 0.87), (0.22, 0.82), (0.18, 0.76),
            (0.20, 0.70), (0.16, 0.65), (0.20, 0.60), (0.16, 0.55),
            (0.20, 0.50), (0.17, 0.44), (0.22, 0.38), (0.18, 0.32),
            (0.22, 0.27), (0.20, 0.22), (0.24, 0.18), (0.22, 0.14),
            (0.26, 0.10), (0.24, 0.05),
        ]
        path = c.beginPath()
        x0, y0 = pt(*puntos_chile[0])
        path.moveTo(x0, y0)
        for p in puntos_chile[1:]:
            path.lineTo(*pt(*p))
        path.close()
        c.setFillColor(HexColor('#C8D8A0'))
        c.setStrokeColor(HexColor('#7A9A50'))
        c.setLineWidth(0.8)
        c.drawPath(path, fill=1, stroke=1)

        # Isla de Pascua (esquina superior izquierda del mapa)
        c.setFillColor(HexColor('#C8D8A0'))
        c.setStrokeColor(HexColor('#7A9A50'))
        c.ellipse(ax*0.05, ay*0.80, ax*0.14, ay*0.84, fill=1, stroke=1)

        # Función para dibujar punto con etiqueta
        def dot(nx, ny, label, color, size=4):
            px, py = pt(nx, ny)
            c.setFillColor(color)
            c.circle(px, py, size, fill=1, stroke=0)
            c.setFillColor(NEGRO)
            c.setFont('Helvetica-Bold', 5.5)
            c.drawString(px + size + 1.5, py - 2, label)

        # Pueblos originarios
        pueblos = [
            (0.42, 0.10, "Aimara/Aymara",     TERRACOTA),
            (0.50, 0.16, "Lickanantay",        HexColor('#8B4513')),
            (0.52, 0.22, "Quechua",            HexColor('#D2691E')),
            (0.44, 0.28, "Colla",              HexColor('#A0522D')),
            (0.40, 0.36, "Diaguita",           HexColor('#CD853F')),
            (0.28, 0.28, "Chango",             AZUL),
            (0.44, 0.50, "Mapuche",            VERDE),
            (0.25, 0.78, "Kawashkar",          AZUL),
            (0.30, 0.87, "Yámana/Yagán",       HexColor('#1A5276')),
            (0.45, 0.83, "Selk'nam",           HexColor('#6C3483')),
        ]
        for nx, ny, lbl, col in pueblos:
            dot(nx, ny, lbl, col)

        # Rapa Nui en la isla ficticia
        c.setFillColor(HexColor('#E74C3C'))
        c.circle(ax*0.095, ay*0.82, 3.5, fill=1, stroke=0)
        c.setFillColor(NEGRO)
        c.setFont('Helvetica-Bold', 5)
        c.drawString(ax*0.005, ay*0.845, "Rapa Nui")

        # Leyenda
        c.setFillColor(ARENA_CLARO)
        c.roundRect(2, 2, ax - 4, 22, 3, fill=1, stroke=0)
        c.setFillColor(NEGRO)
        c.setFont('Helvetica-Bold', 5.5)
        c.drawString(6, 12, "Mapa educativo simplificado")
        c.setFont('Helvetica', 5)
        c.drawString(6, 5, "Las ubicaciones son aproximadas.")

        # Título del mapa
        c.setFillColor(TERRACOTA)
        c.roundRect(2, ay-20, ax-4, 18, 3, fill=1, stroke=0)
        c.setFillColor(BLANCO)
        c.setFont('Helvetica-Bold', 6.5)
        c.drawCentredString(ax/2, ay - 12, "Pueblos Originarios de Chile")


# ── Página de portada (dibujada directamente en canvas) ───────────────────────

def portada(c_obj, doc):
    c_obj.saveState()
    # Fondo degradado simulado con rectángulos
    franjas = [
        (MARRON,    0.00, 0.15),
        (TIERRA,    0.15, 0.50),
        (TERRACOTA, 0.50, 0.75),
        (OCRE,      0.75, 1.00),
    ]
    for color, y0, y1 in franjas:
        c_obj.setFillColor(color)
        c_obj.rect(0, H*y0, W, H*(y1-y0), fill=1, stroke=0)

    # Banda decorativa superior
    c_obj.setFillColor(MARRON)
    c_obj.rect(0, H - 2.5*cm, W, 2.5*cm, fill=1, stroke=0)
    c_obj.setFillColor(OCRE)
    c_obj.rect(0, H - 2.8*cm, W, 0.3*cm, fill=1, stroke=0)

    # Banda decorativa inferior
    c_obj.setFillColor(MARRON)
    c_obj.rect(0, 0, W, 2.2*cm, fill=1, stroke=0)
    c_obj.setFillColor(OCRE)
    c_obj.rect(0, 2.2*cm, W, 0.3*cm, fill=1, stroke=0)

    # Patrón geométrico decorativo (líneas andinas)
    c_obj.setStrokeColor(HexColor('#C0522A'))
    c_obj.setLineWidth(0.5)
    for i in range(0, int(W), 20):
        c_obj.line(i, 0, i, 0.8*cm)
        c_obj.line(i, H - 2.0*cm, i, H - 0.5*cm)

    # Elemento visual: círculos decorativos
    c_obj.setFillColor(HexColor('#A0401A'))
    c_obj.circle(W*0.85, H*0.55, 80, fill=1, stroke=0)
    c_obj.setFillColor(HexColor('#8B3010'))
    c_obj.circle(W*0.85, H*0.55, 55, fill=1, stroke=0)
    c_obj.setFillColor(HexColor('#7A2005'))
    c_obj.circle(W*0.85, H*0.55, 30, fill=1, stroke=0)

    c_obj.setFillColor(HexColor('#4A7C59'))
    c_obj.circle(W*0.12, H*0.30, 60, fill=1, stroke=0)
    c_obj.setFillColor(HexColor('#3A6A49'))
    c_obj.circle(W*0.12, H*0.30, 40, fill=1, stroke=0)

    # Líneas decorativas andinas horizontales
    for i, y_frac in enumerate([0.42, 0.44, 0.46]):
        c_obj.setStrokeColor(HexColor('#E8C880'))
        c_obj.setLineWidth(1 if i == 1 else 0.5)
        c_obj.line(1.5*cm, H*y_frac, W - 1.5*cm, H*y_frac)

    # ── Textos ──
    # Número / edición
    c_obj.setFillColor(ARENA)
    c_obj.setFont('Helvetica', 8)
    c_obj.drawCentredString(W/2, H - 1.6*cm, "REVISTA EDUCATIVA  |  7° y 8° BÁSICO")

    # Título principal
    c_obj.setFillColor(BLANCO)
    c_obj.setFont('Helvetica-Bold', 38)
    c_obj.drawCentredString(W/2, H*0.70, "Raíces que nos unen")

    # Línea bajo título
    c_obj.setStrokeColor(OCRE)
    c_obj.setLineWidth(2.5)
    c_obj.line(W*0.15, H*0.685, W*0.85, H*0.685)

    # Subtítulo
    c_obj.setFillColor(ARENA)
    c_obj.setFont('Helvetica-BoldOblique', 14)
    c_obj.drawCentredString(W/2, H*0.655,
        "Pueblos originarios de Chile, territorio e identidad")

    # Texto descriptivo (multilínea)
    c_obj.setFillColor(ARENA_CLARO)
    c_obj.setFont('Helvetica', 10)
    lineas = [
        "Revista de consulta para conocer la relación entre pueblos originarios,",
        "territorio, clima, relieve, agua, vegetación, recursos naturales,",
        "cultura e identidad."
    ]
    for i, ln in enumerate(lineas):
        c_obj.drawCentredString(W/2, H*0.59 - i*14, ln)

    # Caja de pueblos
    c_obj.setFillColor(HexColor('#3A1A0A'))
    c_obj.roundRect(1.5*cm, H*0.22, W - 3*cm, H*0.30, 8, fill=1, stroke=0)
    c_obj.setStrokeColor(OCRE)
    c_obj.setLineWidth(1.5)
    c_obj.roundRect(1.5*cm, H*0.22, W - 3*cm, H*0.30, 8, fill=0, stroke=1)

    c_obj.setFillColor(OCRE)
    c_obj.setFont('Helvetica-Bold', 10)
    c_obj.drawCentredString(W/2, H*0.505, "Pueblos originarios incluidos en esta revista:")

    pueblos_lista = [
        "Aimara/Aymara   •   Atacameño/Lickanantay   •   Quechua   •   Colla",
        "Diaguita   •   Chango   •   Rapa Nui   •   Mapuche",
        "Kawashkar   •   Yámana/Yagán   •   Selk'nam"
    ]
    c_obj.setFillColor(ARENA_CLARO)
    c_obj.setFont('Helvetica', 9.5)
    for i, ln in enumerate(pueblos_lista):
        c_obj.drawCentredString(W/2, H*0.474 - i*15, ln)

    # ABP nota
    c_obj.setFillColor(VERDE_CLARO)
    c_obj.roundRect(1.5*cm, H*0.155, W - 3*cm, 1.1*cm, 6, fill=1, stroke=0)
    c_obj.setFillColor(VERDE)
    c_obj.setFont('Helvetica-Bold', 9)
    c_obj.drawCentredString(W/2, H*0.190,
        "Recurso para Aprendizaje Basado en Proyectos (ABP)")
    c_obj.setFillColor(MARRON)
    c_obj.setFont('Helvetica', 8.5)
    c_obj.drawCentredString(W/2, H*0.172,
        "Lengua y Literatura  |  Historia, Geografía y Ciencias Sociales")

    # Pie de portada
    c_obj.setFillColor(ARENA)
    c_obj.setFont('Helvetica', 7.5)
    c_obj.drawCentredString(W/2, 0.9*cm, "Uso exclusivamente educativo · Sin fines comerciales")

    c_obj.restoreState()


# ── Canvas personalizado con pie de página ────────────────────────────────────

class MiCanvas:
    """Agrega encabezado y pie a cada página interna."""
    def __init__(self, nombre_archivo, **kwargs):
        self._doc = SimpleDocTemplate(nombre_archivo, **kwargs)
        self._pagina = 0

    def build(self, story, on_first_page, on_later_pages):
        self._doc.build(story,
                        onFirstPage=on_first_page,
                        onLaterPages=on_later_pages)


def encabezado_pie(c_obj, doc, titulo_seccion=""):
    """Encabezado superior y pie de página para páginas internas."""
    # Encabezado
    c_obj.saveState()
    c_obj.setFillColor(TIERRA)
    c_obj.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
    c_obj.setFillColor(OCRE)
    c_obj.rect(0, H - 1.2*cm, W, 0.1*cm, fill=1, stroke=0)
    c_obj.setFillColor(BLANCO)
    c_obj.setFont('Helvetica-Bold', 9)
    c_obj.drawString(1.5*cm, H - 0.75*cm, "RAÍCES QUE NOS UNEN")
    c_obj.setFont('Helvetica', 8)
    c_obj.drawRightString(W - 1.5*cm, H - 0.75*cm,
                          "Pueblos originarios de Chile · Uso educativo")

    # Pie
    c_obj.setFillColor(ARENA)
    c_obj.rect(0, 0, W, 0.9*cm, fill=1, stroke=0)
    c_obj.setFillColor(OCRE)
    c_obj.rect(0, 0.9*cm, W, 0.08*cm, fill=1, stroke=0)
    c_obj.setFillColor(TIERRA)
    c_obj.setFont('Helvetica', 7.5)
    c_obj.drawString(1.5*cm, 0.32*cm,
                     "Revista educativa para 7° y 8° básico · ABP")
    c_obj.drawRightString(W - 1.5*cm, 0.32*cm,
                          f"Página {doc.page}")
    c_obj.restoreState()


# ── Constructores de páginas temáticas ────────────────────────────────────────

def seccion_pueblo(nombre, color_banner, campos, expresiones,
                   museo_texto, pregunta_texto, color_acento=None):
    """Genera el contenido de una página de pueblo originario."""
    ca = color_acento or OCRE
    elems = []
    elems.append(BannerHeader(nombre, color_fondo=color_banner, color_acento=ca))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(tabla_campos(campos, color_fondo=ARENA_CLARO, color_borde=color_banner))
    elems.append(Spacer(1, 0.25*cm))

    # Expresiones culturales
    exp_label = Paragraph("Expresiones culturales", ST['campo_label'])
    exp_val   = Paragraph(expresiones, ST['campo_valor'])
    ancho = W - 3*cm
    t_exp = Table([[exp_label], [exp_val]], colWidths=[ancho])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F0E8D8')),
        ('BOX', (0,0), (-1,-1), 1.2, color_banner),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elems.append(t_exp)
    elems.append(Spacer(1, 0.25*cm))
    elems.append(caja_museo(museo_texto))
    elems.append(Spacer(1, 0.25*cm))
    elems.append(caja_destacada(
        f"✦ Pregunta para investigar: {pregunta_texto}",
        color_fondo=AZUL_CLARO, color_borde=AZUL
    ))
    elems.append(PageBreak())
    return elems


# ── Contenido completo de la revista ──────────────────────────────────────────

def construir_revista():
    story = []

    # ── PÁG 2: PRESENTACIÓN ──────────────────────────────────────────────────
    story.append(BannerHeader("¿Para qué usaremos esta revista?",
                               color_fondo=TIERRA, color_acento=OCRE))
    story.append(Spacer(1, 0.35*cm))
    story.append(Paragraph(
        "Esta revista es una fuente de consulta para conocer algunos pueblos "
        "originarios de Chile y comprender cómo el territorio influye en sus "
        "formas de vida, actividades, cultura e identidad. A través de la "
        "lectura, los estudiantes podrán obtener información para completar "
        "fichas de Lenguaje e Historia y preparar producciones para el museo "
        "intercultural <b>\"Raíces que nos unen\"</b>.",
        ST['cuerpo']
    ))
    story.append(Spacer(1, 0.3*cm))

    # Recuadro de observaciones
    obs_items = [
        "Zona donde habita o habitó.",
        "Clima.",
        "Relieve.",
        "Agua, ríos, lagos, mar o canales.",
        "Vegetación y recursos naturales.",
        "Forma de vida relacionada con el territorio.",
        "Expresiones culturales.",
        "Ideas para representar en el museo intercultural.",
    ]
    obs_label = Paragraph("Observaremos en cada pueblo:", ST['subtitulo_seccion'])
    obs_lista = [Paragraph(f"• {item}", ST['cuerpo']) for item in obs_items]
    ancho = W - 3*cm
    data_obs = [[obs_label]] + [[p] for p in obs_lista]
    t_obs = Table(data_obs, colWidths=[ancho])
    t_obs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#FBF6EC')),
        ('BACKGROUND', (0,0), (0,0), HexColor('#C0522A')),
        ('TEXTCOLOR', (0,0), (0,0), BLANCO),
        ('BOX', (0,0), (-1,-1), 2, TERRACOTA),
        ('LINEBELOW', (0,0), (0,0), 1, TERRACOTA),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_obs)
    story.append(Spacer(1, 0.35*cm))

    # Nota metodológica
    nota_items = [
        ("¿Quiénes lo usarán?",
         "Estudiantes de 7° y 8° básico en el contexto de un Aprendizaje Basado en Proyectos (ABP)."),
        ("¿Para qué asignaturas?",
         "Lengua y Literatura, e Historia, Geografía y Ciencias Sociales."),
        ("¿Cómo usarlo?",
         "Lee cada página, observa los datos territoriales y responde la pregunta de investigación. "
         "Usa la información para completar fichas y preparar el museo intercultural."),
    ]
    t_nota = tabla_campos(nota_items, color_fondo=AZUL_CLARO,
                           color_borde=AZUL)
    story.append(t_nota)
    story.append(PageBreak())

    # ── PÁG 3: MAPA GENERAL ──────────────────────────────────────────────────
    story.append(BannerHeader("Pueblos originarios de Chile — Ubicación aproximada",
                               color_fondo=AZUL, color_acento=VERDE))
    story.append(Spacer(1, 0.3*cm))

    mapa = MapaChile(ancho=7.5*cm, alto=16.5*cm)

    # Leyenda lateral
    pueblos_leyenda = [
        (TERRACOTA,          "Aimara/Aymara — Norte Grande"),
        (HexColor('#8B4513'),"Lickanantay — Antofagasta"),
        (HexColor('#D2691E'),"Quechua — Norte, Antofagasta"),
        (HexColor('#A0522D'),"Colla — Región de Atacama"),
        (HexColor('#CD853F'),"Diaguita — Norte Chico"),
        (AZUL,               "Chango — Costa norte"),
        (HexColor('#E74C3C'),"Rapa Nui — Isla del Pacífico"),
        (VERDE,              "Mapuche — Centro-sur"),
        (AZUL,               "Kawashkar — Canales australes"),
        (HexColor('#1A5276'),"Yámana/Yagán — Tierra del Fuego sur"),
        (HexColor('#6C3483'),"Selk'nam — Tierra del Fuego"),
    ]

    leyenda_data = []
    for col, texto in pueblos_leyenda:
        color_cell = Table(
            [['']], colWidths=[0.4*cm], rowHeights=[0.35*cm]
        )
        color_cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,0), col),
            ('BOX', (0,0),(0,0), 0.5, NEGRO),
        ]))
        txt_cell = Paragraph(texto, ST['campo_valor'])
        leyenda_data.append([color_cell, txt_cell])

    t_leyenda = Table(leyenda_data, colWidths=[0.55*cm, 8.2*cm])
    t_leyenda.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))

    # Nota del mapa
    nota_mapa = Paragraph(
        "Las ubicaciones son aproximadas y sirven con fines educativos. "
        "Los territorios de cada pueblo son amplios y pueden incluir zonas "
        "no representadas en este mapa.",
        ST['nota']
    )

    columna_der = Table(
        [[t_leyenda], [Spacer(1, 0.4*cm)], [nota_mapa]],
        colWidths=[9*cm]
    )
    columna_der.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    t_mapa_layout = Table(
        [[mapa, columna_der]],
        colWidths=[7.8*cm, 9*cm]
    )
    t_mapa_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_mapa_layout)
    story.append(PageBreak())

    # ── PÁG 4: AIMARA/AYMARA ─────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Aimara / Aymara",
        color_banner=TERRACOTA,
        color_acento=OCRE,
        campos=[
            ("Zona",
             "Norte Grande de Chile: Arica y Parinacota, Tarapacá y Antofagasta."),
            ("Territorio",
             "Altiplano, puna, sierra, precordillera, valles altos y valles bajos."),
            ("Clima",
             "Frío y seco en altura; gran diferencia de temperatura entre el día y la noche; "
             "lluvias estivales en sectores altiplánicos."),
            ("Relieve",
             "Altiplano, cordillera, quebradas, valles y zonas de altura."),
            ("Agua y recursos",
             "Bofedales, vegas, quebradas, agricultura en terrazas y ganadería de camélidos."),
            ("Vegetación",
             "Pastos de altura, vegetación de bofedales y arbustos adaptados a la aridez."),
            ("Forma de vida",
             "Su vida se relaciona con distintos pisos ecológicos. Han desarrollado agricultura, "
             "pastoreo, intercambio y organización comunitaria vinculada al territorio."),
        ],
        expresiones=(
            "Lengua aimara, tejidos, música, festividades, relación con la Pachamama "
            "y vida comunitaria."
        ),
        museo_texto=(
            "Mapa de pisos ecológicos, tejido, dibujo de bofedal, "
            "ficha sobre pastoreo o maqueta de terrazas agrícolas."
        ),
        pregunta_texto="¿Cómo influye la vida en altura en las actividades del pueblo Aimara/Aymara?",
    )

    # ── PÁG 5: LICKANANTAY ───────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Atacameño o Lickanantay",
        color_banner=HexColor('#7A3B10'),
        color_acento=HexColor('#C88030'),
        campos=[
            ("Zona",
             "Región de Antofagasta: oasis, quebradas, cuenca del Salar de Atacama y río Loa."),
            ("Territorio",
             "Desierto de Atacama, oasis, salares, vegas, bofedales y quebradas."),
            ("Clima",
             "Desértico, de extrema aridez y gran oscilación térmica entre el día y la noche."),
            ("Relieve",
             "Desierto, cordillera, salares, quebradas y oasis."),
            ("Agua y recursos",
             "Ríos El Loa, El Salado y Vilama; vegas, bofedales y aguas de quebradas."),
            ("Vegetación",
             "Tolar, pajonal, yareta, algarrobo, tamarugo, chañar y vegetación de oasis."),
            ("Forma de vida",
             "El uso del agua permitió la agricultura, el pastoreo y la vida en oasis. "
             "El territorio desértico influyó en sus formas de asentamiento y en su relación "
             "con los recursos naturales."),
        ],
        expresiones=(
            "Lengua kunza, agricultura, alfarería, arquitectura en adobe, "
            "relación con montañas, agua y territorio."
        ),
        museo_texto=(
            "Maqueta de oasis, mapa del río Loa, dibujo de salar, "
            "ficha sobre uso del agua o muestra de símbolos andinos."
        ),
        pregunta_texto="¿Por qué el agua es tan importante en la vida del pueblo Lickanantay?",
    )

    # ── PÁG 6: QUECHUA ───────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Quechua",
        color_banner=HexColor('#8B5A2B'),
        color_acento=HexColor('#D4A04A'),
        campos=[
            ("Zona",
             "Norte de Chile: Región de Antofagasta, sectores de Ollagüe, "
             "Alto Loa y comunidades vinculadas a quebradas y salares."),
            ("Territorio",
             "Altiplano, salares, quebradas, vegas y sectores de pastoreo."),
            ("Clima",
             "Árido y frío de altura, con baja humedad y gran variación térmica."),
            ("Relieve",
             "Cordillera, altiplano, salares, quebradas y volcanes."),
            ("Agua y recursos",
             "Vegas, lagunas, ríos y campos de pastoreo."),
            ("Vegetación",
             "Pajonales, tolares, vegetación de quebradas y plantas adaptadas a la altura y aridez."),
            ("Forma de vida",
             "Históricamente se relaciona con la agricultura, ganadería, "
             "pastoreo y vínculos con rutas andinas."),
        ],
        expresiones=(
            "Lengua quechua, tradición oral, tejidos, agricultura, "
            "pastoreo y herencia cultural andina."
        ),
        museo_texto=(
            "Mapa de rutas andinas, ficha de pastoreo, dibujo de salar "
            "o glosario de palabras quechuas."
        ),
        pregunta_texto="¿Cómo se relacionan las quebradas y salares con la vida del pueblo Quechua?",
    )

    # ── PÁG 7: COLLA ─────────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Colla",
        color_banner=HexColor('#6B3A1A'),
        color_acento=HexColor('#B07030'),
        campos=[
            ("Zona",
             "Región de Atacama: Chañaral, Copiapó, Tierra Amarilla, Potrerillos, "
             "Inca de Oro, Quebrada de Paipote y río Jorquera."),
            ("Territorio",
             "Precordillera y Cordillera de los Andes."),
            ("Clima",
             "Árido en zonas bajas y frío de montaña en zonas altas."),
            ("Relieve",
             "Cordillera, quebradas, campos de pastoreo de altura y fondos de valle."),
            ("Agua y recursos",
             "Río Jorquera, río de La Sal, aguadas, vegas y quebradas."),
            ("Vegetación",
             "Vegetación escasa en quebradas; arbustos como cachiyuyo y brea; "
             "algarrobo, tolar y pajonal."),
            ("Forma de vida",
             "Tradicionalmente ligada al pastoreo, la agricultura, la recolección "
             "y el uso de veranadas e invernadas."),
        ],
        expresiones=(
            "Vida de arriería, relación con animales, conocimiento de rutas "
            "cordilleranas y prácticas campesinas de altura."
        ),
        museo_texto=(
            "Mapa de veranadas e invernadas, dibujo de arriería, "
            "ficha sobre pastoreo o maqueta de quebrada."
        ),
        pregunta_texto="¿Por qué la cordillera es importante para la vida del pueblo Colla?",
    )

    # ── PÁG 8: DIAGUITA ──────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Diaguita",
        color_banner=HexColor('#9A5A20'),
        color_acento=HexColor('#D48A40'),
        campos=[
            ("Zona",
             "Norte Chico: valles del río Huasco y del río Choapa."),
            ("Territorio",
             "Valles transversales, precordillera, quebradas y terrazas agrícolas."),
            ("Clima",
             "Semiárido, con sectores de desierto frío y desierto de montaña en altura."),
            ("Relieve",
             "Valles encajonados, quebradas, montañas, precordillera y terrazas."),
            ("Agua y recursos",
             "Ríos Huasco, Tránsito, Carmen, Choapa y afluentes cordilleranos."),
            ("Vegetación",
             "Hierbas, cactáceas, arbustos, gramíneas, pastos de altura "
             "y vegetación adaptada a zonas semiáridas."),
            ("Forma de vida",
             "El acceso a valles y ríos favoreció la agricultura, "
             "los asentamientos y el uso de terrazas."),
        ],
        expresiones=(
            "Alfarería, diseños geométricos, trabajo agrícola, "
            "identidad territorial y relación con los valles."
        ),
        museo_texto=(
            "Dibujo de cerámica diaguita, mapa del valle, maqueta de terraza "
            "agrícola o patrón geométrico."
        ),
        pregunta_texto="¿Cómo ayudaron los ríos y valles al desarrollo del pueblo Diaguita?",
    )

    # ── PÁG 9: CHANGO ────────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Chango",
        color_banner=AZUL,
        color_acento=AZUL_CLARO,
        campos=[
            ("Zona",
             "Costa del norte de Chile, desde el desierto de Atacama "
             "hacia Coquimbo y otros sectores costeros."),
            ("Territorio",
             "Franja costera del norte, entre la Cordillera de la Costa, "
             "el desierto y el Océano Pacífico."),
            ("Clima",
             "Costero desértico, con escasas lluvias y presencia de camanchaca."),
            ("Relieve",
             "Costa, acantilados, playas, desierto costero y Cordillera de la Costa."),
            ("Agua y recursos",
             "Océano Pacífico, Corriente de Humboldt, peces, mariscos, "
             "algas, aves y mamíferos marinos."),
            ("Vegetación",
             "Vegetación costera asociada a la humedad de la camanchaca "
             "en algunos sectores."),
            ("Forma de vida",
             "Su vida estuvo fuertemente relacionada con el mar: pesca, "
             "recolección de mariscos, navegación y aprovechamiento de recursos marinos."),
        ],
        expresiones=(
            "Embarcaciones, pesca, recolección, intercambio de productos "
            "marinos y conocimientos del litoral."
        ),
        museo_texto=(
            "Maqueta de costa, dibujo de embarcación, ficha sobre "
            "Corriente de Humboldt o muestra visual de recursos marinos."
        ),
        pregunta_texto="¿Por qué el mar fue central para la vida del pueblo Chango?",
    )

    # ── PÁG 10: RAPA NUI ─────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Rapa Nui",
        color_banner=HexColor('#1A6B8A'),
        color_acento=HexColor('#60A8C8'),
        campos=[
            ("Zona",
             "Isla Rapa Nui, en el Océano Pacífico sur."),
            ("Territorio",
             "Isla de origen volcánico, con costa, cráteres, cuevas, "
             "suelos volcánicos y mar abierto."),
            ("Clima",
             "Subtropical, con temperatura media cercana a 21 °C."),
            ("Relieve",
             "Volcanes, cráteres, laderas, costa rocosa y zonas interiores."),
            ("Agua y recursos",
             "No posee cauces permanentes; cuenta con aguas subterráneas "
             "y recursos marinos."),
            ("Vegetación",
             "Actualmente sabana con matorrales y arbustos; "
             "antiguamente tuvo mayor presencia de bosques."),
            ("Forma de vida",
             "El aislamiento insular, el mar y los recursos disponibles influyeron "
             "en su organización, alimentación, navegación, agricultura y cultura."),
        ],
        expresiones=(
            "Lengua rapa nui, moai, ahu, música, danza, relatos, "
            "tallado y patrimonio arqueológico."
        ),
        museo_texto=(
            "Mapa de la isla, dibujo de moai, ficha de volcanes, "
            "audio musical o línea de tiempo cultural."
        ),
        pregunta_texto="¿Cómo influye vivir en una isla en la cultura de un pueblo?",
    )

    # ── PÁG 11: MAPUCHE ──────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Mapuche",
        color_banner=VERDE,
        color_acento=VERDE_CLARO,
        campos=[
            ("Zona",
             "Centro-sur y sur de Chile, con presencia histórica "
             "desde zonas de cordillera hasta la costa."),
            ("Territorio",
             "Valles, bosques, ríos, lagos, costa, precordillera y cordillera."),
            ("Clima",
             "Templado, con zonas lluviosas y frías hacia el sur."),
            ("Relieve",
             "Cordillera, valle central, costa, ríos, lagos, bosques y zonas agrícolas."),
            ("Agua y recursos",
             "Ríos, lagos, bosques, suelos agrícolas, plantas medicinales "
             "y recursos del territorio."),
            ("Vegetación",
             "Bosque nativo, vegetación de zonas templadas y plantas "
             "de uso alimenticio y medicinal."),
            ("Forma de vida",
             "Históricamente desarrollaron agricultura, recolección, "
             "crianza de animales y fuerte vínculo comunitario con el territorio."),
        ],
        expresiones=(
            "Mapudungun, platería, tejidos, relatos, música, "
            "medicina tradicional, ceremonias y organización comunitaria."
        ),
        museo_texto=(
            "Mapa del Wallmapu, glosario mapudungun, tejido, símbolo, "
            "relato breve o ficha sobre bosque nativo."
        ),
        pregunta_texto="¿Cómo se relaciona el pueblo Mapuche con el territorio y la naturaleza?",
    )

    # ── PÁG 12: KAWASHKAR ────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Kawashkar",
        color_banner=HexColor('#1A4A6B'),
        color_acento=HexColor('#4A8AAA'),
        campos=[
            ("Zona",
             "Canales australes, desde el Golfo de Penas hasta sectores "
             "cercanos al Canal Cockburn y Estrecho de Magallanes."),
            ("Territorio",
             "Archipiélagos, islas, canales, fiordos y bosques magallánicos."),
            ("Clima",
             "Frío, lluvioso y ventoso, con inviernos de bajas temperaturas "
             "y veranos frescos."),
            ("Relieve",
             "Canales, islas, montañas, costa irregular y bosques australes."),
            ("Agua y recursos",
             "Canales navegables, mar, fauna marina, peces, moluscos "
             "y recursos costeros."),
            ("Vegetación",
             "Bosque magallánico denso y vegetación austral."),
            ("Forma de vida",
             "Su vida estuvo vinculada a la navegación en canoas, "
             "la movilidad por canales y el uso de recursos marinos."),
        ],
        expresiones=(
            "Conocimiento de navegación, canoas, relatos, "
            "campamentos costeros y relación con el mar austral."
        ),
        museo_texto=(
            "Maqueta de canoa, mapa de canales australes, "
            "ficha sobre navegación o ambientación sonora de lluvia y mar."
        ),
        pregunta_texto="¿Por qué la navegación fue fundamental para el pueblo Kawashkar?",
    )

    # ── PÁG 13: YÁMANA / YAGÁN ───────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Yámana o Yagán",
        color_banner=HexColor('#15395A'),
        color_acento=HexColor('#3A7A9A'),
        campos=[
            ("Zona",
             "Canales al sur de Tierra del Fuego y archipiélago del Cabo de Hornos."),
            ("Territorio",
             "Zona austral extrema, canales fueguinos, islas, costas y archipiélagos."),
            ("Clima",
             "Frío, lluvioso y ventoso, con temperaturas bajas."),
            ("Relieve",
             "Islas, canales, costa irregular, montañas y sectores boscosos."),
            ("Agua y recursos",
             "Mar, canales, peces, moluscos, aves y mamíferos marinos."),
            ("Vegetación",
             "Bosque austral y vegetación adaptada al frío y humedad."),
            ("Forma de vida",
             "Fueron navegantes de los canales australes. Su vida se relacionó "
             "con la canoa, el mar, la pesca, la recolección y la movilidad costera."),
        ],
        expresiones=(
            "Lengua yagán, relatos, navegación, cestería, "
            "vida familiar en campamentos y conocimiento del clima austral."
        ),
        museo_texto=(
            "Mapa del Cabo de Hornos, maqueta de canoa, "
            "ficha sobre recursos marinos o audio de paisaje austral."
        ),
        pregunta_texto="¿Cómo influyó el clima frío y el mar en la vida del pueblo Yámana/Yagán?",
    )

    # ── PÁG 14: SELK'NAM ─────────────────────────────────────────────────────
    story += seccion_pueblo(
        nombre="Pueblo Selk'nam",
        color_banner=HexColor('#5A2D7A'),
        color_acento=HexColor('#9A6DBA'),
        campos=[
            ("Zona",
             "Isla Grande de Tierra del Fuego."),
            ("Territorio",
             "Praderas ventosas del norte y zonas boscosas, montañosas "
             "y lacustres del sur de Tierra del Fuego."),
            ("Clima",
             "Inhóspito, con veranos cortos y frescos e inviernos largos, "
             "húmedos y fríos."),
            ("Relieve",
             "Praderas, bosques, montañas, lagos, costa y pampa fueguina."),
            ("Agua y recursos",
             "Lagos, costa, animales terrestres y marinos, "
             "moluscos y recursos de la pampa."),
            ("Vegetación",
             "Pastizales, bosques australes y vegetación adaptada al frío."),
            ("Forma de vida",
             "Tradicionalmente fueron cazadores-recolectores terrestres. "
             "Su movilidad se relacionaba con la búsqueda de recursos, "
             "especialmente guanacos y otros animales."),
        ],
        expresiones=(
            "Relatos, pintura corporal, ceremonias, "
            "conocimiento del territorio y sistema de creencias."
        ),
        museo_texto=(
            "Mapa de Tierra del Fuego, representación respetuosa de pintura corporal, "
            "ficha sobre guanaco o paisaje de pampa fueguina."
        ),
        pregunta_texto="¿Cómo se adaptó el pueblo Selk'nam al clima y territorio de Tierra del Fuego?",
    )

    # ── PÁG 15: GLOSARIO ─────────────────────────────────────────────────────
    story.append(BannerHeader("Palabras clave para investigar",
                               color_fondo=TIERRA, color_acento=OCRE))
    story.append(Spacer(1, 0.3*cm))

    terminos = [
        ("Pueblo originario",
         "Grupo humano que habitaba un territorio antes de la formación del Estado "
         "actual y que mantiene identidad, historia, cultura y formas propias de vida."),
        ("Territorio",
         "Espacio geográfico donde vive o ha vivido una comunidad, "
         "incluyendo naturaleza, recursos, historia y significado cultural."),
        ("Clima",
         "Conjunto de condiciones atmosféricas habituales de un lugar, "
         "como temperatura, lluvia, humedad y viento."),
        ("Relieve",
         "Formas que tiene la superficie terrestre, como montañas, valles, "
         "desiertos, islas, costas, lagos o cordilleras."),
        ("Vegetación",
         "Conjunto de plantas que crecen en un territorio."),
        ("Recursos naturales",
         "Elementos de la naturaleza que las comunidades pueden utilizar, "
         "como agua, tierra, animales, plantas, minerales o productos del mar."),
        ("Identidad cultural",
         "Conjunto de costumbres, lengua, conocimientos, relatos, símbolos, "
         "valores y formas de vida que caracterizan a un pueblo o comunidad."),
        ("Medioambiente",
         "Conjunto de elementos naturales y sociales que rodean a los seres vivos."),
        ("Interculturalidad",
         "Relación respetuosa entre distintas culturas, "
         "reconociendo sus saberes, derechos e identidades."),
        ("Patrimonio",
         "Bienes, conocimientos, expresiones, tradiciones o lugares que tienen "
         "valor para una comunidad y deben ser respetados y transmitidos."),
    ]

    col_a = []
    col_b = []
    for i, (term, defn) in enumerate(terminos):
        bloque = [
            Paragraph(term, ST['glosario_term']),
            Paragraph(defn, ST['glosario_def']),
        ]
        if i % 2 == 0:
            col_a.append(bloque)
        else:
            col_b.append(bloque)

    # Aplanar bloques en columnas
    items_a = []
    for bl in col_a:
        items_a.extend(bl)
    items_b = []
    for bl in col_b:
        items_b.extend(bl)

    # Construir tabla de dos columnas
    filas_glos = []
    max_len = max(len(col_a), len(col_b))
    for i in range(max_len):
        celd_a = []
        celd_b = []
        if i < len(col_a):
            celd_a = col_a[i]
        if i < len(col_b):
            celd_b = col_b[i]

        inner_a = Table([[p] for p in celd_a],
                         colWidths=[(W - 3*cm)/2 - 0.3*cm]) if celd_a else Table([['']])
        inner_b = Table([[p] for p in celd_b],
                         colWidths=[(W - 3*cm)/2 - 0.3*cm]) if celd_b else Table([['']])
        for tb in [inner_a, inner_b]:
            tb.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), HexColor('#FBF6EC')),
                ('BOX', (0,0), (-1,-1), 1, HexColor('#C8B89A')),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
        filas_glos.append([inner_a, inner_b])

    ancho_col = (W - 3*cm) / 2 - 0.2*cm
    t_glos = Table(filas_glos, colWidths=[ancho_col + 0.3*cm, ancho_col])
    t_glos.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_glos)
    story.append(PageBreak())

    # ── PÁG 16: FUENTES CONSULTADAS ──────────────────────────────────────────
    story.append(BannerHeader("Fuentes oficiales e institucionales consultadas",
                               color_fondo=MARRON, color_acento=TIERRA))
    story.append(Spacer(1, 0.4*cm))

    fuentes = [
        ("1.", "Biblioteca del Congreso Nacional de Chile. <i>Ley N° 19.253 sobre protección, "
               "fomento y desarrollo de los indígenas.</i>"),
        ("2.", "Biblioteca del Congreso Nacional de Chile. Informe: <i>\"Los pueblos indígenas "
               "y sus comunidades en Chile: reconocimiento y distribución geográfica\".</i>"),
        ("3.", "Ministerio de las Culturas, las Artes y el Patrimonio. "
               "<i>\"Recomendaciones para nombrar y escribir sobre pueblos indígenas "
               "y Tribal Afrodescendiente chileno\".</i>"),
        ("4.", "Museo Chileno de Arte Precolombino / Chile Precolombino. Secciones de "
               "ambiente, localización, historia, economía, arte y lengua "
               "de los pueblos originarios."),
        ("5.", "Biblioteca Nacional de Chile / Memoria Chilena."),
        ("6.", "Chile Para Niños / Biblioteca Nacional de Chile."),
    ]

    ancho_f = W - 3*cm
    for num, texto in fuentes:
        n_p = Paragraph(f"<b>{num}</b>", ST['campo_label'])
        t_p = Paragraph(texto, ST['fuente'])
        row = Table([[n_p, t_p]], colWidths=[0.6*cm, ancho_f - 0.6*cm])
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(row)
        story.append(HRFlowable(width=ancho_f, thickness=0.5,
                                 color=HexColor('#C8B89A'), spaceAfter=3))

    story.append(Spacer(1, 0.6*cm))

    # Nota final
    nota_final_txt = (
        "Esta revista fue elaborada con fines educativos. La información está "
        "resumida y adaptada para estudiantes de 7° y 8° básico. No está "
        "destinada a usos comerciales. Las ubicaciones en el mapa son "
        "aproximadas y sirven con fines pedagógicos."
    )
    ancho_nf = W - 3*cm
    nota_p = Paragraph(nota_final_txt, ST['nota'])
    t_nota_final = Table([[nota_p]], colWidths=[ancho_nf])
    t_nota_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F5EDD6')),
        ('BOX', (0,0), (-1,-1), 1.5, TIERRA),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_nota_final)

    return story


# ── Callbacks de página ────────────────────────────────────────────────────────

_pagina_global = [1]

def on_first_page(c_obj, doc):
    """Primera página = portada."""
    portada(c_obj, doc)


def on_later_pages(c_obj, doc):
    """Todas las páginas internas."""
    encabezado_pie(c_obj, doc)


# ── Punto de entrada ──────────────────────────────────────────────────────────

def main():
    output = "/home/user/ESCUELAHOSPITALGERSSON/Raices_que_nos_unen.pdf"

    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.4*cm,
        bottomMargin=1.2*cm,
        title="Raíces que nos unen",
        author="Recurso educativo ABP",
        subject="Pueblos originarios de Chile",
    )

    story = construir_revista()

    doc.build(
        story,
        onFirstPage=on_first_page,
        onLaterPages=on_later_pages,
    )
    print(f"PDF generado: {output}")
    return output


if __name__ == '__main__':
    main()
