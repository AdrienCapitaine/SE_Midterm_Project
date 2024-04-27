import tkinter as tk
import tkintermapview

from map import *


def submit(tk_map):
    tk_map.clear()
    city1 = geocoding(e1.get(), api_key)
    if city1[0] != 200 or city1[1] == 'null' or city1[2] == 'null':
        messagebox.showerror("Map error", "First city not found : \'"+city1[3]+"\'")
        return
    print(city1)
    city2 = geocoding(e2.get(), api_key)
    if city2[0] != 200 or city2[1] == 'null' or city2[2] == 'null':
        messagebox.showerror("Map error", "Second city not found : \'"+city2[3]+"\'")
        return
    print(city2)
    total_time, (total_distance_km, total_distance_miles), instructions = tk_map.display(e3.get(), city1[3], city2[3], city1[1], city1[2], city2[1], city2[2])
    print(total_time, total_distance_km, total_distance_miles, instructions)


# Your GraphHopper API key
api_key = "436b1d6d-1167-4c86-9093-00fa35072e7f"

# Create a Tkinter window
root = tk.Tk()

# Initialize the TkinterMapView widget
tk_map_view = tkintermapview.TkinterMapView(root, width=600, height=400)

tk_map_view.pack(fill="both", expand=True)

tk_map = Map(tk_map_view, api_key)

frame = tk.Frame(root)

l1 = tk.Label(frame, text='From').grid(row=0)
l2 = tk.Label(frame, text='To').grid(row=1)
l3 = tk.Label(frame, text='Vehicule').grid(row=2)
e1 = tk.Entry(frame)
e2 = tk.Entry(frame)
e3 = tk.Entry(frame)
b = tk.Button(frame, text="Submit", command=lambda :submit(tk_map)).grid(row=3, columnspan=2)
b2 = tk.Button(frame, text="View", command=tk_map.save_and_display_browser)
b2.grid(row=4, columnspan=2)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

tk_map.set_btn(b2)

frame.pack()

root.mainloop()

