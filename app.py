from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import errorcode
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Database configuration (!!! MODIFY THIS !!!) ---
config = {
    'user': 'root',
    'password': 'sanket9899',  
    'host': '127.0.0.1',
    'database': 'railway_db',
    'autocommit': False # ESSENTIAL for transactions
}
# ---------------------------------------------------


# --- This is the booking logic ---
def book_ticket(user_id, train_id, travel_date, passenger_list):
    seat_count_to_book = len(passenger_list)
    conn = None
    cursor = None
    
    try:
        # 1. Connect to the database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 2. Check available seats FOR UPDATE (This locks the row)
        query_check_seats = """
        SELECT total_seats - IFNULL(SUM(b.seat_count), 0) AS available
        FROM Trains t
        LEFT JOIN Bookings b ON t.train_id = b.train_id 
                               AND b.travel_date = %s 
                               AND b.status = 'CONFIRMED'
        WHERE t.train_id = %s
        GROUP BY t.train_id, t.total_seats
        FOR UPDATE
        """
        
        cursor.execute(query_check_seats, (travel_date, train_id))
        result = cursor.fetchone()
        
        # --- *** MODIFIED ERROR CHECKING *** ---
        if not result:
            print(f"Error: Train ID {train_id} not found.")
            conn.rollback()
            return False, f"Error: Train ID {train_id} does not exist."
        
        available_seats = result[0]
        if available_seats < seat_count_to_book:
            print(f"Error: Not enough seats. Available: {available_seats}, Required: {seat_count_to_book}")
            conn.rollback()
            return False, f"Not enough seats available. Only {available_seats} left."
        # --- *** END OF MODIFICATION *** ---

        # 3. If seats are available, create the booking
        print(f"Success: {available_seats} seats available. Booking {seat_count_to_book}...")
        
        query_insert_booking = """
        INSERT INTO Bookings (user_id, train_id, travel_date, seat_count, status, total_fare, pnr_number)
        VALUES (%s, %s, %s, %s, 'CONFIRMED', %s, %s)
        """
        fare = 100.0 * seat_count_to_book 
        pnr = f"PNR{user_id}{train_id}{travel_date.replace('-', '')}" 
        
        cursor.execute(query_insert_booking, 
                       (user_id, train_id, travel_date, seat_count_to_book, fare, pnr))
        
        # Get the ID of the new booking
        new_booking_id = cursor.lastrowid

        # 4. Add each passenger
        query_insert_passenger = """
        INSERT INTO Passengers (booking_id, passenger_name, age, gender)
        VALUES (%s, %s, %s, %s)
        """
        for passenger in passenger_list:
            cursor.execute(query_insert_passenger, 
                           (new_booking_id, passenger['name'], passenger['age'], passenger['gender']))

        # 5. Commit the transaction
        conn.commit()
        print(f"Booking successful! PNR: {pnr}")
        return True, f"Booking successful! PNR: {pnr}"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if conn:
            conn.rollback() 
        # Pass the specific error message to the frontend
        return False, f"Database error: {err}"
        
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# --- Flask Web Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def handle_booking():
    try:
        user_id = request.form['user_id']
        train_id = request.form['train_id']
        travel_date_str = request.form['travel_date']
        
        passengers = [
            {'name': request.form['passenger_name'], 
             'age': int(request.form['passenger_age']), 
             'gender': request.form['passenger_gender']}
        ]
        
        success, message = book_ticket(user_id, train_id, travel_date_str, passengers)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
    except Exception as e:
        flash(f"An error occurred: {e}", 'error')
            
    return redirect(url_for('index'))

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)
