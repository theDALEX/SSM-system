from flask import Flask, render_template, request, redirect,url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#data visualisation and prediction
import pandas as pd
import matplotlib.pyplot as plt



# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
DATABASE_URL = 'sqlite:///maindatabase.db'
engine = create_engine(DATABASE_URL, echo=True)

# Create a Declarative Base instance
Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stockdata'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(15), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=func.current_date())

class SalesData(Base):
    __tablename__ = 'salesdata'
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(15), nullable=False)
    quantity = Column(Integer, nullable=False)
    date_of_sale = Column(DateTime, nullable=False, default=func.current_date())

#DATA PREDICTION
def get_data(product_name):
    sales = session.query(SalesData).filter_by(product=product_name).all()
    data = pd.DataFrame([(sale.date_of_sale, sale.quantity) for sale in sales], columns=['date_of_sale', 'quantity'])
    return data

def predict_demand(product_n):
    data = get_data(product_n)
    data['date_of_sale'] = pd.to_datetime(data['date_of_sale'])
    data = data.sort_values('date_of_sale')
    data['Moving_Avg'] = data['quantity'].rolling(window=3).mean()
    next_day_prediction = data['Moving_Avg'].iloc[-1]
    return next_day_prediction

# Create the database and tables
Base.metadata.create_all(engine)

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()


#MAIN APP CODE
@app.route('/')
def home():
    stockDate = session.query(StockData).all()
    print(stockDate)
    return render_template('inventory.html', stockDate=stockDate)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        product_name = request.form['Product_Name'].upper()
        no_of_products = request.form['No_ofProducts']

        # Check if the product already exists
        existing_product = session.query(StockData).filter_by(product=product_name).first()

        if existing_product:
        # If the product exists, update the quantity
            existing_product.quantity += int(no_of_products)
            session.commit()
        else:
            # If the product does not exist, insert a new record
            new_product = StockData(product=product_name, quantity=no_of_products)
            session.add(new_product)
            session.commit()

        return redirect(url_for('inventory'))
    return render_template('add.html')

@app.route('/inventory')
def inventory():
    stockDate = session.query(StockData).all()
    print(stockDate)
    return render_template('inventory.html', stockDate=stockDate)

@app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        product_name = request.form['Product_Name'].upper()
        no_of_products = request.form['No_ofProducts']

        date_of_sale = func.current_date()

        existing_product = session.query(StockData).filter_by(product=product_name).first()

        if existing_product:
        # If the product exists, update the quantity
            existing_product.quantity -= int(no_of_products)
            session.commit()

            # Insert the sale data into the salesdata table
            new_sale = SalesData(product=product_name, quantity=no_of_products, date_of_sale=date_of_sale)
            session.add(new_sale)
            session.commit()

            return redirect(url_for('inventory'))

    return render_template('sale.html')

@app.route('/salesdata', methods=['GET', 'POST'])
def salesdata():
    sales_data = []
    if request.method == 'POST':
        product_name = request.form['Product_Name'].upper()
        sales_data = session.query(SalesData).filter_by(product=product_name).all()

        #MATPLOTLIB DATA REPRESENTATION GRAPH
        dates = [sale.date_of_sale for sale in sales_data]
        quantity = [sale.quantity for sale in sales_data]

        plt.figure(figsize=(10,5))
        plt.plot(dates,quantity, marker='o')

        plt.title('Sales Over Time')
        plt.xlabel('Date')
        plt.ylabel('Quantity')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    return render_template('salesdata.html', sales_data=sales_data)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    product_name = None
    next_day_prediction = None
    
    if request.method == 'POST':
        product_name = request.form['Product_Name'].upper()
        next_day_prediction = predict_demand(product_name)

    return render_template('prediction.html', product_name=product_name, next_day_prediction=next_day_prediction)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
