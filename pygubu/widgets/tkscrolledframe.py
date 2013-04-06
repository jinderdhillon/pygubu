import types
import tkinter as tk

from ..builderobject import *


def _autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed.
    Code from Joe English (JE) at http://wiki.tcl.tk/950"""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)



class TkScrolledFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super(TkScrolledFrame, self).__init__(master, **kw)

        self._canvas = canvas = tk.Canvas(self, bd=0, highlightthickness=0,
            width=200, height=200)
        self.innerframe = innerframe = tk.Frame(self._canvas)
        self.vsb = vsb = tk.Scrollbar(self)
        self.hsb = hsb = tk.Scrollbar(self, orient="horizontal")

        #configure scroll
        self._canvas.configure(
            yscrollcommand=lambda f, l: _autoscroll(vsb, f, l))
        self._canvas.configure(
            xscrollcommand=lambda f, l: _autoscroll(hsb, f, l))
        self.vsb.config(command=canvas.yview)
        self.hsb.config(command=canvas.xview)

        #grid
        self._canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.vsb.grid(row=0, column=1, sticky=tk.NS)
        self.hsb.grid(row=1, column=0, sticky=tk.EW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # create a window inside the canvas which will be scrolled with it
        self._innerframe_id = innerframe_id = canvas.create_window(0, 0,
            window=innerframe, anchor=tk.NW)

        innerframe.bind('<Configure>', self._on_iframe_configure)
        canvas.bind('<Configure>', self._on_canvas_configure)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar

    def _on_iframe_configure(self, event=None):
        new_region = (self.innerframe.winfo_reqwidth(),
            self.innerframe.winfo_reqheight())
        curr_region = tuple(
            map(int, (self._canvas.cget('scrollregion')).split()[2:]))
        if new_region != curr_region:
            newscroll = (0, 0) + new_region
            self._canvas.config(scrollregion=newscroll)

    def _on_canvas_configure(self, event=None):
        innerframe = self.innerframe
        canvas = self._canvas
        innerframe_id = self._innerframe_id
        size = (innerframe.winfo_reqwidth(), innerframe.winfo_reqheight())

        if innerframe.winfo_reqwidth() < canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            canvas.itemconfigure(innerframe_id, width=canvas.winfo_width())
        if innerframe.winfo_reqheight() < canvas.winfo_height():
            canvas.itemconfigure(
                innerframe_id, height= canvas.winfo_height())

        itemsize = (int(canvas.itemcget(innerframe_id, 'width')),
                int(canvas.itemcget(innerframe_id, 'height')))
        if itemsize[0] < size[0] or itemsize[1] < size[1]:
            canvas.itemconfigure( innerframe_id,
                    width= size[0], height= size[1])

    def reposition(self):
        """This method should be called when children are added,
        removed, grid_remove, and grided in the scrolled frame."""
        self.innerframe.update()
        self.after_idle(self._on_iframe_configure, None)
        self.after_idle(self._on_canvas_configure, None)


class TKScrolledFrameBO(BuilderObject):
    class_ = TkScrolledFrame
    container = True
    maxchildren = 1
    allowed_children = ('tk.Frame', 'ttk.Frame' )
    properties = ['background', 'borderwidth', 'cursor', 'height',
        'highlightbackground', 'highlightcolor', 'highlightthickness',
        'padx', 'pady', 'relief', 'takefocus', 'width']
    ro_properties = ro_properties = ('class_',)

    def get_child_master(self):
        return self.widget.innerframe

register_widget('pygubu.widgets.tkscrolledframe', TKScrolledFrameBO,
    'ScrolledFrame', ('Pygubu Utilities', 'tk'))
