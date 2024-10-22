Project Title:
Simple Stock Management System (SSM System)

Video Demo:
<>

Overview:
The SSM System is a web application designed to assist small shop owners with managing their inventory effectively. This user-friendly system is intended to simplify stock management, allowing shop owners to make informed decisions based on accurate sales data and predictions.

Features:
Inventory:
Purpose: Display all products, their quantities, and the date they were received.

Files Involved: The inventory management functionality is implemented in the inventory.html template and the corresponding Flask route in app.py.

Details: Shop owners can quickly see the current stock levels and track when each product was added to the inventory. This helps in identifying old stock that may need to be sold off quickly.

Add Stock:
Purpose: Add new products to the inventory.

Files Involved: The add.html template and the Flask route in app.py.

Details: Shop owners enter new products along with their quantities to keep the stock levels updated. This feature ensures that the inventory is always accurate and up-to-date.

Current Stocks:
Purpose: View the current stock levels.

Files Involved: The inventory.html template and the corresponding Flask route in app.py.

Details: Displays the number of items available for each product in the inventory. This helps shop owners to quickly check stock levels and make informed decisions about reordering products.

Checkout:
Purpose: Record product sales.

Files Involved: The sale.html template and the Flask route in app.py.

Details: Shop owners can enter the product name and quantity sold, which is then saved in a separate sales database. This ensures that sales data is accurately recorded and can be analyzed later.

Sales Data:
Importance: One of the most crucial features of the SSM System.

Purpose: Analyze sales trends to make informed decisions about stock levels.

Files Involved: The salesdata.html template, app.py for handling requests, and uses matplotlib to generating sales graphs.

Functionality: Shop owners enter a product name (e.g., BOOK) and click the "See Data" button. A graphical user interface (GUI) then displays the sales data for that product.

Details: This feature allows shop owners to identify trends, such as peak sales periods and slow days. They can use this information to plan restocks and promotions accordingly.

Sale Prediction:
Importance: Another critical feature for shop owners.

Purpose: Predict future sales to manage stock levels efficiently.

Files Involved: The prediction.html template and prediction logic in app.py.

Functionality: Shop owners enter a product name and click the "Predict" button. The system uses the Simple Moving Average (SMA) technique to forecast the number"# SSM-system" 
