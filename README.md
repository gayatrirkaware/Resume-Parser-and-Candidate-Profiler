# Resume-Parser-and-Candidate-Profiler

This is a Flask-based application that allows users to upload resumes, extract details, store them in a database, and retrieve candidate information.

## Features

- Upload resumes and extract key details
- Store candidate data in MongoDB
- Fetch a list of candidates
- Retrieve details of a specific candidate
- Remove candidate data along with the resume file

## Technologies Used

- Flask (Python web framework)
- MongoDB (Database for storing resume details)
- Jinja2 (Template rendering)
- HTML/CSS (Frontend for dashboards)
- `bson` (Handling MongoDB ObjectIds)

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/gayatrirkaware/Resume-Parser-and-Candidate-Profiler.git
   cd <Resume-Parser-and-Candidate-Profiler>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure MongoDB is running and update configuration if needed.

4. Run the Flask application:
   ```bash
   python main.py
   ```

5. Access the application at:
   ```
   http://localhost:8084
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/` | Loads the resume dashboard |
| `GET` | `/<page>` | Serves static pages |
| `POST` | `/upload-resume` | Uploads a resume and extracts details |
| `GET` | `/get-candidates` | Retrieves all stored candidates |
| `GET` | `/candidate/<candidate_id>` | Retrieves details of a specific candidate |
| `DELETE` | `/remove-candidate/<candidate_id>` | Removes a candidate and their resume |

## Folder Structure

```
├── main.py                 # Main application file
├── project_config.py       # Handles port number, database name and collection name
├── data_extraction.py      # Handles resume data extraction
├── app/database.py         # Database connection and utilities
├── templates/              # HTML template files
├── static/                 # Static assets (CSS, JS)
├── uploads/                # Folder for storing uploaded resumes
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

