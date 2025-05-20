import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartWidget(ctk.CTkFrame):
    def __init__(self, master, figure):
        super().__init__(master)
        self.figure = figure
        self.canvas = None
        self._draw_chart()

    def _draw_chart(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy() # Clear previous chart if any

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    def update_chart(self, new_figure):
        self.figure = new_figure
        self._draw_chart() 