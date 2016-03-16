#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import urwid
import time
import re

# 16 Standard Foreground Colors
#
# 'black'
# 'dark red'
# 'dark green'
# 'brown'
# 'dark blue'
# 'dark magenta'
# 'dark cyan'
# 'light gray'
# 'dark gray'
# 'light red'
# 'light green'
# 'yellow'
# 'light blue'
# 'light magenta'
# 'light cyan'
# 'white'
#
# 8 Standard Background Colors
#
# 'black'
# 'dark red'
# 'dark green'
# 'brown'
# 'dark blue'
# 'dark magenta'
# 'dark cyan'
# 'light gray'
#
# Bold, Underline, Standout
#
# 'bold'
# 'underline'
# 'standout'      -- most supported
#


palette = [
    ('body',        'light gray', 'black'),
    ('outline',     'light gray', 'black'),
    ('clock',       'light blue', 'black'),
    ('title',       'light gray', 'black'),
    ('div',         'dark gray',  'black'),
    ('normal',      'light gray', 'black'),
    ('error',       'white',      'dark red'),
    ('processing',  'black',      'yellow'),
    ('success',     'black',      'dark green'),
    ('pending',     'yellow',     'black'),
]

txt = urwid.Text(('banner', u" Hello World "), align='center')
box = urwid.LineBox(txt)
map1 = urwid.AttrMap(box, 'streak')
fill = urwid.Filler(map1, valign='top', top=2)
map2 = urwid.AttrMap(fill, 'bg')

def text(txt, style=None):
    txt = urwid.Text(txt, align='center', wrap='any')
    if style:
        txt = urwid.AttrMap(txt, style)
    return txt

##############################################################################
# HEADER                                                                     #
##############################################################################
header = urwid.Text(u'МЕХАНИЧЕН ДИЗАЙН И КОНСТРУКЦИИ ООД', align='center')


##############################################################################
# TOP                                                                        #
##############################################################################
now = time.localtime()
date_widget = text('...', 'clock')
time_widget = text('...', 'clock')
title_widget = text(u'СИСТЕМА ЗА УПРАВЛЕНИЕ НА ПРОИЗВОДСТВОТО - КОМАНДИР.НЕТ', 'title')


top_line1 = urwid.Columns([
  ('weight', 12, date_widget),
  ('weight', 54, title_widget),
  ('weight', 10, time_widget)
])

top_line2 = urwid.Columns([
  ('weight', 14, text(u'ТЕРМИНАЛ:123')),
  ('weight', 36, text(u'ОПЕРАЦИЯ:10 ОПЕРАЦИИ ПРЕДИ ОГЪВАНЕ')),
  ('weight', 26, text(u'РАБОТНИК:123 КОСТАДИН К.'))
], dividechars=1)


##############################################################################
# MIDDLE                                                                        #
##############################################################################
mid_tablehead = urwid.Columns([
  ('weight', 2, text(u'No')),
  ('weight', 8, text(u'ПОРЪЧКА')),
  ('weight', 16, text(u'КЛИЕНТ')),
  ('weight', 16, text(u'ИЗДЕЛИЕ')),
  ('weight', 21, text(u'ОЗНАЧЕНИЕ')),
  ('weight', 4, text(u'КОЛ.')),
  ('weight', 5, text(u'ПАПКА')),
], dividechars=1)

mid_tablerow = urwid.Columns([
  ('weight', 2, text('01')),
  ('weight', 8, text('16.03.45')),
  ('weight', 16, text(u'ЛОРЕН НЕТУЪРКС')),
  ('weight', 16, text('')),
  ('weight', 21, text('')),
  ('weight', 4, text('1000')),
  ('weight', 5, text('')),
], dividechars=1)


