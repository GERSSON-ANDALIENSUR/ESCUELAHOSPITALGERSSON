#!/usr/bin/env python3
"""Genera el Bingo de Pueblos Originarios de Chile - 24 cartones."""

import random
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from collections import Counter

random.seed(42)

# ─────────────────────────────────────────────────────────────
# DATOS
# ─────────────────────────────────────────────────────────────
ELEMENTS = [
    "Mapuche", "Aymara", "Rapa Nui", "Quechua", "Atacameño", "Colla",
    "Diaguita", "Chango", "Kawésqar", "Yagán", "Selk'nam", "Moai",
    "Kultrún", "Trarilonco", "Vasija Diaguita", "Máscara Selk'nam",
    "Ruca", "Canoa", "Totora", "Alpaca", "Zampoña", "Cesta",
    "Quena", "Desierto",
]

CATEGORIES = [
    "Pueblo originario", "Pueblo originario", "Pueblo originario",
    "Pueblo originario", "Pueblo originario", "Pueblo originario",
    "Pueblo originario", "Pueblo originario", "Pueblo originario",
    "Pueblo originario", "Pueblo originario", "Objeto cultural",
    "Instrumento musical", "Objeto cultural", "Objeto cultural",
    "Objeto cultural", "Vivienda o construcción", "Objeto cultural",
    "Elemento natural o territorial", "Animal",
    "Instrumento musical", "Objeto cultural",
    "Instrumento musical", "Elemento natural o territorial",
]

PROMPTS = [
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Mapuche, con fondo de naturaleza del sur de Chile, bosques nativos y colores cálidos. Estilo educativo, colorido y respetuoso. Sin texto, sin logos, sin marcas de agua, sin caricaturizar. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Aymara, con paisaje de altiplano, montañas nevadas, cielo azul y colores andinos vibrantes. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Rapa Nui, con fondo de isla tropical, mar azul y vegetación verde. Estilo educativo, alegre y colorido. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Quechua, con paisaje andino colorido, textiles tradicionales y montañas de fondo. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Atacameño, con desierto de Atacama, oasis, montañas del norte de Chile y colores tierra cálidos. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Colla, con paisaje cordillerano del norte de Chile, animales andinos y cielo cálido. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Diaguita, con cerámica geométrica colorida, valle del norte chico y colores tierra vibrantes. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Chango, con costa del Pacífico, mar azul, pesca artesanal y embarcación tradicional. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Kawésqar, con canales australes, canoa tradicional, mar frío y paisaje verde del extremo sur de Chile. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Yagán, con canales australes de Tierra del Fuego, canoa, maritorio y paisaje frío y nublado. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una representación respetuosa del pueblo Selk'nam, con paisaje de Tierra del Fuego, tonos naturales y enfoque cultural respetuoso, sin teatralizar ceremonias. Estilo educativo. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de un moai de Rapa Nui construido con bloques LEGO, sobre una plataforma ahu sencilla, con pasto verde, cielo azul y mar al horizonte. Estilo educativo y colorido. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de un kultrún mapuche como objeto cultural, sobre una mesa con sus diseños geométricos visibles, fondo neutro cálido y respetuoso, sin representar rituales. Estilo educativo. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de un trarilonco como pieza ornamental mapuche en plata, presentado en una vitrina de museo intercultural con fondo neutro claro. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una vasija diaguita con diseños geométricos en rojo y negro, sobre fondo de museo intercultural con colores tierra cálidos. Estilo educativo y respetuoso. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una máscara ceremonial Selk'nam como objeto cultural de museo, con colores naturales y presentada con respeto sobre fondo neutro. Sin burlarse de ceremonias. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una ruca mapuche construida con bloques LEGO, en un entorno natural del sur de Chile con árboles nativos, pasto verde y cielo claro. Estilo educativo y colorido. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una canoa tradicional de pueblos canoeros australes, flotando en canales del sur de Chile con montañas nevadas y agua fría. Estilo educativo y colorido. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una planta de totora en un humedal andino, junto a un lago con montañas al fondo y cielo azul. Estilo educativo y colorido. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una alpaca andina esponjosa y colorida, en un paisaje de altiplano con montañas, paja brava y cielo despejado. Estilo educativo y simpático. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una zampoña andina como instrumento musical, presentada sobre una manta tejida con patrones andinos coloridos y fondo de montañas. Estilo educativo. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una cesta artesanal tejida con fibras naturales y patrones geométricos coloridos, presentada sobre fondo cálido y simple. Estilo educativo. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de una quena andina como instrumento musical de viento, sobre una manta con patrones andinos coloridos y fondo de altiplano con montañas. Estilo educativo. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
    "Crea una imagen cuadrada en formato LEGO animado 3D de un paisaje del desierto de Atacama con arena dorada, formaciones rocosas, cielo azul intenso y un pequeño oasis con agua al fondo. Estilo educativo y colorido. Sin texto, sin logos, sin marcas de agua. Imagen clara para tarjeta de bingo escolar.",
]

