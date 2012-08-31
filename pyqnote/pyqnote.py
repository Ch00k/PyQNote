import gtk
import keybinder
from dropbox_actor import DropboxActor
from config import Config


class PyQNote(object):
    def __init__(self):
        # Status icon
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_stock(gtk.STOCK_INDEX)
        self.status_icon.set_visible(True)
        self.status_icon.connect('activate', self.show_main_window)
        self.status_icon.connect('popup-menu', self.show_status_menu)

        # Main window
        self.main_window = gtk.Window()
        self.main_window.set_usize(300, 100)
        self.main_window.set_title('PyQNote')
        self.main_window.connect('delete-event', self.close_main_window)

        # Text box
        self.text_buffer = gtk.TextBuffer()
        self.textbox = gtk.TextView(self.text_buffer)

        # Save button
        self.submit_button = gtk.Button('Save')
        self.submit_button.connect('clicked', self.save_note)

        # VBox
        parent_vbox = gtk.VBox(False, 5)
        parent_vbox.pack_start(self.textbox, True, True)
        parent_vbox.pack_start(self.submit_button, False, False)
        self.main_window.add(parent_vbox)

        # Save hotkey
        accelgroup = gtk.AccelGroup()
        self.main_window.add_accel_group(accelgroup)
        self.submit_button.add_accelerator('activate',
                                           accelgroup,
                                           gtk.keysyms.Return,
                                           0,
                                           gtk.ACCEL_VISIBLE)

        # Global hotkey
        hotkey = '<Alt>B'
        keybinder.bind(hotkey, self.hotkey_callback)

    def show_status_menu(self, icon, button, time):
        menu = gtk.Menu()

        settings = gtk.MenuItem('Settings')
        about = gtk.MenuItem('About')
        quit = gtk.MenuItem('Quit')

        settings.connect('activate', Settings)
        about.connect('activate', self.show_about_dialog)
        quit.connect('activate', gtk.main_quit)

        menu.append(settings)
        menu.append(about)
        menu.append(quit)

        menu.show_all()

        menu.popup(None,
                   None,
                   gtk.status_icon_position_menu,
                   button,
                   time,
                   self.status_icon)

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name('PyQNote')
        about_dialog.set_version('0.0.1')
        about_dialog.set_authors(['Andriy Yurchuk'])

        about_dialog.run()
        about_dialog.destroy()

    def show_main_window(self, window):
        if self.main_window.props.is_active:
            self.close_main_window(self.main_window, None)
        else:
            self.main_window.show_all()
            self.main_window.present()

    def close_main_window(self, window, data):
        self.main_window.hide_all()
        return True

    def save_note(self, widget):
        start_iter = self.text_buffer.get_start_iter()
        end_iter = self.text_buffer.get_end_iter()

        print self.text_buffer.get_line_count()
        text = self.text_buffer.get_text(start_iter, end_iter)

        lines = text.split('\n')

        for line in lines:
            # TODO: change this when saving to dropbox is implemented
            print line, '\n\n'

        self.text_buffer.delete(start_iter, end_iter)
        self.close_main_window(self.main_window, None)

    def hotkey_callback(self):
        self.show_main_window(self.main_window)
        self.main_window.present()


class Settings(object):
    def __init__(self, window):
        config_dict = Config().read_config()
        dropbox_enabled = config_dict['dropbox']['use'] == 'True'
        try:
            dropbox_path = config_dict['dropbox']['path']
        except KeyError:
            dropbox_path = ''

        # Settings window
        settings_window = gtk.Window()
        settings_window.set_usize(600, 300)
        settings_window.set_title('Settings')

        # Use Dropbox checkbox
        self.use_dropbox_checkbox = gtk.CheckButton('Use Dropbox')
        self.use_dropbox_checkbox.set_active(dropbox_enabled)

        # Dropbox path entry
        self.dropbox_dir_location = gtk.Entry()
        self.dropbox_dir_location.set_text(dropbox_path)
        self.dropbox_dir_location.set_sensitive(dropbox_enabled)

        # Get Dropbox directory button
        self.get_dropbox_dir_button = gtk.Button('Get Dropbox directory')
        self.get_dropbox_dir_button.connect('clicked', self.get_dropbox_path)
        self.get_dropbox_dir_button.set_sensitive(dropbox_enabled)

        # Checkbox state event
        self.use_dropbox_checkbox.connect('toggled',
                                     self.toggle_editable,
                                     self.dropbox_dir_location,
                                     self.get_dropbox_dir_button)

        # Save button
        save_button = gtk.Button('Save')
        save_button.connect('clicked', lambda w: self.save_config())

        # Cancel button
        cancel_button = gtk.Button('Cancel')
        cancel_button.connect('clicked', lambda w: settings_window.destroy())

        # VBox
        parent_vbox = gtk.VBox(False, 5)
        parent_vbox.pack_start(self.use_dropbox_checkbox)
        parent_vbox.pack_start(self.dropbox_dir_location)
        parent_vbox.pack_start(self.get_dropbox_dir_button)
        parent_vbox.pack_start(save_button)
        parent_vbox.pack_start(cancel_button)
        settings_window.add(parent_vbox)

        settings_window.show_all()

    def toggle_editable(self, checkbox, entry, button):
        self.dropbox_dir_location.set_sensitive(checkbox.get_active())
        self.get_dropbox_dir_button.set_sensitive(checkbox.get_active())

    def save_config(self):
        kwargs = dict()
        kwargs['use_dropbox'] = self.use_dropbox_checkbox.get_active()
        kwargs['dropbox_path'] = self.dropbox_dir_location.get_text()
        config = Config()
        config.write_config(**kwargs)

    def get_dropbox_path(self, window):
        self.dropbox_dir_location.set_text(DropboxActor.get_path())

def main():
    PyQNote()
    gtk.main()

if __name__ == '__main__':
    main()