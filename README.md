# Diggity Jobs

A brief description of what this project does and who it's for.

## Description

This project is a comprehensive job management system that automates the process of scraping job listings from various sources, tracking job applications, and managing job-related outreach efforts. It features a user-friendly web interface for easy interaction and management of job listings.

## Features

- Automated scraping of job listings.
- Job application tracking and management.
- Outreach efforts tracking for each job application.
- User-friendly web interface for ease of use.

## Getting Started

### Dependencies

- MongoDB
- Python 3.x
- FastAPI
- Uvicorn
- React
- Node.js and npm

### Installing

1. Clone the repository to your local machine.
2. Ensure MongoDB is installed and running.
3. Install the required Python dependencies by navigating to the project root and running:

```bash
pip install -r requirements.txt
```

4. Install the required Node.js dependencies by navigating to the `frontend` directory and running:

```bash
npm install
```

### Executing the program

To run the project, you need to start both the backend FastAPI server and the frontend React application.

1. Start the backend server:

```bash
# Activate the Python virtual environment
source venv/bin/activate
# Start the FastAPI server
uvicorn main:app --reload
```

2. In a new terminal, start the frontend application:

```bash
# Navigate to the frontend directory
cd frontend
# Start the React application
npm start
```

### Running Tests

To run the automated tests for this project, use the following command:

```bash
python3 -m pytest
```

### Backup Database

To backup the MongoDB database, use the following command:

```bash
mongodump --db job_database --out ~/mongodb-backups/backup-$(date +%Y-%m-%d)
```
<!-- 
## License

This project is licensed under the [LICENSE NAME HERE] License - see the LICENSE.md file for details.

## Acknowledgments

Inspiration, code snippets, etc.
- [example1](http://www.example.com)
- [example2](http://www.example.com) -->