# ─────────────────────────────────────────────────────────────
# GENERACIÓN DE CARTONES (diseño circulante equilibrado)
# Cada elemento aparece exactamente 12 veces en los 24 cartones.
# ─────────────────────────────────────────────────────────────
def generate_cards():
    cards = []
    for i in range(24):
        card = [ELEMENTS[(i + j) % 24] for j in range(12)]
        random.shuffle(card)
        cards.append(card)
    return cards


# ─────────────────────────────────────────────────────────────
# UTILIDADES DE ESTILO
# ─────────────────────────────────────────────────────────────
def border(style="medium"):
    s = Side(style=style)
    return Border(left=s, right=s, top=s, bottom=s)


def cell_style(ws, row, col, value, *, font_size=12, bold=False,
               bg_color=None, font_color="2C1810", h_align="center",
               wrap=True, border_style="medium"):
    cell = ws.cell(row=row, column=col)
    cell.value = value
    cell.font = Font(name="Calibri", size=font_size, bold=bold, color=font_color)
    cell.alignment = Alignment(horizontal=h_align, vertical="center", wrap_text=wrap)
    if bg_color:
        cell.fill = PatternFill(start_color=bg_color, end_color=bg_color,
                                fill_type="solid")
    cell.border = border(border_style)
    return cell


# ─────────────────────────────────────────────────────────────
# HOJA 1 – CARTONES BINGO
# ─────────────────────────────────────────────────────────────
# Paleta: (fondo casilla, fondo título, color texto título)
SCHEMES = [
    ("FFF3E0", "E65100", "FFFFFF"),   # Naranja tierra
    ("E8F5E9", "2E7D32", "FFFFFF"),   # Verde naturaleza
    ("E3F2FD", "1565C0", "FFFFFF"),   # Azul cielo
    ("FFFDE7", "F57F17", "FFFFFF"),   # Amarillo sol
    ("F3E5F5", "6A1B9A", "FFFFFF"),   # Violeta suave
    ("FBE9E7", "BF360C", "FFFFFF"),   # Terracota
]


def build_sheet1(wb, cards):
    ws = wb.active
    ws.title = "Cartones Bingo"

    COLS_PER_CARD = 4
    DATA_ROWS = 3
    CARDS_PER_ROW = 3
    COL_GAP = 2      # columnas vacías entre cartones
    ROW_GAP = 1      # fila vacía entre filas de cartones
    BLOCK_ROWS = 1 + DATA_ROWS + ROW_GAP  # 5 filas por bloque

    for idx, card in enumerate(cards):
        c_row = idx // CARDS_PER_ROW
        c_col = idx % CARDS_PER_ROW

        sr = c_row * BLOCK_ROWS + 1                     # fila inicio
        sc = c_col * (COLS_PER_CARD + COL_GAP) + 1     # col inicio

        bg, title_bg, title_fg = SCHEMES[idx % len(SCHEMES)]

        # ── Título (celda combinada) ──────────────────────────
        title_cell = ws.cell(row=sr, column=sc)
        title_cell.value = f"Cartón {idx + 1}"
        title_cell.font = Font(name="Calibri", size=14, bold=True, color=title_fg)
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        title_cell.fill = PatternFill(start_color=title_bg, end_color=title_bg,
                                      fill_type="solid")

        # Borde exterior de la fila título (celdas individuales antes de combinar)
        med = Side(style="medium")
        thin = Side(style="thin")
        for c_off in range(COLS_PER_CARD):
            tc = ws.cell(row=sr, column=sc + c_off)
            is_first = c_off == 0
            is_last = c_off == COLS_PER_CARD - 1
            tc.border = Border(
                left=med if is_first else Side(style=None),
                right=med if is_last else Side(style=None),
                top=med,
                bottom=thin,
            )
            tc.fill = PatternFill(start_color=title_bg, end_color=title_bg,
                                  fill_type="solid")

        ws.merge_cells(start_row=sr, start_column=sc,
                       end_row=sr, end_column=sc + COLS_PER_CARD - 1)

        # ── Casillas de datos ─────────────────────────────────
        for r in range(DATA_ROWS):
            for c in range(COLS_PER_CARD):
                elem = card[r * COLS_PER_CARD + c]
                dcell = ws.cell(row=sr + 1 + r, column=sc + c)
                dcell.value = elem
                dcell.font = Font(name="Calibri", size=12, bold=False, color="2C1810")
                dcell.alignment = Alignment(horizontal="center", vertical="center",
                                            wrap_text=True)
                dcell.fill = PatternFill(start_color=bg, end_color=bg,
                                         fill_type="solid")

                is_top = r == 0
                is_bottom = r == DATA_ROWS - 1
                is_left = c == 0
                is_right = c == COLS_PER_CARD - 1
                dcell.border = Border(
                    left=med if is_left else thin,
                    right=med if is_right else thin,
                    top=thin if is_top else thin,
                    bottom=med if is_bottom else thin,
                )

    # ── Anchos de columna ──────────────────────────────────────
    for c_col in range(CARDS_PER_ROW):
        sc = c_col * (COLS_PER_CARD + COL_GAP) + 1
        for off in range(COLS_PER_CARD):
            ws.column_dimensions[get_column_letter(sc + off)].width = 18
        for g in range(COL_GAP):
            ws.column_dimensions[get_column_letter(sc + COLS_PER_CARD + g)].width = 3

    # ── Altos de fila ─────────────────────────────────────────
    total_card_rows = (24 + CARDS_PER_ROW - 1) // CARDS_PER_ROW
    for c_row in range(total_card_rows):
        sr = c_row * BLOCK_ROWS + 1
        ws.row_dimensions[sr].height = 26        # título
        for r in range(1, DATA_ROWS + 1):
            ws.row_dimensions[sr + r].height = 42  # casillas
        ws.row_dimensions[sr + DATA_ROWS + 1].height = 10  # separador

    # ── Configuración de impresión ───────────────────────────
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_options.horizontalCentered = True


