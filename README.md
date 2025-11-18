# RailwayProject_MySQL
This DBMS Mini Project is a functional Railway Ticket Booking System. It demonstrates backend engineering skills by solving the "Lost Update" problem common in reservation systems. Using MySQL's transaction controls, the app ensures that multiple users cannot book the same seat simultaneously.

# 🚂 Railway Reservation System (DBMS Project)

**RailwayProject_MySQL** is a web-based booking system that demonstrates core Database Management System (DBMS) concepts using **Python (Flask)** and **MySQL**. 

The project solves the "race condition" problem in ticket booking by using transaction management and row-level locking.

## ✨ Key Features
* **Concurrency Control:** Uses MySQL `FOR UPDATE` locking to prevent two users from booking the last seat at the exact same time.
* **ACID Transactions:** Ensures data integrity; if any part of the booking fails, the entire transaction is rolled back.
* **Dynamic Booking:** Real-time seat availability checking and PNR generation.
* **User Interface:** Glassmorphism-styled UI built with HTML/CSS and FontAwesome.

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS
* **Backend:** Python (Flask)
* **Database:** MySQL
* **Tools:** VS Code, MySQL Workbench

## 📂 Project Structure
```text
RailwayProject_MySQL/
├── app.py               # Main Python Flask application
├── templates/           # Folder containing HTML files
│   └── index.html       # The frontend user interface
└── README.md            # Project documentation
