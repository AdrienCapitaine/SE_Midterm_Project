import customtkinter as ctk
import tkinter as tk
from tkinter import Frame, Label
import tkintermapview

from map import *
from weather01 import *
from airports import *
from stations import *

# Set the appearance mode / color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

api_key = "436b1d6d-1167-4c86-9093-00fa35072e7f"


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

        self.input_frame = None
        self.map_frame = None
        self.result_frame = None

        #API var

        #Track
        self.cityFrom = None
        self.cityTo = None
        self.total_time = None
        self.total_distance_km = None
        self.total_distance_miles = None
        self.instructions = None

        #Weather
        self.destDescription = None
        self.dest_current_temp_C = None
        self.time_at_dest = None
        self.dest_icon_url = None

        self.fromDescription = None
        self.from_current_temp_C = None
        self.time_at_start = None
        self.from_icon_url = None

        #Airport
        self.airports = None

        #Gas Station
        self.stations = None

        self.setupui()


    def add_content_to_list(self):
        new_content = "New Content Added"
        self.content_list.append(new_content)
        tab2 = self.result_frame.scrollable_frame_track

        for item in self.content_list:
            label = ctk.CTkLabel(master=tab2, text=item)
            label.pack(padx=20, pady=20)

    def handle_error(self, error_message):
        # Create a new top-level window
        error_window = ctk.CTkToplevel()
        error_window.title("Error")

        # Create a label to display the error message
        error_label = ctk.CTkLabel(error_window, text=error_message, font=("Helvetica", 18), width= 300, height=150)
        error_label.pack(padx=10, pady=10)

        # Create a button to close the error window
        close_button = ctk.CTkButton(error_window, text="Close", command=error_window.destroy)
        close_button.pack(pady=10)

        error_window.grab_set()
        error_window.after(100, error_window.lift)
        error_window.geometry(CenterWindowToDisplay(self, 350, 250))

    def submit(self, tk_map):
        self.input_frame.requestButton.configure(text=self.input_frame.textLoading)
        self.input_frame.requestButton.update_idletasks()
        try:
            tk_map.clear()
            city1 = geocoding(self.input_frame.fromEntry.get(), api_key)
            if city1[0] != 200 or city1[1] == 'null' or city1[2] == 'null':
                self.error_message = "Information Error\n First city not found\n"
                self.handle_error(self.error_message)
                return
            #print(city1)
            self.cityFrom = city1
            city2 = geocoding(self.input_frame.toEntry.get(), api_key)
            if city2[0] != 200 or city2[1] == 'null' or city2[2] == 'null':
                self.error_message = "Information Error\n Second city not found\n"
                self.handle_error(self.error_message)
                return
            #print(city2)
            self.cityTo = city2
            self.total_time, (self.total_distance_km, self.total_distance_miles), self.instructions = tk_map.display(
                self.input_frame.transportBox.get(), city1[3],
                city2[3], city1[1],
                city1[2], city2[1],
                city2[2])
            #print(self.total_time, self.total_distance_km, self.total_distance_miles, self.instructions)
            #print(len(self.instructions))
            [self.destDescription, self.dest_current_temp_C, self.time_at_dest,self.dest_icon_url] = get_weather(city2[1],city2[2], key)
            print(self.cityTo[1])
            print(self.cityTo[2])
            print(self.input_frame.toEntry.get())
            [self.fromDescription, self.from_current_temp_C, self.time_at_start, self.from_icon_url] = get_weather(city1[1], city1[2], key)
            self.airports = get_airports(self.input_frame.toEntry.get(), (self.cityTo[1], self.cityTo[2]))
            self.stations = get_stations([(self.cityTo[1], self.cityTo[2])])
            print(self.airports)
            print(self.stations)
            self.result_frame.clear_tab()
            self.result_frame.display_details()
            self.result_frame.display_instructions()
            self.result_frame.display_weather()
            self.result_frame.display_airports()
            self.result_frame.display_stations()
        finally:
            self.input_frame.requestButton.configure(text=self.input_frame.textRequest)

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
        self.map_frame = MapFrame(self, self)

        self.result_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        self.map_frame.grid(row=0, column=1, rowspan=2, padx=15, pady=15, sticky="nsew")

