# -*- coding: utf-8 -*-
#
# Abstract class for screen widgets
class ScreenWidget:

    title = ""
    desc = ""
    help = ""
    icon = None

    def shown(self):
        pass

    def execute(self):
        return True

    def backCheck(self):
        return False
