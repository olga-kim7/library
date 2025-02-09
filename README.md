# **Library Management System**  

### **Requirements:**  

**Functional:**  
- Web-based application  
- Manage book inventory  
- Manage book borrowing  
- Manage customers  
- Display notifications  
- Handle payments  

**Non-functional:**  
- Support for 5 concurrent users  
- Handle up to 1,000 books  
- Support 50,000 borrowings per year  
- Approximate data usage of ~30MB per year  

### **Specific Endpoint Requirements:**  

**Payment Endpoint:**  
- Implement an endpoint that makes requests to the Stripe service to handle payments.  

**Borrowers List Endpoint:**  
- Endpoint takes a search string as an argument and returns a list of current borrowers.  

**Local Database Integration:**  
- Requests of the implemented API should work with the local database (fetch data from the database, not from the Library API).  

### **Technologies to Use:**  
- Stripe API for payment processing  
- Telegram API for sending notifications  
- Celery for asynchronous requests to notify about each new borrower  
- Swagger for documenting all endpoints  

### **How to Run:**  
- Copy `.env.sample` to `.env` and populate it with all required data.  
- Install dependencies:  
  ```bash
  pip install -r requirements.txt
  ```
- Start the application:  
  ```bash
  python manage.py runserver
  ```
- Create an admin user:  
  ```bash
  python manage.py createsuperuser
  ```
- Start Celery for handling background tasks:  
  ```bash
  celery -A library worker --loglevel=info
  ```

  
### **API Documentation:**  
- All endpoints are documented using Swagger.  
- Swagger documentation can be accessed at:  
  ```
  http://localhost:8000/swagger/
  ```  

Let me know if you need any changes! 🚀