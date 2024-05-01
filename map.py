from geo import * #import all the functions that make call to the geolocation API
import webbrowser
import folium
import customtkinter as ctk
import tkintermapview

# Class for the map
class Map:

    def __init__(self, map_view: tkintermapview.TkinterMapView, api_key:str):
        """
            The constructor

            Parameters:
                map_view: the tkinter widget for map view
                api_key: api key

        """
        self.coordinates = []
        self.start_lat = None
        self.start_lon = None
        self.end_lat = None
        self.end_lon = None
        self.map_view = map_view
        self.allow_view = False
        self.city1_name = None
        self.city2_name = None
        self.btn_view = None
        self.api_key = api_key

    def set_btn(self, btn: ctk.CTkButton):
        """
            set the view boutton in browser

            Parameters:
                btn: the tkinter button widget
        """
        self.btn_view = btn
        self.btn_view["state"] = "disable"

    def save_and_display_browser(self):
        """
            display the map in the browser
        """
        if self.allow_view:
            webbrowser.open("map.html")

    def set_coordinate(self, coordinates: list[list[float, float]], start_lat:float, start_lon:float, end_lat:float, end_lon:float):
        """
            set the variable : coordinates, start_lat, start_lon, end_lat, end_lon

            Parameters:
                coordinates : list of coordinates for the route
                start_lat, start_long : coordinate of starting point
                end_lat, end_long : coordinate of arrival point
        """
        self.coordinates = coordinates
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon

    def clear(self):
        """
            Clear the map view widget
        """
        self.map_view.delete_all_path()
        self.map_view.delete_all_marker()

    def display_on_map(self):
        """
            Set the markers and the route one the map view widget
        """
        self.map_view.set_marker(self.start_lat, self.start_lon, text="Start")
        self.map_view.set_marker(self.end_lat, self.end_lon, text="End", marker_color_circle="green", marker_color_outside="green3")

        self.map_view.set_position(self.start_lat, self.start_lon)

        self.map_view.set_zoom(10)

        self.map_view.set_path(self.coordinates, color="blue", width=2)

    def save_map(self):
        """
            Create the HTML file with marker in order to display it in the browser later if necessary
        """
        m = folium.Map(location=[self.start_lat, self.start_lon], zoom_start=13)
        folium.PolyLine(self.coordinates, color="blue", weight=float(2.5), opacity=1).add_to(m)

        start_marker = folium.Marker(
            location=[self.start_lat, self.start_lon],
            icon=folium.Icon(icon='cross', color='red'),
            popup=folium.Popup('Start Point', max_width=250)
        )
        end_marker = folium.Marker(
            location=[self.end_lat, self.end_lon],
            icon=folium.Icon(icon='cross', color='green'),
            popup=folium.Popup('End Point', max_width=250)
        )

        start_marker.add_to(m)
        end_marker.add_to(m)
        folium.map.Marker(
            [self.start_lat, self.start_lon],
            icon=folium.DivIcon(
                icon_size=(250, 36),
                icon_anchor=(11, 30),
                html='<div><div style="pointer-events:none;font-size: 8pt;position:relative;z-index:1000!important; color:white"; font-weight:bold>Start</div></div>',
            )
        ).add_to(m)

        folium.map.Marker(
            [self.end_lat, self.end_lon],
            icon=folium.DivIcon(
                icon_size=(250, 36),
                icon_anchor=(8, 30),
                html='<div><div style="pointer-events:none;font-size: 8pt;position:relative;z-index:1000!important; color:white"; font-weight:bold>End</div></div>',
            )
        ).add_to(m)

        bounds = [[self.start_lat, self.start_lon], [self.end_lat, self.end_lon]]

        margin_x = (abs(bounds[0][0] - bounds[1][0])) / 50
        margin_y = (abs(bounds[0][1] - bounds[1][1])) / 50

        adjusted_bounds = [
            [bounds[0][0] - margin_x, bounds[0][1] - margin_y],
            [bounds[1][0] + margin_x, bounds[1][1] + margin_y]
        ]

        m.fit_bounds(adjusted_bounds)

        m.save("map.html")


    def display(self, vehicle: str, city1_name:str, city2_name:str, start_lat:float, start_lon:float, end_lat:float, end_lon:float):
        """
            The main function for the map that compute the route, time, distance and instructions from coordinates and vehicule

            Parameters:
                vehicule : the mean of transport [car, bike, foot]
                city1_name, city2_name : city name
                start_lat, start_long : coordinate of starting point
                end_lat, end_long : coordinate of arrival point

            Return:
                time, distance and instructions

        """
        self.city1_name = city1_name
        self.city2_name = city2_name

        coordinate, total_time, total_distance, instructions = get_info(self.api_key, vehicle, start_lat, start_lon, end_lat, end_lon)
        self.set_coordinate(coordinate, start_lat, start_lon, end_lat, end_lon)
        if coordinate is None:
            #messagebox.showerror("Map error", "Road not found beetween :\n\n\'" + self.city1_name + "\'\n\n\tand\n\n\'" + self.city2_name + "\'.")

            self.map_view.set_marker(self.start_lat, self.start_lon, text="Start")
            self.map_view.set_marker(self.end_lat, self.end_lon, text="End", marker_color_circle="green", marker_color_outside="green3")


            self.map_view.set_position(self.start_lat, self.start_lon)

            self.map_view.set_zoom(10)
            self.allow_view = False
            if self.btn_view is not None:
                self.btn_view['state'] = 'disable'
            return None, (None, None), None
        self.display_on_map()
        self.save_map()
        if self.btn_view is not None:
            self.btn_view["state"] = "active"
        self.allow_view = True
        return total_time, total_distance, instructions