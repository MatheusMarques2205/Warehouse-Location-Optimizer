# 🏭 Warehouse Location Optimizer

## About
This project implements a solution for the classic Facility Location Problem, specifically focused on finding the optimal warehouse location considering a network of suppliers and customers.

## 🚀 Features
- Warehouse location optimization based on:
  - Distances between suppliers and customers
  - Cargo volumes
  - Transportation costs
- Interactive visualization using Folium maps
- Optimization progress tracking
- Complete cost analysis

## 📊 Required Data
The system requires three CSV files:
- `suppliers.csv`: Supplier data (ID, latitude, longitude)
- `customers.csv`: Customer data (ID, latitude, longitude)
- `shipments.csv`: Shipment data (origin, destination, volume)

## 🛠️ Technologies Used
- Python 3.x
- Pandas: Data manipulation
- NumPy: Numerical computing
- SciPy: Mathematical optimization
- Geopy: Geographic distance calculations
- Folium: Interactive map visualization

## ⚙️ How to Use
1. Clone the repository
2. Install dependencies:
3. Prepare your CSV files with the required data
4. Run the script:

## 📈 Results
The program generates:
- Optimal warehouse coordinates
- Minimized total cost
- Interactive map showing:
  - Supplier locations (red)
  - Customer locations (blue)
  - Optimal warehouse location (green star)
  - Optimization history

## 📝 License
This project is under the MIT license.
