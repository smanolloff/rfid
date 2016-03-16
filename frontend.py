#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import urwid
import time
import re
import ConfigParser
import os
from backend import BarcodeProcessor

global master_config
master_config = ConfigParser.ConfigParser()
master_config.read('config.ini')
processor = BarcodeProcessor(master_config)
out_delay = float(master_config.get('timers', 'barcode_status'))
msg_refresh = float(master_config.get('timers', 'message_refresh'))
msg_scroll = float(master_config.get('timers', 'message_scroll'))
msg_file = processor.subconf_path('message')

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

PROCESSING_STYLES = {
  'normal':   ('black_on_green', 'green_on_black'),
  'invalid':  ('white_on_red', 'red_on_black'),
  'reserved': ('black_on_yellow', 'yellow_on_black'),
  'configure':  ('white_on_blue', 'blue_on_black'),
  'other':    ('black_on_white', 'white_on_black')
}


palette = [
    ('body',            'white', 'black'),
    ('outline',         'white', 'black'),
    ('clock',           'yellow', 'black'),
    ('title',           'white,bold', 'black'),
    ('div',             'dark gray',  'black'),
    ('normal',          'white', 'black'),

    # Soft coloring
    ('white_on_black',  'white',      'black'),
    ('yellow_on_black', 'yellow',     'black'),
    ('red_on_black',    'dark red',   'black'),
    ('green_on_black',  'dark green', 'black'),
    ('blue_on_black',   'light blue', 'black'),
    ('gray_on_black',   'light gray', 'black'),
    ('black_on_white',  'black',      'white'),
    ('magenta_on_black',  'light magenta',      'black'),

    ('dark_gray_on_black',   'dark gray', 'black'),
    ('red_on_blue',          'light red',   'dark blue'),
    ('yellow_on_blue',       'yellow',     'dark blue'),
    ('light_red_on_black',   'light red',   'black'),


    # Soft + bold
    ('b_white_on_black',  'white,bold',      'black'),
    ('b_yellow_on_black', 'yellow,bold',     'black'),
    ('b_red_on_black',    'dark red,bold',   'black'),
    ('b_green_on_black',  'dark green,bold', 'black'),
    ('b_blue_on_black',   'light blue,bold', 'black'),
    ('b_gray_on_black',   'light gray,bold', 'black'),
    ('b_black_on_white',  'black,bold',      'white'),

    # Soft + underline (NOTE: not widely supported)
    ('u_white_on_black',  'white,underline',      'black'),
    ('u_yellow_on_black', 'yellow,underline',     'black'),
    ('u_red_on_black',    'dark red,underline',   'black'),
    ('u_green_on_black',  'dark green,underline', 'black'),
    ('u_blue_on_black',   'light blue,underline', 'black'),
    ('u_gray_on_black',   'light gray,underline', 'black'),
    ('u_black_on_white',  'black,underline',      'white'),

    # Heavy coloring
    ('black_on_white',  'black',      'white'),
    ('black_on_yellow', 'black',      'yellow'),
    ('white_on_red',    'white',      'dark red'),
    ('black_on_green',  'black',      'dark green'),
    ('white_on_blue',   'white',      'dark blue'),
    ('white_on_gray',   'white',      'dark gray'),
    ('black_on_gray',   'black',      'light gray'),

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
date_widget = text('...', 'magenta_on_black')
time_widget = text('...', 'magenta_on_black')
title_widget = text(u'СИСТЕМА ЗА УПРАВЛЕНИЕ НА ПРОИЗВОДСТВОТО - КОМАНДИР.НЕТ', 'b_white_on_black')

terminal_widget = text(u'...', 'red_on_black')
operation_widget = text(u'...', 'yellow_on_black')
worker_widget = text(u'...', 'red_on_black')

top_line1 = urwid.Columns([
  ('weight', 12, date_widget),
  ('weight', 54, title_widget),
  ('weight', 10, time_widget)
])

# top_line2 = urwid.Columns([
#   ('weight', 14, terminal_widget),
#   ('weight', 36, operation_widget),
#   ('weight', 26, worker_widget)
# ], dividechars=1)

top_line2 = urwid.Columns([
  ('weight', 14, terminal_widget),
  ('weight', 36, operation_widget),
  ('weight', 26, worker_widget)
], dividechars=1)


##############################################################################
# MIDDLE                                                                        #
##############################################################################
col_style = 'gray_on_black'
col_head_style = 'b_gray_on_black'
col_sep_style = 'dark_gray_on_black'

mid_tablehead = urwid.Columns([
  ('weight', 2, text(u'No', col_head_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 8, text(u'ПОРЪЧКА', col_head_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 16, text(u'КЛИЕНТ', col_head_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 16, text(u'ИЗДЕЛИЕ', col_head_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 21, text(u'ОЗНАЧЕНИЕ', col_head_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 4, text(u'КОЛ.', col_head_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 5, text(u'ПАПКА', col_head_style)),
], dividechars=0)

mid_tablerow = urwid.Columns([
  ('weight', 2, text('...', col_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 8, text('...', col_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 16, text(u'...', col_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 16, text('...', col_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 21, text('...', col_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 4, text('...', col_style)),
  ('weight', 1, text(u'\N{BOX DRAWINGS LIGHT VERTICAL}', col_sep_style)),
  ('weight', 5, text('...', col_style)),
], dividechars=0)


# mid_tablerow = urwid.Columns([
#   ('weight', 2, text('', 'white_on_black')),
#   ('weight', 8, text('', 'gray_on_black')),
#   ('weight', 16, text('', 'white_on_black')),
#   ('weight', 16, text('', 'gray_on_black')),
#   ('weight', 21, text('', 'white_on_black')),
#   ('weight', 4, text('', 'gray_on_black')),
#   ('weight', 5, text('', 'white_on_black')),
# ], dividechars=1)

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


txt = '...'
# txt = '''Lorem ipsum dolor sit amet, no assum facilisi argumentum his, ius eu vocibus reprehendunt. Et nec vitae indoctum voluptatum, cu duo nihil impedit disputationi. Civibus postulant efficiendi ad nec. Sed labores maluisset elaboraret cu, nemore fierent mediocrem id quo. Id iuvaret feugiat expetenda ius, discere salutatus deterruisset qui at. Exerci inermis ius in, sumo veri referrentur ius an. Vis tantas recusabo et, eu vivendo pertinax has, ut sed idque everti.'''
msg_widget = urwid.Filler(urwid.Text(txt, align='center'), valign='middle', height='pack')


##############################################################################
# BOTTOM                                                                     #
##############################################################################
# Fields
# bot_field = urwid.Text(u'НЕВАЛИДЕН БАРКОД', align='center')
input_field = urwid.Text(u'', align='center')
# input_field = urwid.Edit(u'', align='center')
input_field = urwid.AttrMap(input_field, 'normal')

output_field = urwid.Text(u'', align='center')
output_field = urwid.AttrMap(output_field, 'normal')

##############################################################################
# ALL                                                                        #
##############################################################################

# pile = urwid.Pile([
#   ('pack', top_grid),
#   ('weight',12, urwid.LineBox(mid_pile)),
#   ('weight',12, urwid.LineBox(msg_widget)),
#   ('pack', bot_field)
# ])

div = urwid.Divider(u'\N{BOX DRAWINGS LIGHT HORIZONTAL}')
div = urwid.AttrMap(div, 'div')
blankdiv = urwid.Divider(u' ')
bpile = urwid.Pile([])
pile = urwid.AttrMap(bpile, 'body')
msg_container = urwid.Padding(msg_widget, left=1, right=1)

# pile.contents.append((urwid.Padding(div, left=20, right=20), ('pack', None)))
bpile.contents.append((blankdiv, ('pack', None)))
bpile.contents.append((top_line1, ('pack', None)))
bpile.contents.append((blankdiv, ('pack', None)))
bpile.contents.append((top_line2, ('pack', None)))
bpile.contents.append((div, ('pack', None)))
bpile.contents.append((mid_table, ('pack', None)))
bpile.contents.append((div, ('pack', None)))
bpile.contents.append((msg_container, ('weight', 1)))
bpile.contents.append((div, ('pack', None)))
# bpile.contents.append((input_field, ('pack', None)))

bot_input = urwid.Padding(input_field, left=1, right=1)
bot_output = urwid.Padding(output_field, left=1, right=1)

bot_row = urwid.Columns([
  (14, bot_input),
  ('weight', 64, bot_output)
])




# bot_field = urwid.AttrMap('normal', bot_field)
bpile.contents.append((bot_row, ('pack', None)))

bpile.set_focus(bot_row)

#
# Fake 80/25 display
#
outline = urwid.LineBox(pile, title=u'МЕХАНИЧЕН ДИЗАЙН И КОНСТРУКЦИИ ООД')
outline = urwid.AttrMap(outline, 'outline')

sichko = outline
emulator = urwid.Overlay(outline, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
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

global etag_output
global etag_input
etag_output = None
etag_input = None

def clear_output(loop, etag):
    global etag_output
    global etag_input

    # It is our input, safe to clear
    if etag_input is etag:
        input_field.base_widget.set_text('')
        input_field.set_attr_map({None: 'normal'})

    # It is our output, safe to clear
    if etag_output is etag:
        output_field.base_widget.set_text('')
        output_field.set_attr_map({None: 'normal'})


def normalize_message(message):
    res = ' '.join(message.split())   # squish
    if len(res) > 62:
      res = res[0:59] + '...'         # truncate

    return res

def build_message(result, data):
    if result == 'normal':      msg = 'ОК: %s' % str(data)
    elif result == 'invalid':   msg = 'НЕВАЛИДЕН БАРКОД'
    elif result == 'reserved':  msg = 'РЕЗЕРВИРАН БАРКОД'
    elif result == 'configure': msg = 'СПЕЦИАЛЕН БАРКОД'
    else:                       msg = 'ГРЕШКА: %s' % str(data)

    return msg

def set_attr_map(loop, (widget, mapping)):
    widget.set_attr_map(mapping)


def update_values(ident):
    target = None

    if ident == 'terminal':
        original_style = 'dark_gray_on_black'
        target = terminal_widget
        new_value = "ТЕРМИНАЛ:%s" % processor.tid
    elif ident == 'operation':
        original_style = 'yellow_on_black'
        target = operation_widget
        new_value = "ОПЕРАЦИЯ:%s %s" % (processor.oid, processor.operation)
    elif ident == 'worker':
        original_style = 'light_red_on_black'
        target = worker_widget
        new_value = "РАБОТНИК:%s %s" % (processor.wid, processor.worker)
    else:
        return

    target.base_widget.set_text(new_value)

    main_loop.set_alarm_in(0, set_attr_map, (target, {None: 'yellow_on_blue'}))
    main_loop.set_alarm_in(1, set_attr_map, (target, {None: original_style}))


def process_barcode(barcode):
    return processor.process(barcode)


def on_input(key):
    if key == 'enter':
        submit()
    elif key in '1234567890':
        valid_input(key)
    else:
        invalid_input(key)

def valid_input(key):
    global etag_input
    global etag_output
    current_text = input_field.base_widget.get_text()[0]

    # New operation
    if etag_output is etag_input:
        current_text = ''
        etag_input = time.time()

    if len(current_text) >= 12: return

    input_field.base_widget.set_text(current_text + key)
    input_field.set_attr_map({None: 'in_progress'})


def invalid_input(key):
    # Ignore any invalid input for now
    pass


def submit():
    global etag_input
    global etag_output
    global out_delay

    etag_output = etag_input

    current_text = input_field.base_widget.get_text()[0]
    input_field.set_attr_map({None: 'processing'})
    main_loop.draw_screen()
    (result, data) = process_barcode(current_text)

    message = build_message(result, data)

    if result == 'configure':
        update_values(data[0])

    output_field.base_widget.set_text(normalize_message(message))

    styles = PROCESSING_STYLES.get(result, PROCESSING_STYLES.get('other'))

    input_field.set_attr_map({None: styles[0]})
    output_field.set_attr_map({None: styles[1]})
    main_loop.set_alarm_in(out_delay, clear_output, etag_output)


def update_clock(loop, (period, date_widget, time_widget)):
    now = time.localtime()
    date_widget.base_widget.set_text(time.strftime('%d.%m.%Y', now))
    time_widget.base_widget.set_text(time.strftime('%H:%M:%S', now))

    loop.set_alarm_in(period, update_clock, (period, date_widget, time_widget))

def update_message(loop, (period, msg_widget, last_modified)):
    now_modified = os.stat(msg_file).st_mtime
    if now_modified > last_modified:
        with open(msg_file, 'rU') as f:
            text = f.read()

        msg_widget.base_widget.set_text(text)

    loop.set_alarm_in(period, update_message, (period, msg_widget, now_modified))

#
# INIT
#
main_loop = urwid.MainLoop(emulator, palette, unhandled_input=on_input)

main_loop.set_alarm_in(2, update_clock, (0.5, date_widget, time_widget))
main_loop.set_alarm_in(3, update_message, (msg_refresh, msg_widget, 0))

for i in ['terminal', 'operation', 'worker']:
    update_values(i)



main_loop.run()

