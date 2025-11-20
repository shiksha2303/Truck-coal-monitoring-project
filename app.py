CSV_FILE = 'truck_log.csv'

# Create CSV with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Truck Number', 'Driver Name', 'Expected Route', 'Actual Route', 'Status'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    truck_number = request.form['truck_number']
    driver_name = request.form['driver_name']
    expected_route = request.form['expected_route'].strip().lower()
    actual_route = request.form['actual_route'].strip().lower()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if expected_route != actual_route:
        status = "⚠️ Route Deviation Alert"
    else:
        status = "✅ Route Verified"

    # Save to CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, truck_number, driver_name, expected_route, actual_route, status])
    
    return f"""
        <h2>{status}</h2>
        <p><strong>Truck Number:</strong> {truck_number}</p>
        <p><strong>Driver Name:</strong> {driver_name}</p>
        <p><strong>Expected Route:</strong> {expected_route.upper()}</p>
        <p><strong>Actual Route:</strong> {actual_route.upper()}</p>
        <p><strong>Time:</strong> {timestamp}</p>
        <br><a href="/">Go Back</a>
    """

# ✅ PASTE THIS AFTER SUBMIT FUNCTION (outside it)
@app.route('/dashboard')
def dashboard():
    entries = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            entries.append(row)
    
    return render_template('dashboard.html', entries=entries)

# 🔚 Bottom of the file
if __name__ == '__main__':
    app.run(debug=True)

