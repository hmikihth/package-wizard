#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import os
import signal
import string
import sys
import gtk
#import commands

from common import *
import common; _ = common._
from Package import *
from PackageView import *
from ProgressIndicator import *
from StoreRow import *

class Application:
    """This class represents the application itself."""

    # Initialization methods
    
    def Init(self):
        """Initialize the application."""
        os.nice(20)
        self.InitWindow()
        signal.signal(signal.SIGINT, self.InterruptHandler)
        gtk.main()
    
    def InterruptHandler(self, signal_num, frame):
        """SIGINT handler."""
        if self.active_progress:
            self.SendCloseMessage()
        gtk.main_quit()
    
    def InitWindow(self):
        """Initialize the application window."""
        
        main_window_signals = {
            'on_main_window_map_event': self.OnMainWindowShow,
            'on_main_window_destroy': gtk.main_quit,
            'on_install_button_clicked': self.OnInstallButtonClicked,
            'on_remove_button_clicked': self.OnRemoveButtonClicked,
            'on_upgrade_button_clicked': self.OnUpgradeButtonClicked,
            'on_source_editor_button_clicked': self.OnSourceEditorButtonClicked,
            'on_quit_button_clicked': gtk.main_quit,
            'on_info_checkbutton_toggled': self.OnInfoCheckButtonToggled,
            'on_filter_checkbutton_toggled': self.OnRebuildView,
            'on_listmode_combobox_changed': self.OnRebuildView,
            'on_search_button_clicked': self.OnSearch,
            'on_search_entry_activate': self.OnSearch,
            'on_search_clear_button_clicked': self.OnSearchClearButtonClicked
        }

        info_window_signals = {
            'on_package_info_window_delete_event': self.OnInfoWindowDeleteEvent,
            'on_detailed_info_checkbutton_clicked':self.OnInfoWindowClicked
        }

        glade_xml_main_window = gtk.glade.XML(GLADE_FILENAME, 'main_window')
        self.main_window_mapped = False
        self.install_button = glade_xml_main_window.get_widget('install_button')
        self.remove_button = glade_xml_main_window.get_widget('remove_button')
        self.remove_button_label = glade_xml_main_window.get_widget('remove_button_label')
        self.upgrade_button = glade_xml_main_window.get_widget('upgrade_button')
        self.upgrade_button_label = glade_xml_main_window.get_widget('upgrade_button_label')
        self.source_editor_button = glade_xml_main_window.get_widget('source_editor_button')
        self.quit_button = glade_xml_main_window.get_widget('quit_button')
        self.info_checkbutton = glade_xml_main_window.get_widget('info_checkbutton')
        self.all_info_checkbutton = glade_xml_main_window.get_widget('all_info_checkbutton')
        self.show_upgradable_checkbutton = glade_xml_main_window.get_widget('show_upgradable_checkbutton')
        self.limited_bandwidth_checkbutton = glade_xml_main_window.get_widget('limited_bandwidth_checkbutton')
        self.apps_checkbutton = glade_xml_main_window.get_widget('apps_checkbutton')
        self.libs_checkbutton = glade_xml_main_window.get_widget('libs_checkbutton')
        self.installed_checkbutton = glade_xml_main_window.get_widget('installed_checkbutton')
        self.install_button_label = glade_xml_main_window.get_widget('install_button_label')
        self.noninstalled_checkbutton = glade_xml_main_window.get_widget('noninstalled_checkbutton')
        self.listmode_combobox = glade_xml_main_window.get_widget('listmode_combobox')
        self.listmode_combobox.set_active(0)
        self.search_combobox = glade_xml_main_window.get_widget('search_combobox')
        self.search_combobox.set_active(0)
        self.search_entry = glade_xml_main_window.get_widget('search_entry')    
        self.search_button = glade_xml_main_window.get_widget('search_button')  
        self.search_clear_button = glade_xml_main_window.get_widget('search_clear_button')  
        self.vbox = glade_xml_main_window.get_widget('vbox')
        glade_xml_main_window.signal_autoconnect(main_window_signals)
        
        glade_xml_info_window = gtk.glade.XML(GLADE_FILENAME, 'package_info_window')
        self.package_info_window = glade_xml_info_window.get_widget('package_info_window')
        self.detailed_info_checkbutton = glade_xml_info_window.get_widget('detailed_info_checkbutton')
        self.textview = glade_xml_info_window.get_widget('textview')
        self.textbuffer = self.textview.get_buffer()
        self.fg_red_tag = self.textbuffer.create_tag('fg_red', foreground='red')
        glade_xml_info_window.signal_autoconnect(info_window_signals)
        
        self.sensitive_widgets = [self.install_button, self.remove_button,
            self.upgrade_button, self.source_editor_button, self.quit_button,
            self.info_checkbutton, self.all_info_checkbutton,
            self.show_upgradable_checkbutton,
            self.limited_bandwidth_checkbutton, self.apps_checkbutton,
            self.libs_checkbutton, self.installed_checkbutton,
            self.noninstalled_checkbutton, self.listmode_combobox,
            self.search_combobox, self.search_entry, self.search_button,
            self.search_clear_button, self.detailed_info_checkbutton]
        
        self.view = PackageView()
        self.view_widget = None
        self.progress_indicator = ProgressIndicator()
        self.active_progress = False

    # Signal handlers

    def OnMainWindowShow(self, event, param):
        if not self.main_window_mapped:
            self.RebuildView(full_rebuild=True)
        self.main_window_mapped = True

    def OnInstallButtonClicked(self, widget):
        packages = self.view.GetSelectedPackages()
        if len(packages) != 0:
          package_names = [package.longname for package in packages if not package.is_installed]
          command = 'gurpmi2 ' + string.join(package_names)
          debug(DEBUG_FORKS, command)
          args = ['gurpmi2'] + package_names
          os.spawnvp(os.P_WAIT, 'gurpmi2', args)
          self.RebuildView(full_rebuild=True)

    def OnRemoveButtonClicked(self, widget):
        packages = self.view.GetSelectedPackages()
        if len(packages) != 0:
          package_names = [package.longname for package in packages if package.is_installed]
          command = 'echo n | urpme --test ' + string.join(package_names)
          (infile, outfile) = os.popen4(command)
          lines = outfile.readlines()
          text = unescape(string.join(lines, ''))
          remove = self.ShowRemoveDialog(text)
        
          if remove:
            command = 'urpme --auto ' + string.join(package_names) 
            self.ShowRemoveProgressWindow(command)
            args = ['urpme', '--auto'] + package_names #kivaras beiktatasa
            os.spawnvp(os.P_WAIT, 'urpme', args) #kivaras vege
            self.RebuildView(full_rebuild=True)

    def OnUpgradeButtonClicked(self, widget):
        packages = self.view.GetSelectedPackages()
        if len(packages) != 0:
          package_names = [package.shortname for package in packages if package.is_upgradable]
          self.ShowUpgradeWindow(1)
    
    def OnSourceEditorButtonClicked(self, widget):
        URPM_EDITOR = 'edit-repos'
        os.spawnlp(os.P_WAIT, URPM_EDITOR, URPM_EDITOR) # var a gombra
