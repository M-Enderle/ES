import TKinterModernThemes as TKMT

from es.modules import invoice, receipt, analytics
from es.utils.tkinter_utils import add_image_to_frame
from es.utils.utils import get_project_root


class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Enderle Solutions", mode="dark")

        self.Label("Rechnungssoftware").grid(row=1, column=0, pady=(30, 0))

        img = add_image_to_frame(self, f"{get_project_root()}/assets/images/logo.png", 0.3)
        img.grid(row=0, column=0, pady=(50, 0))
        

        self.notebook = self.Notebook("Notebook Test")
        self.inv_tab = self.notebook.addTab("Rechnungen")
        self.corrections_tab = self.notebook.addTab("Korrekturen")
        self.analytics_tab = self.notebook.addTab("Analysen")

        self.close_button = self.Button(
            "Schließen",
            command=self.root.destroy,
            widgetkwargs={
                "width": 40,
            },
            pady=20
        )

        self.add_buttons()
        
    def add_buttons(self):

        self.inv_tab.Button(
            "Ausgangsrechnung schreiben",
            command=lambda: print("Ausgangsrechnung schreiben"),
            widgetkwargs={
                "width": 40,
            },
            pady=(20, 13)
        )

        self.inv_tab.Button(
            "Eingangsrechnung schreiben",
            command=lambda: print("Eingangsrechnung schreiben"),
            widgetkwargs={
                "width": 40,
            },
            pady=(13, 30)
        )

        self.analytics_tab.Button(
            "Analyse starten",
            command=lambda: analytics.open_streamlit(),
            widgetkwargs={
                "width": 40,
            },
            pady=(20, 13)
        )

        