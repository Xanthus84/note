import gi
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.styles import ParagraphStyle as PS, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Spacer

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from reportlab.pdfbase.ttfonts import TTFont


# whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))

def create_a_report(lStore_now, lStore_medium, lStore_perspective, place):
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))  # импорт и регистрация шрифта с поддержкой
    # кириллицы, файл должен располагаться в папке приложения
    pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', 'DejaVuSerif-Bold.ttf'))  # импорт и регистрация шрифта с
    # поддержкой кириллицы, файл должен располагаться в папке приложения
    doc = SimpleDocTemplate(place + "\\ToDoIt.pdf", pagesize=A4, initialFontName="DejaVuSerif",
                            initialFontSize=14)  # создание документа
    elements = []  # список для будущего хранения данных для сохранения в документе
    # whatis(doc)
    styles1 = getSampleStyleSheet()  # импорт базового стиля
    styles1.add(PS(name='DejaVuSerif',  # настройка стиля параграфа
                   fontName='DejaVuSerif-Bold',
                   fontSize=16,
                   alignment=TA_CENTER
                   ))
    table_contents1 = [['№', 'Заметка', 'Дата']]  # список для контента списка срочных дел + заголовки
    table_contents2 = [['№', 'Заметка', 'Дата']]  # список для контента списка среднесрочных дел + заголовки
    table_contents3 = [['№', 'Заметка', 'Дата']]  # список для контента списка перспективных дел + заголовки
    # сохранение значений из базы данных в списки
    for i in range(2, len(lStore_now) + 2):
        path = Gtk.TreePath(i - 2)  # перебор строк с присвоением в path
        treeiter = lStore_now.get_iter(path)
        table_contents1.append([
            lStore_now.get_value(treeiter, 0),
            lStore_now.get_value(treeiter, 1),
            lStore_now.get_value(treeiter, 2),
        ])
    for i in range(2, len(lStore_medium) + 2):
        path = Gtk.TreePath(i - 2)  # перебор строк с присвоением в path
        treeiter = lStore_medium.get_iter(path)
        table_contents2.append([
            lStore_medium.get_value(treeiter, 0),
            lStore_medium.get_value(treeiter, 1),
            lStore_medium.get_value(treeiter, 2),
        ])
    for i in range(2, len(lStore_perspective) + 2):
        path = Gtk.TreePath(i - 2)  # перебор строк с присвоением в path
        treeiter = lStore_perspective.get_iter(path)
        table_contents3.append([
            lStore_perspective.get_value(treeiter, 0),
            lStore_perspective.get_value(treeiter, 1),
            lStore_perspective.get_value(treeiter, 2),
        ])

    t1 = Table(table_contents1)  # загрузка контента в конструктор таблицы
    t2 = Table(table_contents2)  # загрузка контента в конструктор таблицы
    t3 = Table(table_contents3)  # загрузка контента в конструктор таблицы
    # установка стилей таблицы
    t1.setStyle(TableStyle([('FONT', (0, 0), (2, 0), "DejaVuSerif-Bold", 14),
                            ('FONT', (0, 1), (-1, -1), "DejaVuSerif", 12),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 2, colors.black),
                            ]))
    t2.setStyle(TableStyle([('FONT', (0, 0), (2, 0), "DejaVuSerif-Bold", 14),
                            ('FONT', (0, 1), (-1, -1), "DejaVuSerif", 12),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 2, colors.black),
                            ]))
    t3.setStyle(TableStyle([('FONT', (0, 0), (2, 0), "DejaVuSerif-Bold", 14),
                            ('FONT', (0, 1), (-1, -1), "DejaVuSerif", 12),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                            ('BOX', (0, 0), (-1, -1), 2, colors.black),
                            ]))
    # добавление элементов в список для сохранения в документе
    elements.append(Paragraph('Список срочных дел', styles1["DejaVuSerif"]))
    elements.append(Spacer(1, 24))  # пустая строка
    elements.append(t1)
    elements.append(PageBreak())  # Признак начала с новой страницы
    elements.append(Paragraph('Список среднесрочных дел', styles1["DejaVuSerif"]))
    elements.append(Spacer(1, 24))  # пустая строка
    elements.append(t2)
    elements.append(PageBreak())  # Признак начала с новой страницы
    elements.append(Paragraph('Список перспективных дел', styles1["DejaVuSerif"]))
    elements.append(Spacer(1, 24))  # пустая строка
    elements.append(t3)

    try:
        doc.multiBuild(elements)  # многостраничное сохранение
        return "OK"
    except:
        return "Error"
