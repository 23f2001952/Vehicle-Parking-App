from celery import shared_task
from application.models import User,BookingHistory
from application.database import db
import csv
from jinja2 import Template 
from .mail import send_email
import requests

@shared_task(ignore_result=False, name="download_csv_report")  
def user_csv_report():
    user_details = User.query.filter(User.role != "admin").all()
    csv_file_name = "user_details.csv"
    with open(f'static/{csv_file_name}', 'w', newline="") as csvfile:
        sr_no = 1
        user_csv = csv.writer(csvfile, delimiter=',')
        user_csv.writerow(["Sr No", "Username", "Email", "Address", "Pincode"]) 
        for user in user_details:
            user_row = [sr_no, user.username, user.email, user.address, user.pincode]
            user_csv.writerow(user_row)
            sr_no += 1
    return csv_file_name



@shared_task(ignore_result=True, name="monthly_report")
def monthly_report():
    users = User.query.filter_by(role="user").all()
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['address'] = user.address 
        user_data['pincode'] = user.pincode 
        booking_history = BookingHistory.query.filter_by(user_id=user.id).all()
        bookings = []  
        for booking in booking_history:
            booking_data = {
                'spot_id': booking.spot_id,
                'vehicle_number': booking.vehicle_number,
                'start_time': booking.start_time.isoformat(),
                'end_time': booking.end_time.isoformat() if booking.end_time else None,
                'parking_cost': str(booking.parking_cost) if booking.parking_cost else None,
                'is_paid': booking.is_paid
            }
            bookings.append(booking_data)
        user_data['bookings'] = bookings

        mail_template = """
        <h3>Monthly Report for {{user_data['username']}}</h3>
        <p>Here is your monthly report:</p>
        <p>Email: {{user_data['email']}}</p>
        <p>Address: {{user_data['address']}}</p>
        <p>Pincode: {{user_data['pincode']}}</p>
        <h4>Booking History:</h4>
        <ul>
        {% for booking in user_data['bookings'] %}
            <li>
                Spot ID: {{booking['spot_id']}}<br>
                Vehicle Number: {{booking['vehicle_number']}}<br>
                Start Time: {{booking['start_time']}}<br>
                End Time: {{booking['end_time']}}<br>
                Parking Cost: {{booking['parking_cost']}}<br>
                Is Paid: {{booking['is_paid']}}
            </li>
        {% endfor %}
        </ul>
        """
        template = Template(mail_template)
        rendered_mail = template.render(user_data=user_data)
        send_email(user.email,"ParkingPoint - MonthlyReport", rendered_mail)


@shared_task(ignore_result=True, name="generate_msg")
def generate_msg(parking_plot, location):
    msg = f"This is to notify that new {parking_plot} has been added at {location}."
    response = requests.post(
        "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage",
        data={"chat_id": "<YOUR_CHAT_ID>", "text": msg}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
    else:    
        print("Message sent successfully")
    print(msg) 
    return msg