#        os.spawnlp(os.P_NOWAIT, URPM_EDITOR, URPM_EDITOR) # nem var a gombra
        self.RebuildView(full_rebuild=True) #ujraolvasas

    def OnInfoWindowDeleteEvent(self, window, event):
        window.hide_all()
        self.info_checkbutton.set_active(False)
        return True
    
    def OnInfoCheckButtonToggled(self, checkbutton):
        visible = checkbutton.get_active()
        window = self.package_info_window
        if visible:
            self.RefreshInfoWindow()
            window.show_all()
        else:
            window.hide_all()
    
    def OnRebuildView(self, widget):
        self.RebuildView()

    def OnSearch(self, widget):
        search_mode = self.search_combobox.get_active()
        text = self.search_entry.get_text()
        self.RebuildView(search_mode, text)

    def OnSearchClearButtonClicked(self, widget):
        active = self.search_combobox.get_active()
        self.search_entry.set_text('')
        self.RebuildView(active)
    
    def OnInfoWindowClicked(self, window):
        self.RefreshInfoWindow()
    
    # Public methods

    def RebuildView(self, search_mode=-1, search_string='', full_rebuild=False):
        """Rebuild the view."""
        phases_num = len(singletons.package_pool.GetActiveSources(new=True)) + 2
        if full_rebuild:
            phases_num += 4
        self.IndicateProgress(True, phases_num)
        
        if full_rebuild:
            singletons.package_pool.Init()
        
        apps_toggled = self.apps_checkbutton.get_active()
        libs_toggled = self.libs_checkbutton.get_active()
        installed_toggled = self.installed_checkbutton.get_active()
        noninstalled_toggled = self.noninstalled_checkbutton.get_active()

        self.DisplayProgress(_('Filtering packages'))
        singletons.package_pool.Filter(apps_toggled, libs_toggled, installed_toggled, noninstalled_toggled, search_mode, search_string)

        self.DisplayProgress(_('Rebuilding view'))
        active = self.listmode_combobox.get_active()
        self.view.Populate(active)
        
        self.IndicateProgress(False)
        self.RefreshButtons()
        self.RefreshInfoWindow()
    
    def IndicateProgress(self, bool, phases=0):
        """Turn on or of progress indication according to bool.
            phases is only relevant if bool is True and in this case it
            defines the total number of phases of the progress bar."""
        self.active_progress = bool
        self.phases = phases
        self.counter = 0.0
        for widget in self.sensitive_widgets:
                widget.set_sensitive(not bool)
        
        if bool:
            singletons.application.ReplaceView \
                (singletons.application.progress_indicator)
            
            pipe1_fd_in, pipe1_fd_out = os.pipe()
            pipe2_fd_in, pipe2_fd_out = os.pipe()
            self.pipe_file_out = os.fdopen(pipe1_fd_out, 'w')
            self.pipe_file_in = os.fdopen(pipe2_fd_in, 'r')
            
            child = not os.fork()
            if child:
                os.dup2(pipe1_fd_in, 0)
                os.dup2(pipe2_fd_out, 1)
                os.execlp('./rpmanager.py', './rpmanager.py', 'child')
            else:
                self.pipe_file_in.readline()  # wait for the child to show up
        
        else:
            singletons.application.ReplaceView(singletons.application.view.sw)
            self.SendCloseMessage()
    
    def DisplayProgress(self, message):
        """Display the sent message in the progress indicator and advance the
            counter."""
        progress = self.counter/self.phases
        self.pipe_file_out.write(str(progress) + ' ' + message + '\n')
        self.pipe_file_out.flush()
        self.counter += 1

    def RefreshButtons(self):
        """Refresh the operation buttons."""
        (installable, removable, upgradable) = self.view.GetButtonCounts()
        buttons = [
            (self.install_button_label, installable, _('Install')),
            (self.remove_button_label, removable, _('Remove')),
            (self.upgrade_button_label, upgradable, _('Upgrade'))
        ]
        
        for button in buttons:
            widget = button[0]
            count = button[1]
            text = button[2] + ' (' + str(count) + ')'
            widget.set_label(text)
            widget.set_sensitive(count)

    def RefreshInfoWindow(self):
        """Refresh the info window."""
        self.textbuffer.set_text('')
        
        if self.view.IsEmpty():
            text = _('There are currently no packages in the view.')
            self.textbuffer.set_text(text)
        else:
            detailed_button_active = self.detailed_info_checkbutton.get_active()
            info = self.view.GetCurrentRowInfo(detailed_button_active);
            for row_info in info:
                start_iter = self.textbuffer.get_end_iter()
                name = row_info[0]
                value = ': ' + row_info[1] + '\n'
                self.textbuffer.insert_with_tags \
                    (start_iter, name, self.fg_red_tag)
                self.textbuffer.insert_at_cursor(conv(value))

    # Helper methods

    def SendCloseMessage(self):
        """Send close message to the progress indicator process."""
        self.SendMessage('1 quit\n')
    
    def SendMessage(self, message):
        """Send the message to the progress indicator process."""
        self.pipe_file_out.write(message)
        self.pipe_file_out.flush()
    
    def ReplaceView(self, widget):
        """Replace the package view area with widget."""
        if self.view_widget:
            self.vbox.remove(self.view_widget)
        
        self.view_widget = widget
        self.vbox.pack_start(widget)
        self.vbox.show_all()
        
        while gtk.events_pending():
            gtk.main_iteration(True)

    def ShowRemoveDialog(self, text):
        """Show the remove dialog."""
        text = string.replace(text, '\\"', '"')
        
        info_label = gtk.Label(conv(text))
        info_label.set_line_wrap(True)
        info_label.set_use_markup(True)
        
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add_with_viewport(info_label)
        
        question = _('Remove package(s)?')
        dialog = gtk.Dialog(question,
            buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        
        warning_label = gtk.Label()
        warning_label.set_markup('<span foreground="red" size="x-large">' + question + '</span>')
        
        dialog.vbox.pack_start(warning_label, False)
        dialog.vbox.pack_start(sw)
        dialog.vbox.show_all()
        
        dialog.set_default_size(400, 300)
        response = dialog.run()
        dialog.destroy()
        
        if response == gtk.RESPONSE_OK:
            return 1
        else:
            return 0
    
    def ShowRemoveProgressWindow(self, command):
        """Show the remove progress window."""
        def timeout_callback():
            progressbar.pulse()
            status = os.waitpid(pid, os.WNOHANG)[1]
            exited = os.WIFEXITED(status)
            if exited:
                window.destroy()
            return not exited
        
        message = _('Removing package(s)...')
        
        label = gtk.Label(message)
        progressbar = gtk.ProgressBar()
        
        vbox = gtk.VBox()
        vbox.pack_start(label)
        vbox.pack_start(progressbar)
        
        window = gtk.Window()
        window.set_title(message)
        window.set_border_width(10)
        window.set_default_size(200, 50)
        window.add(vbox)
        window.show_all()
        
        args = string.split(command)
        pid = os.spawnvp(os.P_NOWAIT, 'urpme', args)
        gtk.timeout_add(100, timeout_callback)
    
    def ShowUpgradeWindow(self, shortnames):

        def on_cancel_button_clicked(widget):
            window.destroy()
        
        def on_ok_button_clicked(widget):
            args = ['gurpmi2'] + upgradable_longnames
            os.spawnvp(os.P_WAIT, 'gurpmi2', args)
            window.destroy()
            self.RebuildView(full_rebuild=True)

        upgrade_window_signals = {
                                    'on_cancel_button_clicked': on_cancel_button_clicked,
                                    'on_ok_button_clicked': on_ok_button_clicked
                                 }
        STORE_NAME = 0
        store = gtk.TreeStore(gobject.TYPE_STRING)
        glade_window = gtk.glade.XML(GLADE_FILENAME, 'upgrade_window')
        glade_window.signal_autoconnect(upgrade_window_signals)
        window = glade_window.get_widget('upgrade_window')
        treeview = glade_window.get_widget('package_treeview')
        treeview.set_model(store)
        col = gtk.TreeViewColumn(_('Name'), gtk.CellRendererText(), text=STORE_NAME)
        treeview.append_column(col)
        selected_packages = singletons.application.view.GetSelectedPackages()
        self.upgradable_shortnames = [package.shortname for package in selected_packages if package.is_upgradable]
        self.upgradable_longnames = []
        i = 0
        for key in singletons.package_pool.upgradable_packages:
            if key in self.upgradable_shortnames:
                self.upgradable_longnames.append(singletons.package_pool.upgradable_packages_long[i])
                store.append(None, [key])
            i += 1
        treeview.expand_all()
