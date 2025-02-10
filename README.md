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
How to Run:

Copy .env.sample to .env and populate it with all required data.
Run the following command to build and start the application:
docker-compose up --build

Create an admin user and schedule the synchronization of overdue borrowers.
