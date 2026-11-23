
# StyleHub – Clothing Store Web Application

## 1. Project Description

StyleHub is a web-based clothing store management system developed using Python, Flask, MySQL, HTML, CSS, and JavaScript.

The application provides functionality for managing clothing products, categories, brands, sizes, colors, clients, orders, discounts, and stock quantities.

It also includes advanced product search, real-time stock tracking, JWT-based authentication, role-based access control, and sales reports.

The main purpose of StyleHub is to simplify clothing store operations by providing an organized system for managing products, customers, orders, and inventory.

## 2. Technologies Used

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- JWT Authentication

### Frontend
- HTML5
- CSS3
- JavaScript

### Tools
- Visual Studio Code
- MySQL Workbench
- Postman
- Git and GitHub

## 3. Main Features

### 3.1 Product Management
- Add, view, update, and delete products.
- Manage product names, descriptions, and prices.
- Assign categories, brands, genders, sizes, and colors.
- Manage product stock quantities.
- Prevent deletion of products with existing order history.

### 3.2 Discount Management
- Apply percentage-based discounts to products.
- Set discount start and end dates.
- Update and delete existing discounts.
- Display original and discounted product prices.
- Validate discount percentages and overlapping discounts.

### 3.3 Client Management
- Add new clients.
- View client information.
- Update and delete client records.
- Associate clients with their orders.
- Prevent deletion of clients who have existing orders.

### 3.4 Order Management
- Create orders containing multiple products.
- Associate orders with clients.
- Track order statuses.
- Update order statuses.
- Validate product availability and requested quantities.
- Store product prices at the time of purchase.
- Prevent deletion of confirmed orders.

### 3.5 Advanced Product Search

Products can be filtered using multiple criteria:
- Category
- Gender
- Brand
- Minimum and maximum price
- Size
- Color
- Availability (in stock or out of stock)

Multiple filters can be combined to find specific products.

### 3.6 Real-Time Stock Tracking

The application dynamically calculates the available quantity of each product.

**Formula:**

`Available Quantity = Initial Quantity - Sold Quantity`

Only products included in confirmed or shipped orders are counted as sold.

### 3.7 Sales Reports
- Daily earnings.
- Monthly earnings.
- Top-selling products.

### 3.8 User Authentication and Role-Based Access Control

The application uses JWT-based authentication to identify users and control access to different functionalities.

Three user roles are available:

**Admin**
- Full access to the system.
- Manage products, users, and user roles.
- Manage discounts and lookup tables.
- View and manage orders.
- Generate sales reports.

**Advanced User**
- Add, update, and delete products.
- Update product stock quantities.
- View orders and update their statuses.
- Generate sales reports.
- Cannot manage users, roles, discounts, or lookup tables.

**Simple User**
- View products and available lookup information.
- Add and update products.
- Access permitted product and discount information.
- Cannot delete products, update stock, manage users, or access restricted administrative functionalities.

## 4. Database Structure

The application uses a relational MySQL database named `web_store_db`.

The database consists of the following main tables:

| Table | Description |
|---|---|
| Products | Stores product information |
| Categories | Stores product categories |
| Brands | Stores clothing brands |
| Sizes | Stores available product sizes |
| Colors | Stores available product colors |
| Genders | Stores product gender categories |
| Users | Stores registered user accounts |
| Roles | Stores user roles |
| Clients | Stores customer information |
| Orders | Stores order information |
| OrderItems | Stores products and quantities included in orders |
| Discounts | Stores product discount information |
| Product Color | Connects products with their available colors |
| Product Sizes | Connects products with their available sizes |

The Product Color and Product Sizes tables are association tables used to establish many-to-many relationships between products and their available colors and sizes.

## 5. REST API Documentation

The application provides REST API endpoints for managing authentication, products, lookup values, discounts, clients, orders, and reports.

**Base URL:**

`http://127.0.0.1:5000`

### 5.1 Authentication

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/register` | Register a new user | Public |
| POST | `/api/login` | Authenticate a user and receive a JWT token | Public |
| GET | `/api/profile` | Retrieve the current user's profile | Authenticated User |

### 5.2 User Management

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/users` | Retrieve all users | Admin |
| POST | `/api/users` | Create a new user | Admin |
| PUT | `/api/users/<id>/role` | Update a user's role | Admin |
| DELETE | `/api/users/<id>` | Delete a user | Admin |