class MapFrame(ctk.CTkFrame):

    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)
        self.app_instance = app_instance
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        self.mapLabel = ctk.CTkLabel(self, text="Map View", font=("Helvetica", 21))
        self.mapLabel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.map_widget = tkintermapview.TkinterMapView(self, corner_radius=12,
                                                        width=500,  # int(self.winfo_width() * 0.8),
                                                        height=500)  # int(self.winfo_height() * 0.8))
        self.map_widget.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.map = Map(self.map_widget, api_key)

        self.showButton = ctk.CTkButton(self, text="Show in Browser", font=("Helvetica", 18),
                                        command=self.map.save_and_display_browser, border_spacing=5)
        self.showButton.place(relx=0.85, rely=0.06, anchor=tk.CENTER)
        self.map.set_btn(self.showButton)


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
        self.tab5 = None

        self.scrollable_frame_details = None
        self.scrollable_frame_track = None
        self.scrollable_frame_weather = None
        self.scrollable_frame_airport = None
        self.scrollable_frame_station = None

        self.instruction_current_index = 0

        self.create_result_widget()


    def create_result_widget(self):
        scrollable_frame_width = 400
        scrollable_frame_height = 400
        self.tabview = ctk.CTkTabview(self,
                                 width=scrollable_frame_width,
                                 height=scrollable_frame_height)
        self.tabview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tab1 = self.tabview.add("Track Details")
        self.tab2 = self.tabview.add("Track Instructions")
        self.tab3 = self.tabview.add("Weather")
        self.tab4 = self.tabview.add("Airport")
        self.tab5 = self.tabview.add("Gas Station")

        # Set current tab
        self.tabview.set("Track Details")

        self.scrollable_frame_details = ctk.CTkScrollableFrame(master=self.tab1, width=scrollable_frame_width,
                                                             height=scrollable_frame_height)
        self.scrollable_frame_track = ctk.CTkScrollableFrame(master=self.tab2, width=scrollable_frame_width,
                                                             height=scrollable_frame_height)
        self.scrollable_frame_weather = ctk.CTkScrollableFrame(master=self.tab3, width=scrollable_frame_width,
                                                          height=scrollable_frame_height)
        self.scrollable_frame_airport = ctk.CTkScrollableFrame(master=self.tab4, width=scrollable_frame_width,
                                                          height=scrollable_frame_height)
        self.scrollable_frame_station = ctk.CTkScrollableFrame(master=self.tab5, width=scrollable_frame_width,
                                                          height=scrollable_frame_height)

        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_rowconfigure(0, weight=1)
        (self.scrollable_frame_details.grid(row=0, column=0, padx=10, pady=10, sticky="nsew"))

        self.tab2.grid_columnconfigure(0, weight=1)
        self.tab2.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_track.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tab3.grid_columnconfigure(0, weight=1)
        self.tab3.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_weather.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tab4.grid_columnconfigure(0, weight=1)
        self.tab4.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_airport.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tab5.grid_columnconfigure(0, weight=1)
        self.tab5.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_station.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set ip Scroll tab Details

        self.scrollable_frame_details.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_details.grid_columnconfigure(1, weight=1)
        self.scrollable_frame_details.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_details.grid_rowconfigure(1, weight=1)
        self.scrollable_frame_details.grid_rowconfigure(2, weight=1)
        self.scrollable_frame_details.grid_rowconfigure(2, weight=1)

        # Set up Scroll tab Instruction

        self.scrollable_frame_track.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_track.grid_columnconfigure(1, weight=1)

        self.scrollable_frame_track.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_track.grid_rowconfigure(1, weight=1)
        self.scrollable_frame_track.grid_rowconfigure(2, weight=2)
        self.scrollable_frame_track.grid_rowconfigure(3, weight=1)
        self.scrollable_frame_track.grid_rowconfigure(4, weight=1)
        self.scrollable_frame_track.grid_rowconfigure(5, weight=1)
        self.scrollable_frame_track.grid_rowconfigure(6, weight=1)

        # Set up for Weather Scroll

        self.scrollable_frame_weather.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_weather.grid_columnconfigure(1, weight=1)

        self.scrollable_frame_weather.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_weather.grid_rowconfigure(1, weight=1)
        self.scrollable_frame_weather.grid_rowconfigure(2, weight=2)
        self.scrollable_frame_weather.grid_rowconfigure(3, weight=1)
        self.scrollable_frame_weather.grid_rowconfigure(4, weight=1)
        self.scrollable_frame_weather.grid_rowconfigure(5, weight=1)

        self.prev_button = ctk.CTkButton(self.scrollable_frame_track, text="Previous", command=self.instruction_show_previous)
        self.prev_button.grid(row=0, column=0, padx=10, pady=10)

        self.next_button = ctk.CTkButton(self.scrollable_frame_track, text="Next", command=self.instruction_show_next)
        self.next_button.grid(row=0, column=1, padx=10, pady=10)

    def clear_instructions(self):
        for item in self.scrollable_frame_track.winfo_children():
            if isinstance(item, ctk.CTkLabel):
                item.destroy()
    def clear_tab(self):
        tab = {self.scrollable_frame_details,
                  self.scrollable_frame_track,
                  self.scrollable_frame_station,
                  self.scrollable_frame_airport,
                  self.scrollable_frame_weather}
        for elt in tab:
            for item in elt.winfo_children():
                if isinstance(item, ctk.CTkLabel):
                    item.destroy()

    def display_instructions(self):
        self.clear_instructions()
        for i in range(self.instruction_current_index, min(self.instruction_current_index + 6, len(self.app_instance.instructions))):
            instruction_label = ctk.CTkLabel(self.scrollable_frame_track, text=self.app_instance.instructions[i],
                                             font=("Helvetica", 15), wraplength=self.scrollable_frame_track.winfo_width(), corner_radius=8)
            instruction_label.grid(row=i+1, column=0, columnspan=2, padx=30, pady=10,sticky="nsew", ipady = 10)
            if i == self.instruction_current_index:
                instruction_label.configure(fg_color="gray28")

    def instruction_show_previous(self):
        if self.instruction_current_index > 0:
            self.instruction_current_index -= 1
            self.display_instructions()

    def instruction_show_next(self):
        if self.instruction_current_index < len(self.app_instance.instructions) - 1:
            self.instruction_current_index += 1
            self.display_instructions()

    def display_details(self):
        from_label = ctk.CTkLabel(self.scrollable_frame_details, text="From :", font=("Helvetica", 15),
                                         wraplength=400)
        from_label.grid(row=0, column=0, padx=10, pady=20)
        from_answer = ctk.CTkLabel(self.scrollable_frame_details, text=self.app_instance.cityFrom[3], font=("Helvetica", 15),
                                  wraplength=400)
        from_answer.grid(row=0, column=1, padx=10, pady=20)

        to_label = ctk.CTkLabel(self.scrollable_frame_details, text="Destination :", font=("Helvetica", 15),
                                  wraplength=400)
        to_label.grid(row=1, column=0, padx=10, pady=20)
        to_answer = ctk.CTkLabel(self.scrollable_frame_details, text=self.app_instance.cityTo[3], font=("Helvetica", 15),
                                   wraplength=400)
        to_answer.grid(row=1, column=1, padx=10, pady=20)

        time_label = ctk.CTkLabel(self.scrollable_frame_details, text="Travel Time :", font=("Helvetica", 15),
                                wraplength=400)
        time_label.grid(row=2, column=0, padx=10, pady=20)
        time_answer = ctk.CTkLabel(self.scrollable_frame_details, text=self.app_instance.total_time, font=("Helvetica", 15),
                                 wraplength=400)
        time_answer.grid(row=2, column=1, padx=10, pady=20)

        km_label = ctk.CTkLabel(self.scrollable_frame_details, text="Distance in Km :", font=("Helvetica", 15),
                                wraplength=400)
        km_label.grid(row=3, column=0, padx=10, pady=20)
        km_answer = ctk.CTkLabel(self.scrollable_frame_details, text=self.app_instance.total_distance_km, font=("Helvetica", 15),
                                 wraplength=400)
        km_answer.grid(row=3, column=1, padx=10, pady=20)

        miles_label = ctk.CTkLabel(self.scrollable_frame_details, text="Distance in Miles :", font=("Helvetica", 15),
                                wraplength=400)
        miles_label.grid(row=4, column=0, padx=10, pady=20)
        miles_answer = ctk.CTkLabel(self.scrollable_frame_details, text=self.app_instance.total_distance_miles, font=("Helvetica", 15),
                                 wraplength=400)
        miles_answer.grid(row=4, column=1, padx=10, pady=20)

    def display_weather(self):
        from_label = ctk.CTkLabel(self.scrollable_frame_weather, text=f"Weather from {self.app_instance.cityFrom[3]} :",
                                  font=("Helvetica", 15),
                                  wraplength=400)
        from_label.grid(row=0, column=0, padx=10, pady=20)
        from_answer = ctk.CTkLabel(self.scrollable_frame_weather, text=self.app_instance.fromDescription,
                                   font=("Helvetica", 15),
                                   wraplength=400)
        from_answer.grid(row=0, column=1, padx=10, pady=20)

        temp_from_label = ctk.CTkLabel(self.scrollable_frame_weather, text=f"Current Temperature in {self.app_instance.cityFrom[3]} :",
                                  font=("Helvetica", 15),
                                  wraplength=400)
        temp_from_label.grid(row=1, column=0, padx=10, pady=20)
        temp_from_answer = ctk.CTkLabel(self.scrollable_frame_weather, text=self.app_instance.from_current_temp_C,
                                   font=("Helvetica", 15),
                                   wraplength=400)
        temp_from_answer.grid(row=1, column=1, padx=10, pady=20)

        time_from_label = ctk.CTkLabel(self.scrollable_frame_weather,
                                  text=f"Current Time in {self.app_instance.cityFrom[3]} :",
                                  font=("Helvetica", 15),
                                  wraplength=400)
        time_from_label.grid(row=2, column=0, padx=10, pady=20)
        time_from_answer = ctk.CTkLabel(self.scrollable_frame_weather, text=self.app_instance.time_at_start,
                                   font=("Helvetica", 15),
                                   wraplength=400)
        time_from_answer.grid(row=2, column=1, padx=10, pady=20)

        to_label = ctk.CTkLabel(self.scrollable_frame_weather, text=f"Weather from {self.app_instance.cityTo[3]} :",
                                  font=("Helvetica", 15),
                                  wraplength=400)
        to_label.grid(row=3, column=0, padx=10, pady=20)
        to_answer = ctk.CTkLabel(self.scrollable_frame_weather, text=self.app_instance.destDescription,
                                   font=("Helvetica", 15),
                                   wraplength=400)
        to_answer.grid(row=3, column=1, padx=10, pady=20)

        temp_to_label = ctk.CTkLabel(self.scrollable_frame_weather,
                                       text=f"Current Temperature in {self.app_instance.cityTo[3]} :",
                                       font=("Helvetica", 15),
                                       wraplength=400)
        temp_to_label.grid(row=4, column=0, padx=10, pady=20)
        temp_to_answer = ctk.CTkLabel(self.scrollable_frame_weather, text=self.app_instance.dest_current_temp_C,
                                        font=("Helvetica", 15),
                                        wraplength=400)
        temp_to_answer.grid(row=4, column=1, padx=10, pady=20)

        time_to_label = ctk.CTkLabel(self.scrollable_frame_weather,
                                       text=f"Current Time in {self.app_instance.cityTo[3]} :",
                                       font=("Helvetica", 15),
                                       wraplength=400)
        time_to_label.grid(row=5, column=0, padx=10, pady=20)
        time_to_answer = ctk.CTkLabel(self.scrollable_frame_weather, text=self.app_instance.time_at_dest,
                                        font=("Helvetica", 15),
                                        wraplength=400)
        time_to_answer.grid(row=5, column=1, padx=10, pady=20)


    def display_airports(self):
        self

    def display_stations(self):
        self

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

        self.transportBox = ctk.CTkComboBox(self, state="readonly", values=["Car", "Bike", "Foot"])
        self.transportBox.grid(row=3, column=1, padx=20, pady=10)
        self.transportBox.set("Car")

        self.textRequest = "Submit Request"
        self.textLoading = "Loading ..."
        self.requestButton = ctk.CTkButton(self, text="Submit Request", font=("Helvetica", 18), width=170,
                                           height=40,
                                           command=lambda: self.app_instance.submit(self.app_instance.map_frame.map))
        self.requestButton.grid(row=4, column=0, columnspan=2, padx=20, pady=20)



if __name__ == "__main__":
    app = App()
    # Set the window size and center it on the main screen
    app.geometry(CenterWindowToDisplay(app, 1600, 800))
    app.mainloop()
