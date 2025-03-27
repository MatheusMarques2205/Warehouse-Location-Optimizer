import pandas as pd
import numpy as np

# =============================================
# GENERATE DATA FOR EUROPE (WIDER COORDINATES)
# =============================================

# Geographical boundaries of Europe
EUROPE_BOUNDS = {
    'min_lat': 35.0,   # south
    'max_lat': 70.0,    # north
    'min_lon': -10.0,   # west
    'max_lon': 40.0     # east 
}

# Gerar 100 Suppliers
suppliers = pd.DataFrame({
    "Supplier_ID": [f"Supplier_ID{i}" for i in range(1, 101)],
    "Latitude": np.round(np.random.uniform(EUROPE_BOUNDS['min_lat'], EUROPE_BOUNDS['max_lat'], 100)), 
    "Longitude": np.round(np.random.uniform(EUROPE_BOUNDS['min_lon'], EUROPE_BOUNDS['max_lon'], 100))
})

# Gerar 100 Customers
customers = pd.DataFrame({
    "Customer_ID": [f"Customer_ID{i}" for i in range(1, 101)],
    "Latitude": np.round(np.random.uniform(EUROPE_BOUNDS['min_lat'], EUROPE_BOUNDS['max_lat'], 100)),
    "Longitude": np.round(np.random.uniform(EUROPE_BOUNDS['min_lon'], EUROPE_BOUNDS['max_lon'], 100))
})

# Generate 500 shipments (250 inbound, 250 outbound)
inbound = pd.DataFrame({
    "Shipment_ID": [f"Inbound_{i}" for i in range(1, 251)],
    "Origin": np.random.choice(suppliers["Supplier_ID"], 250),
    "Destination": "Warehouse",
    "Volume_m³": np.round(np.random.uniform(10, 100, 250)) 
})

outbound = pd.DataFrame({
    "Shipment_ID": [f"Outbound_{i}" for i in range(1, 251)],
    "Origin": "Warehouse",
    "Destination": np.random.choice(customers["Customer_ID"], 250),
    "Volume_m³": np.round(np.random.uniform(10, 100, 250))
})

shipments = pd.concat([inbound, outbound])

# Save CSV (no index)
suppliers.to_csv("suppliers.csv", index=False)
customers.to_csv("customers.csv", index=False)
shipments.to_csv("shipments.csv", index=False)

print("Arquivos gerados com sucesso!")
print(f"Suppliers: {len(suppliers)} | Customers: {len(customers)} | Shipments: {len(shipments)}")