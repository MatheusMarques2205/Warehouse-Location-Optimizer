import pandas as pd
import numpy as np
from geopy.distance import distance
from scipy.optimize import minimize
import folium
import webbrowser
import os

# =============================================
# 1. AUXILIARY FUNCTIONS
# =============================================

def load_and_prepare_data():
    """
    Loads and prepares data from CSV files.
    
    Returns:
        tuple: Contains DataFrames for inbound shipments, outbound shipments,
              suppliers, and customers data
    """
    suppliers = pd.read_csv("suppliers.csv")
    customers = pd.read_csv("customers.csv")
    shipments = pd.read_csv("shipments.csv")
    
    inbound = shipments[shipments["Destination"] == "Warehouse"].copy()
    outbound = shipments[shipments["Origin"] == "Warehouse"].copy()
    
    inbound = pd.merge(inbound, suppliers, left_on="Origin", right_on="Supplier_ID", how="left")
    outbound = pd.merge(outbound, customers, left_on="Destination", right_on="Customer_ID", how="left")
    
    return inbound, outbound, suppliers, customers

def calculate_total_cost(warehouse_coords, inbound, outbound, distance_cost=0.5, volume_cost=10):
    """
    Calculates the total cost given warehouse coordinates.
    
    Args:
        warehouse_coords (tuple): Latitude and longitude of the warehouse
        inbound (DataFrame): Inbound shipments data
        outbound (DataFrame): Outbound shipments data
        distance_cost (float): Cost per kilometer of distance
        volume_cost (float): Cost per cubic meter of volume
    
    Returns:
        float: Total cost for all shipments
    """
    warehouse_lat, warehouse_lon = warehouse_coords
    
    inbound["Distance_km"] = inbound.apply(
        lambda row: distance((row["Latitude"], row["Longitude"]), (warehouse_lat, warehouse_lon)).km,
        axis=1
    )
    inbound["Cost"] = (inbound["Distance_km"] * distance_cost) + (inbound["Volume_m³"] * volume_cost)
    
    outbound["Distance_km"] = outbound.apply(
        lambda row: distance((warehouse_lat, warehouse_lon), (row["Latitude"], row["Longitude"])).km,
        axis=1
    )
    outbound["Cost"] = (outbound["Distance_km"] * distance_cost) + (outbound["Volume_m³"] * volume_cost)
    
    return inbound["Cost"].sum() + outbound["Cost"].sum()

def create_interactive_map(optimal_coords, suppliers, customers, cost_history):
    """
    Creates an interactive Folium map showing suppliers, customers, and optimal warehouse location.
    
    Args:
        optimal_coords (tuple): Optimal warehouse coordinates (lat, lon)
        suppliers (DataFrame): Suppliers data
        customers (DataFrame): Customers data
        cost_history (list): List of cost values during optimization
    """
    # Create base map centered on optimal location
    m = folium.Map(location=optimal_coords, zoom_start=6)
    
    # Add suppliers (red markers)
    for _, row in suppliers.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"Supplier {row['Supplier_ID']}",
            icon=folium.Icon(color="red", icon="truck", prefix="fa")
        ).add_to(m)
    
    # Add customers (blue markers)
    for _, row in customers.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"Customer {row['Customer_ID']}",
            icon=folium.Icon(color="blue", icon="user", prefix="fa")
        ).add_to(m)
    
    # Add optimal warehouse (green star)
    folium.Marker(
        location=optimal_coords,
        popup=f"Optimal Warehouse<br>Lat: {optimal_coords[0]:.4f}<br>Lon: {optimal_coords[1]:.4f}",
        icon=folium.Icon(color="green", icon="star", prefix="fa")
    ).add_to(m)
    
    # Add cost history as a feature group
    cost_group = folium.FeatureGroup(name="Optimization Progress")
    for i, cost in enumerate(cost_history):
        cost_group.add_child(
            folium.CircleMarker(
                location=[optimal_coords[0] + 0.1, optimal_coords[1] + 0.1 + i*0.01],
                radius=5,
                color="#3186cc",
                fill=True,
                fill_color="#3186cc",
                popup=f"Iteration {i+1}: ${cost:,.2f}"
            )
        )
    m.add_child(cost_group)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save and open map
    map_path = "optimal_warehouse_map.html"
    m.save(map_path)
    webbrowser.open(f"file://{os.path.abspath(map_path)}")

# =============================================
# 2. OPTIMIZATION WITH COST HISTORY
# =============================================

def optimize_with_history(inbound, outbound, suppliers, customers):
    """
    Optimizes warehouse location and stores cost history.
    
    Args:
        inbound (DataFrame): Inbound shipments data
        outbound (DataFrame): Outbound shipments data
        suppliers (DataFrame): Suppliers data
        customers (DataFrame): Customers data
    
    Returns:
        tuple: Contains optimal coordinates, minimum cost, and cost history
    """
    cost_history = []
    
    def callback(xk):
        cost_history.append(calculate_total_cost(xk, inbound, outbound))
    
    # Initial guess (geographic center)
    initial_guess = [
        (suppliers["Latitude"].mean() + customers["Latitude"].mean()) / 2,
        (suppliers["Longitude"].mean() + customers["Longitude"].mean()) / 2
    ]
    
    # Optimization
    result = minimize(
        fun=lambda coords: calculate_total_cost(coords, inbound, outbound),
        x0=initial_guess,
        method="L-BFGS-B",
        bounds=[(suppliers["Latitude"].min(), suppliers["Latitude"].max()),
               (suppliers["Longitude"].min(), suppliers["Longitude"].max())],
        callback=callback
    )
    
    return result.x, result.fun, cost_history

# =============================================
# 3. Main Function
# =============================================

def main():
    """Executes the complete workflow and generates visualizations."""
    print("Loading data...")
    inbound, outbound, suppliers, customers = load_and_prepare_data()
    
    print("Optimizing location...")
    optimal_coords, optimal_cost, cost_history = optimize_with_history(inbound, outbound, suppliers, customers)
    
    print("\n=== RESULTS ===")
    print(f"Best location: Latitude = {optimal_coords[0]:.6f}, Longitude = {optimal_coords[1]:.6f}")
    print(f"Minimum total cost: ${optimal_cost:,.2f}")
    
    # Create interactive map
    print("\nGenerating interactive map...")
    create_interactive_map(optimal_coords, suppliers, customers, cost_history)

if __name__ == "__main__":
    main()