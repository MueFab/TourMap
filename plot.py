import os
import gpxpy
import folium
import itertools

def plot_gpx_tracks(map_obj: folium.Map, directory: str, feature_group: folium.FeatureGroup) -> None:
    """Load and plot each GPX file's track from the specified directory into a specific feature group."""
    colors = ['blue', 'green', 'red', 'purple']
    color_cycle = itertools.cycle(colors)
    for file in sorted(os.listdir(directory)):
        if file.endswith('.gpx'):
            try:
                with open(os.path.join(directory, file), 'r') as gpx_file:
                    gpx = gpxpy.parse(gpx_file)
                track_color = next(color_cycle)
                for track in gpx.tracks:
                    for segment in track.segments:
                        points = [(point.latitude, point.longitude) for point in segment.points]
                        folium.PolyLine(points, color=track_color, weight=2.5, opacity=1).add_to(feature_group)
            except Exception as e:
                print(f"Error processing file {file}: {e}")

def add_tile_layers(map_obj: folium.Map) -> None:
    """Add various tile layers to the map."""
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(map_obj)
    folium.TileLayer('Stamen Terrain', name='Stamen Terrain').add_to(map_obj)
    folium.TileLayer('Stamen Toner', name='Stamen Toner').add_to(map_obj)
    folium.TileLayer('Stamen Watercolor', name='Stamen Watercolor').add_to(map_obj)
    folium.TileLayer('CartoDB Positron', name='CartoDB Positron').add_to(map_obj)
    folium.TileLayer('CartoDB Dark_Matter', name='CartoDB Dark Matter').add_to(map_obj)

def main() -> None:
    """Main function to generate the map with GPX tracks and tile layers."""
    tours_dir = "./tours"
    planned_tours_dir = "./planned_tours"
    initial_location = [51.0, 10.0]  # Central location for the map
    zoom_start = 12

    map_osm = folium.Map(location=initial_location, zoom_start=zoom_start)
    add_tile_layers(map_osm)

    # Plot finished tours
    tours_group = folium.FeatureGroup(name='Finished Tours', show=True)
    plot_gpx_tracks(map_osm, tours_dir, tours_group)
    map_osm.add_child(tours_group)

    # Plot planned tours
    planned_tours_group = folium.FeatureGroup(name='Planned Tours', show=True)
    plot_gpx_tracks(map_osm, planned_tours_dir, planned_tours_group)
    map_osm.add_child(planned_tours_group)

    folium.LayerControl().add_to(map_osm)

    map_osm.save("map.html")
    print("Map saved successfully as map.html")

if __name__ == "__main__":
    main()
