 #!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import gtk
import pango
from common import *
import common; _ = common._

class ProgressIndicator(gtk.Alignment):
    """This class represents the progress indicator widget."""
    
    def __init__(self):
        gtk.Alignment.__init__(self, 0.5, 0.5)
#---add show image
#        self.label = gtk.Label(_('Processing')+'...')
        pixbufanim = gtk.gdk.PixbufAnimation("gui/install.gif")
        image = gtk.Image()
        image.set_from_animation(pixbufanim)
        image.show()

#        attr = pango.AttrSize(14000, 0, 15)
#        attrlist = pango.AttrList()
#        attrlist.insert(attr)
#        self.label.set_attributes(attrlist)
#        self.add(self.label)
        self.add(image)
#-- image show over
#    def SetLabel(self, text):
#        """Set the label."""
#        self.label.set_label(text + '...')
#        
    def Start(self):
        """Start pulsing the bar."""
        application.ReplaceView(application.progress_indicator)
        self.timer = gtk.timeout_add(10, self.Progress, self)

    def Progress(self, param):
        """Pulse the bar or finish pulsing it."""
        global thread_finished

        if thread_finished:
            application.ReplaceView(application.view.sw)
        else:
            self.bar.pulse()

        return not thread_finished