# ─────────────────────────────────────────────────────────────
# HOJA 2 – PROMPTS GEMINI
# ─────────────────────────────────────────────────────────────
def build_sheet2(wb):
    ws = wb.create_sheet("Prompts Gemini")

    headers = ["N°", "Elemento", "Categoría", "Prompt para Gemini"]
    header_bg = "1B5E20"
    alt_colors = ["FFFFFF", "F1F8E9"]

    # ── Encabezado ────────────────────────────────────────────
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=col)
        c.value = h
        c.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.fill = PatternFill(start_color=header_bg, end_color=header_bg,
                             fill_type="solid")
        c.border = border("medium")
    ws.row_dimensions[1].height = 30

    # ── Filas de datos ────────────────────────────────────────
    for i in range(24):
        row = i + 2
        bg = alt_colors[i % 2]
        row_data = [i + 1, ELEMENTS[i], CATEGORIES[i], PROMPTS[i]]
        aligns = ["center", "center", "center", "left"]

        for col, (val, align) in enumerate(zip(row_data, aligns), 1):
            c = ws.cell(row=row, column=col)
            c.value = val
            c.font = Font(name="Calibri", size=11)
            c.alignment = Alignment(horizontal=align, vertical="center",
                                    wrap_text=True)
            c.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
            c.border = border("thin")

        ws.row_dimensions[row].height = 72

    # ── Anchos de columna ──────────────────────────────────────
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 88

    # ── Impresión ─────────────────────────────────────────────
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    cards = generate_cards()

    # Verificaciones
    assert len(cards) == 24, "Número de cartones incorrecto"
    assert all(len(c) == 12 for c in cards), "Algún cartón no tiene 12 elementos"
    counts = Counter(e for c in cards for e in c)
    assert all(v == 12 for v in counts.values()), f"Distribución no equilibrada: {counts}"
    # Verificar que no haya dos cartones iguales (como conjuntos)
    sets = [frozenset(c) for c in cards]
    assert len(set(sets)) == 24, "Hay cartones duplicados"

    wb = Workbook()
    build_sheet1(wb, cards)
    build_sheet2(wb)

    output = "/home/user/ESCUELAHOSPITALGERSSON/Bingo_Pueblos_Originarios_24_Cartones.xlsx"
    wb.save(output)
    print(f"✓ Archivo guardado: {output}")

    print("\nDistribución de elementos (cada uno debe aparecer 12 veces):")
    for elem in ELEMENTS:
        print(f"  {counts[elem]:2d}×  {elem}")

    print(f"\n✓ 24 cartones generados")
    print(f"✓ 12 casillas por cartón")
    print(f"✓ 24 prompts en hoja 2")
    print(f"✓ Sin cartones duplicados")


if __name__ == "__main__":
    main()