### 5.3 Product Management

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/products` | Retrieve all products | Public |
| GET | `/api/products/<id>` | Retrieve a specific product | Authenticated User |
| POST | `/api/products` | Add a new product | Admin / Advanced User / Simple User |
| PUT | `/api/products/<id>` | Update a product | Admin / Advanced User / Simple User |
| DELETE | `/api/products/<id>` | Delete a product | Admin / Advanced User |
| PUT | `/api/products/<id>/stock` | Update initial stock quantity | Admin / Advanced User |
| GET | `/api/products/<id>/quantity` | Retrieve product stock information | Check authentication requirements |
| GET | `/api/products/search` | Search and filter products | Check authentication requirements |

### 5.4 Lookup Management

Lookup values include categories, brands, sizes, colors, and genders.

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/lookups/<lookup_type>` | Retrieve lookup values | Authenticated User |
| POST | `/api/lookups/<lookup_type>` | Add a lookup value | Admin |
| PUT | `/api/lookups/<lookup_type>/<id>` | Update a lookup value | Admin |
| DELETE | `/api/lookups/<lookup_type>/<id>` | Delete a lookup value | Admin |

### 5.5 Discount Management

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/products/<id>/discounts` | Apply a discount to a product | Admin |
| GET | `/api/products/<id>/discounts` | Retrieve discounts for a product | Authenticated User |
| GET | `/api/discounts/<id>` | Retrieve a specific discount | Authenticated User |
| PUT | `/api/discounts/<id>` | Update a discount | Admin |
| DELETE | `/api/discounts/<id>` | Delete a discount | Admin |

### 5.6 Client Management

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/clients` | Retrieve all clients | Authenticated User |
| GET | `/api/clients/<id>` | Retrieve a specific client | Authenticated User |
| POST | `/api/clients` | Add a new client | Public |
| PUT | `/api/clients/<id>` | Update a client | Verify route permissions |
| DELETE | `/api/clients/<id>` | Delete a client | Verify route permissions |

### 5.7 Order Management

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/orders` | Create a new order | Public |
| GET | `/api/orders` | Retrieve all orders | Admin / Advanced User |
| GET | `/api/orders/<id>` | Retrieve a specific order | Check route permissions |
| PUT | `/api/orders/<id>/status` | Update order status | Admin / Advanced User |
| DELETE | `/api/orders/<id>` | Delete an order | Admin |

**Example order creation request:**

```json
{
    "items": [
        {
            "product_id": 1,
            "quantity": 2,
            "size_id": 1,
            "color_id": 1
        }
    ]
}
```

**Example order status update:**

```json
{
    "status": "confirmed"
}
```

Supported order statuses should follow the values implemented in the application.

The application validates product availability and requested quantities before accepting orders. Stock is calculated based on confirmed and shipped orders.

### 5.8 Reports

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/reports/daily` | Generate daily earnings report | Admin / Advanced User |
| GET | `/api/reports/monthly` | Generate monthly earnings report | Admin / Advanced User |
| GET | `/api/reports/top-products` | Retrieve top-selling products | Admin / Advanced User |

## 6. Installation and Setup

### Prerequisites

Make sure the following software is installed:
- Python 3
- MySQL Server
- MySQL Workbench (optional)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Lebibe735/StyleHub.git
```

Navigate to the project directory:

```bash
cd StyleHub
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

Install the project dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Database

1. Start your MySQL server.
2. Create a database named `web_store_db`.
3. Configure the database connection in the application.
4. Make sure your MySQL username and password are correct.

Create the database using:

```sql
CREATE DATABASE web_store_db;
```

The application initializes the required database tables and default lookup values when it starts.

### Step 5: Run the Application

```bash
python app.py
```

The application will be available at:

`http://127.0.0.1:5000`

Open this address in your browser to access StyleHub.

## 7. API Testing with Postman

The REST API endpoints can be tested using Postman.

For protected endpoints:

1. Send a POST request to `/api/login`.
2. Enter the user's login credentials.
3. Copy the JWT token from the response.
4. Open the Authorization tab in Postman.
5. Select **Bearer Token**.
6. Paste the JWT token.
7. Send requests to the protected endpoints.

Different user roles can be tested to verify that the role-based access control works correctly.

For example:
- Admin users should have access to administrative endpoints.
- Advanced users should receive access only to their permitted functionalities.
- Simple users should receive a `403 Forbidden` response when attempting restricted actions.

## 8. Project Repository

GitHub Repository:

https://github.com/Lebibe735/StyleHub

## 9. Author

**Lebibe Mehmedi**

Master's Student in Software Engineering  
South East European University (SEEU)

---

**StyleHub – Clothing Store Management System**
