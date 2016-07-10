#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import gobject
import gtk
import gtk.glade
import select
import sys
import os
import signal
from common import *

class Child:
    def __init__(self):
        signals = {
            'on_child_window_map_event': self.OnMap,
            'on_child_window_delete_event': self.OnDelete
        }
        glade_window = gtk.glade.XML(GLADE_FILENAME, 'child_window')
        glade_window.signal_autoconnect(signals)

        self.label = glade_window.get_widget('child_label')
        self.progressbar = glade_window.get_widget('child_progressbar')
        self.hbox = glade_window.get_widget('child_hbox')
        self.window = glade_window.get_widget('child_window')

        animation = gtk.gdk.PixbufAnimation('gui/search.gif')
        image = gtk.Image()
        image.set_from_animation(animation)
        self.hbox.pack_end(image)
        self.window.show_all()

        self.poll = select.poll()
        self.poll.register(0, select.POLLIN)
        gobject.timeout_add(10, self.OnTimeOut)
        signal.signal(signal.SIGINT, self.InterruptHandler)
        gtk.main()

    def InterruptHandler(self, signal_num, frame):
        gtk.main_quit()

    def OnDelete(self, widget, event):
        return True
        
    def OnMap(self, widget, event):
        print 'ready\n'
        sys.stdout.flush()
    
    def OnTimeOut(self):
      try:
        text = self.ReadMessage()

        if text == 'quit\n':
            gtk.main_quit()
        elif text != False:
            self.ProcessMessage(text)
        return True
      except KeyboardIterrupt(e):
        gtk.main_quit()
        
    def ReadMessage(self):
        poll = self.poll.poll(0)
        if len(poll) == 0:
            return False

        if poll[0][1] == select.POLLIN:
            return os.read(0, 65535)
        else:
            return False

    def ProcessMessage(self, message):
        message = message.split('\n')[-2]
        fraction_str = message.split()[0]
        text = message[len(fraction_str)+1:]
        fraction = float(fraction_str)

        if fraction == 1 and text == 'quit':
            gtk.main_quit()

        self.progressbar.set_fraction(fraction)
        self.label.set_text(text)
