# Vehicle Parking System (ParkingPoint)

A Flask-based RESTful API web application for managing a smart parking system with authentication, booking, admin dashboards, and background task automation.

---

## Author
**Name:** Mangal Devanshu Govind  
**Roll Number:** 23f2001952  
**Email:** 23f2001952@ds.study.iitm.ac.in  
**Program:** BSc Data Science, IIT Madras  

---

## Project Description
This project involved developing a RESTful API-based web application that allows users to:

- Register and authenticate securely  
- Book parking spots  
- Manage parking lots and spot availability  
- View booking history and summaries  
- Access role-based dashboards (User/Admin)  

Admins can additionally monitor analytics, manage lots/spots, and generate reports via Celery-powered background tasks.  
The application is modular, scalable, and follows OpenAPI documentation standards.

---

## Technologies Used
- **Backend:** Flask, Flask-JWT-Extended, Flask-SQLAlchemy  
- **Database:** SQLite (development)  
- **Frontend:** Vue.js, Bootstrap, Chart.js  
- **Testing:** Postman  
- **Task Scheduling:** Celery + Redis  

---

## API Design
- **Framework:** Flask (RESTful API)  
- **Authentication:** JWT tokens secure all sensitive endpoints  
- **Features:**  
  - User registration and login  
  - Parking lot and spot management  
  - Booking system with history tracking  
  - Role-based dashboards (User/Admin)  
  - Asynchronous background tasks (CSV reports, summaries)  
- **Structure:** Modular design with blueprints  

---

## Database Schema Design
- Normalized schema avoids duplication and ensures separation of concerns  
- Foreign keys maintain referential integrity between users, lots, spots, and bookings  
- Enum constraints enforce valid spot states only  
- Validations such as `NOT NULL`, `UNIQUE`, and defaults ensure secure data entry  
- Scalable structure supports future features such as pricing, payments, and role-based access

<img width="803" height="844" alt="image" src="https://github.com/user-attachments/assets/3fe1217c-73c2-499c-ba9c-25c49c54fdef" />

---

## Architecture and Features
- **Backend:**  
  - Organized into controllers, routes, models, and middleware  
  - JWT-protected endpoints  
  - Celery for background tasks such as CSV generation and monthly summaries  

- **Frontend:**  
  - Vue-based pages and reusable components  
  - Bootstrap for styling  
  - Chart.js for analytics and dynamic charts  

---

## Demo Video
[Watch the Demo](https://drive.google.com/file/d/1xzGR7W_nUxjjfoWiiJjrdzAVT62baPAC/view?usp=sharing)

---

## Future Enhancements
- Integration of payment gateway  
- Dynamic pricing models  
- Advanced analytics and reporting for admins  
- Enhanced role-based permissions  

---

## License
This project is for academic purposes under the IIT Madras BSc Data Science program.
  
