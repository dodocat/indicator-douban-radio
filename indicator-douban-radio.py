import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify
import gobject
gobject.threads_init()
import os
import webbrowser
import subprocess
import json

from radio import Radio

def add2menu(menu, text=None, icon=None, conector_event=None, conector_action=None):
    if text != None:
        menu_item = Gtk.ImageMenuItem.new_with_label(text)
        if icon:
            image = Gtk.Image.new_from_file(icon)
            menu_item.set_image(image)
            menu_item.set_always_show_image(True)
    else:
        if icon == None:
            menu_item = Gtk.SeparatorMenuItem()
        else:
            menu_item= Gtk.ImageMenuItem.new()
            img = Gtk.Image.new_from_file(icon)
            menu_item.set_always_show_image(True)
    if conector_event != None and conector_action != None:
        menu_item.connect(conector_event, conector_action)
    menu_item.show()
    menu.append(menu_item)
    return menu_item

def add_chl(menu, event, action, chl):
    menu_item = Gtk.ImageMenuItem.new_with_label(chl['name'])
    if event != None and action != None:
        menu_item.connect(event, action, chl)
    menu_item.show()
    menu.append(menu_item)
    return menu_item

class IndicatorDoubanRadio():
    def __init__(self):
        self.about_dialog = None
        self.icon = os.path.abspath('./tabletop_radio_.png')
        self.active_icon = None
        self.attention_icon = None
        self.radio = Radio()
        self.notification = Notify.Notification.new('', '', None)
        self.indicator = appindicator.Indicator.new("DoubanRadio-Indicator",
                self.icon, appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_attention_icon(self.icon)
        self.menu = self.get_menu()
        self.indicator.set_menu(self.menu)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    
    def get_menu(self):
        """ Create and populate the menu """
        menu = Gtk.Menu()
        self.img_item = add2menu(menu, icon=os.path.abspath("./tabletop_radio_.png"))
        self.song_info = add2menu(menu, text="song_name")
        self.next_song = add2menu(menu, text="next", conector_event='activate',
                conector_action=self.play_next)
        menu.show()
        return menu

    def play_next(self, nouse):
        self.radio.next()
    
    def main(self):
        self.radio.next()
        chls = self.radio.get_channels()
        self.show_chls(chls)
        self.exit_item = add2menu(self.menu, text="quit", 
                conector_event='activate', conector_action=self._on_quit_clicked)
        Gtk.main()
        exit(0)

    def show_chls(self,chls):
        chls = json.loads(chls)
        groups = chls['groups']
        for group in groups:
            group_item = add2menu(self.menu, group['group_name'])
            if group['group_id'] is 0:
                for chl in group['chls']:
                     add_chl(self.menu, 'activate', self._on_switch_channel, chl)
                add2menu(self.menu)
            else:
                #group_item = Gtk.ImageMenuItem.new_with_label(group['group_name'])
                subchl = Gtk.Menu()
                for chl in group['chls']:
                    add_chl(subchl, 'activate', self._on_switch_channel, chl)
                subchl.show()
                group_item.set_submenu(subchl)
                #group_item.show()
                #self.menu.append(group_item)

    def _on_switch_channel(self, nouse, chl):
        self.radio.channel = chl['id']
        self.radio.skip()

    def _on_quit_clicked(self, widget):
        exit(0)

if __name__ == "__main__":
    IndicatorDoubanRadio().main()
 
