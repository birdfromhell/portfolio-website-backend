# README.md content for the portfolio-admin project

# Portfolio Admin Dashboard

This project is an admin dashboard for a portfolio website built using Flask. It provides functionalities for user management and statistics display.

## Project Structure

```
portfolio-admin
├── src
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── main.js
│   ├── templates
│   │   ├── admin
│   │   │   ├── dashboard.html
│   │   │   ├── login.html
│   │   │   └── base.html
│   │   └── index.html
│   ├── models
│   │   └── user.py
│   ├── routes
│   │   └── admin.py
│   ├── utils
│   │   └── auth.py
│   └── app.py
├── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd portfolio-admin
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/app.py
   ```

## Usage

- Access the admin dashboard at `http://localhost:5000/admin`.
- Use the login page to authenticate as an admin user.

## License

This project is licensed under the MIT License.