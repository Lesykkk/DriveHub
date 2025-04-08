# DriveHub Platform
### *A modern web platform that simplifies the process of buying and selling vehicles.* ###

![logo](https://github.com/user-attachments/assets/c84a081a-86b0-43ba-ae88-3681fe5aebe2)

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

DriveHub is a Django-based web platform that connects buyers and sellers of transport vehicles. The platform provides:

- User accounts with different roles
- Vehicle listings with advanced search/filter capabilities
- Rating and review system

## Technologies

### Backend
- Django (4.2+) - Core framework
- SQLite3 - Primary database

### Frontend
- HTML5, CSS3, JavaScript

## Setup Instructions

### Requirements
- Python 3.10+

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lesykkk/drivehub.git
   cd drivehub

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
4. **Run migrations**
   ```bash
   python manage.py migrate
   
5. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser

6. **Run development server**
   ```bash
   python manage.py runserver
   ```
   Access the admin panel at: http://localhost:8000/admin

### Contributing
We welcome contributions! Please follow these steps:

- Fork the repository
- Create your feature branch
- Commit your changes
- Push to the branch
- Create a Pull Request

### License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Lesykkk/DriveHub/blob/main/LICENSE) file for details.
