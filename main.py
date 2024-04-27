import customtkinter as ctk
import tkinter as tk
from tkinter import Frame, Label
import tkintermapview

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Centers the window in middle of the screen of the user
def CenterWindowToDisplay(Screen: ctk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


# App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content_list = []

        self.setupui()

    def add_content_to_list(self):
        new_content = "New Content Added"
        self.content_list.append(new_content)
        tab1 = self.result_frame.scrollable_frame_track

        for item in self.content_list:
            label = ctk.CTkLabel(master=tab1, text=item)
            label.pack(padx=20, pady=20)

    def clear_tab(self):
        for item in self.result_frame.scrollable_frame_track.winfo_children():
            if isinstance(item, ctk.CTkLabel):
                item.destroy()



    def setupui(self):
        self.title("Project Application")
        self.geometry("1600x800")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=6)
        self.grid_columnconfigure(0, weight=30)
        self.grid_columnconfigure(1, weight=60)

        # Split the app in 3 parts
        self.input_frame = Input(self, self)
        self.result_frame = Result(self, self)
        self.map_frame = Map(self, self)

        self.result_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        self.map_frame.grid(row=0, column=1, rowspan=2, padx=15, pady=15, sticky="nsew")



class Map(ctk.CTkFrame):

    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)
        self.app_instance = app_instance
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        self.mapLabel = ctk.CTkLabel(self, text="Map View", font=("Helvetica", 21))
        self.mapLabel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.after(100, self.create_map_widget())

    def create_map_widget(self):
        map_widget = tkintermapview.TkinterMapView(self, corner_radius=12,
                                                   width=500,#int(self.winfo_width() * 0.8),
                                                   height=500)#int(self.winfo_height() * 0.8))
        map_widget.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")


class Result(ctk.CTkFrame):

    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)
        self.app_instance = app_instance
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=8)

        self.resultLabel = ctk.CTkLabel(self, text="Result", font=("Helvetica", 21))
        self.resultLabel.grid(row=0, column=0, padx=10, pady=20)

        self.tabview = None

        self.tab1 = None
        self.tab2 = None
        self.tab3 = None
        self.tab4 = None

        self.scrollable_frame_track = None
        self.scrollable_frame_weather = None
        self.scrollable_frame_airport = None
        self.scrollable_frame_station = None

        self.create_result_widget()


    def create_result_widget(self):
        scrollable_frame_width = 400#int(self.winfo_width() * 0.6)  # Set a specific width
        scrollable_frame_height = 400#int(self.winfo_height() * 0.8)  # Set a specific height
        self.tabview = ctk.CTkTabview(self,
                                 width=scrollable_frame_width,
                                 height=scrollable_frame_height)
        self.tabview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tab1 = self.tabview.add("Track Details")
        self.tab2 = self.tabview.add("Weather")
        self.tab3 = self.tabview.add("Airport")
        self.tab4 = self.tabview.add("Gas Station")

        # Set current tab
        self.tabview.set("Track Details")

        self.scrollable_frame_track = ctk.CTkScrollableFrame(master=self.tab1, width=scrollable_frame_width,
                                                             height=scrollable_frame_height)
        self.scrollable_frame_weather = ctk.CTkScrollableFrame(master=self.tab2, width=scrollable_frame_width,
                                                          height=scrollable_frame_height)
        self.scrollable_frame_airport = ctk.CTkScrollableFrame(master=self.tab3, width=scrollable_frame_width,
                                                          height=scrollable_frame_height)
        self.scrollable_frame_station = ctk.CTkScrollableFrame(master=self.tab4, width=scrollable_frame_width,
                                                          height=scrollable_frame_height)
        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_track.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")



class Input(ctk.CTkFrame):

    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)
        self.app_instance = app_instance
        # Configure the input grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.infoLabel = ctk.CTkLabel(self, text="Information", font=("Helvetica", 21))
        self.infoLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        self.fromLabel = ctk.CTkLabel(self, text="Departure Location", font=("Helvetica", 15))
        self.fromLabel.grid(row=1, column=0, padx=20, pady=10)

        self.fromEntry = ctk.CTkEntry(self, placeholder_text="Enter Location")
        self.fromEntry.grid(row=1, column=1, padx=20, pady=10)

        self.toLabel = ctk.CTkLabel(self, text="Destination", font=("Helvetica", 15))
        self.toLabel.grid(row=2, column=0, padx=20, pady=10)

        self.toEntry = ctk.CTkEntry(self, placeholder_text="Enter Destination")
        self.toEntry.grid(row=2, column=1, padx=20, pady=10)

        self.transportLabel = ctk.CTkLabel(self, text="Preferred Mode of Transportation",
                                           font=("Helvetica", 15))
        self.transportLabel.grid(row=3, column=0, padx=20, pady=10)

        self.transportBox = ctk.CTkComboBox(self, state="readonly", values=["Car", "Bike", "Walking"])
        self.transportBox.grid(row=3, column=1, padx=20, pady=10)

        self.requestButton = ctk.CTkButton(self, text="Submit Request", font=("Helvetica", 18), width=170,
                                           height=40)
        self.requestButton.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

        self.requestButton.configure(command=self.app_instance.add_content_to_list)



if __name__ == "__main__":
    app = App()
    # Set the window size and center it on the main screen
    app.geometry(CenterWindowToDisplay(app, 1600, 800))
    app.mainloop()