mid_table = urwid.Pile([
  (1, urwid.Filler(mid_tablehead)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
  (1, urwid.Filler(mid_tablerow)),
])


txt = '''Lorem ipsum dolor sit amet, no assum facilisi argumentum his, ius eu vocibus reprehendunt. Et nec vitae indoctum voluptatum, cu duo nihil impedit disputationi. Civibus postulant efficiendi ad nec. Sed labores maluisset elaboraret cu, nemore fierent mediocrem id quo. Id iuvaret feugiat expetenda ius, discere salutatus deterruisset qui at. Exerci inermis ius in, sumo veri referrentur ius an. Vis tantas recusabo et, eu vivendo pertinax has, ut sed idque everti.'''
mid_text = urwid.Filler(urwid.Text(txt), valign='top', height='pack')


##############################################################################
# BOTTOM                                                                     #
##############################################################################
# Fields
# bot_field = urwid.Text(u'НЕВАЛИДЕН БАРКОД', align='center')
input_field = urwid.Text(u'', align='center')
# input_field = urwid.Edit(u'', align='center')
input_field = urwid.AttrMap(input_field, 'normal')

##############################################################################
# ALL                                                                        #
##############################################################################

# pile = urwid.Pile([
#   ('pack', top_grid),
#   ('weight',12, urwid.LineBox(mid_pile)),
#   ('weight',12, urwid.LineBox(mid_text)),
#   ('pack', bot_field)
# ])

div = urwid.Divider(u'\N{BOX DRAWINGS LIGHT HORIZONTAL}')
div = urwid.AttrMap(div, 'div')
blankdiv = urwid.Divider(u' ')
bpile = urwid.Pile([])
pile = urwid.AttrMap(bpile, 'body')

# pile.contents.append((urwid.Padding(div, left=20, right=20), ('pack', None)))
bpile.contents.append((blankdiv, ('pack', None)))
bpile.contents.append((top_line1, ('pack', None)))
bpile.contents.append((div, ('pack', None)))
bpile.contents.append((top_line2, ('pack', None)))
bpile.contents.append((div, ('pack', None)))
bpile.contents.append((mid_table, ('pack', None)))
bpile.contents.append((div, ('pack', None)))
bpile.contents.append((urwid.Padding(mid_text, left=1, right=1), ('weight', 1)))
bpile.contents.append((div, ('pack', None)))
# bpile.contents.append((input_field, ('pack', None)))

bot_field = urwid.Padding(input_field, left=1, right=1)
# bot_field = urwid.AttrMap('normal', bot_field)
bpile.contents.append((bot_field, ('pack', None)))

bpile.set_focus(bot_field)

#
# Fake 80/25 display
#
outline = urwid.LineBox(pile, title=u'МЕХАНИЧЕН ДИЗАЙН И КОНСТРУКЦИИ ООД')
outline = urwid.AttrMap(outline, 'outline')

sichko = urwid.Overlay(outline, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    width=80,
    height=25,
    # width=180,
    # height=125,
    align='center',
    valign='middle')


# def on_input_field_change(edit, new_edit_text, widget):
#     if len(new_edit_text) == 0:
#         widget.set_attr_map({None: 'normal'})
#     if len(new_edit_text) == 12:
#         widget.set_attr_map({None: 'success'})
#     else:
#         widget.set_attr_map({None: 'error'})

global current_operation
current_operation = None

def clear_output(loop, operation):
    global current_operation
    if operation is current_operation:
        input_field.base_widget.set_text('')
        input_field.set_attr_map({None: 'normal '})


def process_barcode(barcode):
    time.sleep(1)

def on_input(key):
    if key == 'enter':
        submit()
    elif key in '1234567890':
        valid_input(key)
    else:
        invalid_input(key)

def valid_input(key):
    global current_operation
    current_text = input_field.base_widget.get_text()[0]

    if current_operation:
        current_operation = None
        current_text = ''

    input_field.base_widget.set_text(current_text + key)
    input_field.set_attr_map({None: 'pending'})


def invalid_input(key):
    # Ignore any invalid input for now
    pass


def submit():
    global current_operation

    current_text = input_field.base_widget.get_text()[0]
    current_operation = time.time()
    input_field.set_attr_map({None: 'processing'})
    main_loop.draw_screen()
    res = process_barcode(current_text)

    if res == 0:
        style = 'success'
    elif res == 63:
        style = 'warning'
    else:
        style = 'error'

    input_field.set_attr_map({None: style})
    main_loop.set_alarm_in(3, clear_output, current_operation)



def update_clock(loop, (period, date_widget, time_widget)):
    now = time.localtime()
    date_widget.base_widget.set_text(time.strftime('%d.%m.%Y', now))
    time_widget.base_widget.set_text(time.strftime('%H:%M:%S', now))

    loop.set_alarm_in(period, update_clock, (period, date_widget, time_widget))


# urwid.connect_signal(input_field.base_widget, 'change', on_input_field_change, input_field)

main_loop = urwid.MainLoop(sichko, palette, unhandled_input=on_input)

period = 0.5
main_loop.set_alarm_in(period, update_clock, (period, date_widget, time_widget))
# pdb.set_trace()

main_loop.run()

