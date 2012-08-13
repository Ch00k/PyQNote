import gtk


class PyQNote(object):
    def __init__(self):
        self.staticon = gtk.StatusIcon()
        self.staticon.set_from_stock(gtk.STOCK_INDEX)
        self.staticon.set_visible(True)
        self.staticon.connect('activate', self.browser)
        gtk.main()

    def browser(self, window):
        browser = gtk.Window()
        browser.set_usize(600, 500)
        textbox = gtk.TextView()
        browser.add(textbox)
        browser.show_all()


if __name__ == '__main__':
    PyQNote()
