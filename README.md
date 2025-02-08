# File Upload Backend

This is the backend for the File Upload System. It is built using Django and Django REST Framework.

## Features

- Upload files in chunks
- List uploaded files
- Delete uploaded files

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/semahkadri/FileUpload-backend.git
    cd FileUpload-backend
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the migrations:**

    ```sh
    python manage.py migrate
    ```

5. **Start the development server:**

    ```sh
    python manage.py runserver
    ```

6. **Access the API:**

    Open your browser and go to `http://localhost:8000/api/`

## API Endpoints

- `POST /api/files/upload-chunk/` - Upload a file chunk
- `GET /api/files/` - List all uploaded files
- `DELETE /api/files/{file_id}/` - Delete a file

## Project Structure

- `backend/` - Django project settings
- `files/` - Django app for file upload functionality
- `manage.py` - Django management script

## License

This project is licensed under the MIT License.