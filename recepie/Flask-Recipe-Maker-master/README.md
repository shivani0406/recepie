# Flask Recipe Realm

A comprehensive web application built with Flask, allowing users to create, edit, and manage recipes. The application features user authentication, image uploads, and a modern design using Bootstrap.


## Features

- **User Authentication**: Register, login, and manage user sessions.
- **Recipe Management**: Add, edit, and delete recipes.
- **Image Uploads**: Upload and display images with recipes.
- **Responsive Design**: Clean, modern UI using Bootstrap 4.
- **Enhanced UI**: Background images and improved fonts for a recipe-centric look.
- **Delete Confirmation**: Confirm recipe deletions with a dialog prompt.

## Requirements

To run this project, you'll need:

- Python 3.7 or higher
- Flask
- SQLAlchemy
- Flask-Migrate
- Jinja2
- Bootstrap 4
- AOS (Animate on Scroll) for animations

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/Flask-Recipe-List.git
cd Flask-Recipe-List
```

### Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

### Install the Required Packages

```bash
pip install -r requirements.txt
```

### Set Up the Database

```bash
flask --app main db init
flask --app main db migrate -m "Initial migration"
flask --app main db upgrade
```

## Configuration

Configure application settings in `config.py`:

- **`UPLOAD_FOLDER`**: Directory for storing uploaded images.
- **`SQLALCHEMY_DATABASE_URI`**: URI for your database.
- **`SECRET_KEY`**: Secret key for session management and CSRF protection.

## Running the Application

To start the application, use:

```bash
flask --app main run
```

Visit `http://127.0.0.1:5000/` in your browser to access the application.

## Project Structure

```
flask_recipe_maker/
│
├── main.py                # Main application file
├── config.py              # Configuration settings
├── models.py              # Database models
├── templates/             # HTML templates
├── static/                # Static files (CSS, JavaScript, images)
├── migrations/            # Database migrations
└── README.md              # This README file
```

## Future Improvements

- **User Authentication Enhancements**: Implement features like password reset and user profile management.
- **Pagination**: Add pagination to the recipe list for better usability.
- **Image Handling**: Improve image management with resizing and thumbnails.
- **Advanced UI Features**: Explore additional UI enhancements and animations.

## Contributing

Contributions are welcome! Fork the repository and submit a pull request for review.

## Website 

![Screenshot 2024-08-07 172814](https://github.com/user-attachments/assets/1088424a-8414-45ac-aac4-1f047c4bf6b3)

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The Python microframework used in this project.
- [Bootstrap](https://getbootstrap.com/) - The CSS framework for styling.
- [AOS](https://michalsnik.github.io/aos/) - For scroll animations.
