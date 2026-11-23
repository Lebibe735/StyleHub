
# StyleHub – Clothing Store Web Application

## 1. Project Description

StyleHub is a web-based clothing store management system developed using Flask, MySQL, HTML, CSS, and JavaScript.

The application allows users to manage clothing products, categories, brands, sizes, colors, clients, orders, discounts, and stock quantities.

It also provides advanced product search, real-time stock tracking, user authentication, role-based access control, and sales reports.

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
- MySQL
- Postman
- Git and GitHub

## 3. Main Features

### Product Management
- Add, edit, view, and delete products.
- Manage product names, descriptions, and prices.
- Assign categories, brands, genders, sizes, and colors.
- Manage available stock quantities.

### Discount Management
- Apply percentage-based discounts to products.
- Set discount start and end dates.
- Update and delete discounts.
- Display discounted product prices.

### Client Management
- Add new clients.
- View client information.
- Edit and delete client records.
- Associate clients with their orders.

### Order Management
- Create orders for clients.
- Add multiple products to an order.
- Track order statuses.
- Update order statuses.
- Validate product availability before confirming orders.

### Advanced Product Search
Products can be filtered using multiple criteria:
- Category
- Gender
- Brand
- Minimum and maximum price
- Size
- Color
- Availability (in stock or out of stock)

### Real-Time Stock Tracking

The application dynamically calculates available product quantities.

**Formula:**

Current Quantity = Initial Quantity - Sold Quantity

Only products in confirmed or shipped orders are counted as sold.

### Reports
- Daily earnings.
- Monthly earnings.
- Top-selling products.

### User Authentication and Roles

The application uses JWT-based authentication and role-based access control.

Three user roles are available:

**Admin**
- Full access to the system.
- Manage products, users, and roles.
- Manage discounts and lookup tables.
- View and manage orders.
- Generate reports.

**Advanced User**
- Manage products.
- View orders and update their statuses.
- Update stock quantities.
- Generate sales reports.

**Simple User**
- Manage products with limited privileges.
- Cannot manage users or generate reports.
- Cannot access restricted administrative functionalities.

## 4. Database Structure

The application uses a relational MySQL database named `web_store_db`.

Main database tables include:

| Table | Description |
|---|---|
| Products | Stores product information |
| Categories | Product categories |
| Brands | Product brands |
| Sizes | Available product sizes |
| Colors | Available product colors |
| Genders | Men, Women, and Children |
| Users | User accounts |
| Roles | User roles and permissions |
| Clients | Customer information |
| Orders | Order information |
| OrderItems | Products and quantities within orders |
| Discounts | Product discount information |
| Product Color | Connects products with their available colors |
| Product Sizes | Connects products with their available sizes |

## 5. REST API Endpoints

Base URL:

`http://127.0.0.1:5000`

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register a user |
| POST | `/api/login` | Authenticate a user |
| GET | `/api/profile` | Get current user profile |

### Products
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products` | Get all products |
| GET | `/api/products/<id>` | Get a specific product |
| POST | `/api/products` | Add a product |
| PUT | `/api/products/<id>` | Update a product |
| DELETE | `/api/products/<id>` | Delete a product |
| PUT | `/api/products/<id>/stock` | Update product stock |
| GET | `/api/products/<id>/quantity` | Get current product quantity |
| GET | `/api/products/search` | Search and filter products |

### Lookup Management
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/lookups/<lookup_type>` | Get lookup values |
| POST | `/api/lookups/<lookup_type>` | Add a lookup value |
| PUT | `/api/lookups/<lookup_type>/<id>` | Update a lookup value |
| DELETE | `/api/lookups/<lookup_type>/<id>` | Delete a lookup value |

Lookup types include categories, brands, sizes, colors, and genders.

### Discounts
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/products/<id>/discounts` | Apply a discount |
| GET | `/api/products/<id>/discounts` | Get product discounts |
| GET | `/api/discounts/<id>` | Get a specific discount |
| PUT | `/api/discounts/<id>` | Update a discount |
| DELETE | `/api/discounts/<id>` | Delete a discount |

### Clients
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/clients` | Get all clients |
| GET | `/api/clients/<id>` | Get a specific client |
| POST | `/api/clients` | Add a client |
| PUT | `/api/clients/<id>` | Update a client |
| DELETE | `/api/clients/<id>` | Delete a client |

### Orders
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/orders` | Get all orders |
| GET | `/api/orders/<id>` | Get a specific order |
| POST | `/api/orders` | Create an order |
| PUT | `/api/orders/<id>/status` | Update order status |
| DELETE | `/api/orders/<id>` | Delete an order |

### Reports
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/reports/daily-earnings` | Generate daily earnings |
| GET | `/api/reports/monthly-earnings` | Generate monthly earnings |
| GET | `/api/reports/top-products` | Get top-selling products |

## 6. Installation and Setup

### Prerequisites
Make sure you have installed:
- Python 3
- MySQL Server
- MySQL Workbench (optional)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Lebibe735/StyleHub.git
```

Navigate to the project folder:

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

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Database

1. Start your MySQL server.
2. Create a database named `web_store_db`.
3. Configure the database connection in the application.
4. Make sure your MySQL username and password are correct.

```sql
CREATE DATABASE web_store_db;
```

The application initializes the required database tables and default lookup values.

### Step 5: Run the Application

```bash
python app.py
```

The backend server will be available at:

`http://127.0.0.1:5000`

Open the application in your browser to access StyleHub.

## 7. API Testing

The REST APIs can be tested using Postman.

For protected endpoints:
1. Send a POST request to `/api/login`.
2. Obtain the JWT token from the response.
3. Open the Authorization tab in Postman.
4. Select Bearer Token.
5. Paste the token.
6. Send requests to the protected endpoints.

## 8. Project Repository

GitHub: https://github.com/Lebibe735/StyleHub

## 9. Author

**Lebibe Mehmedi**

Masters's Degree in Computer Science  
South East European University (SEEU)

---

**StyleHub – Clothing Store Management System**
