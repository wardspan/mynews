# MyNews

MyNews is a personalized news aggregation platform similar to Flipboard, providing curated articles from multiple sources. The application allows users to customize their news feed, categorize content, save articles for later reading, and add personal notes and tags.

## Features

* Personalized News Feed: Browse curated articles from multiple news sources
* Customizable Categories: Add, remove, and modify news categories
* Smart Tagging: AI-powered article tagging and user-defined tags for better organization
* Article Management: Save articles, add personal notes, and filter by custom tags
* Tab-Based Navigation: Easy access to different categories with most recently visited tabs
* Sharing: Share articles with other users or via email
* User Accounts: Configurable user profiles with personal preferences
* Mobile-Friendly Interface: Responsive design for all devices

## Architecture
MyNews uses a modern, scalable architecture:

* Frontend: React/Next.js application hosted on Vercel
* Backend API: FastAPI Python service running on Google Cloud Run
* Database: MongoDB Atlas cloud database
* Processing Tasks: AI-powered article summarization and tagging
* News Sources: Multiple news APIs including NewsAPI, Gnews, The Guardian, and more

### Tech Stack
#### Frontend

* Next.js/React
* Chakra UI for component library
* React Query for state management
* Axios for API communication

#### Backend

* FastAPI (Python)
* Motor/PyMongo for MongoDB async operations
* NLTK and Transformers for NLP tasks
* JWT for authentication

#### Infrastructure

* Docker for containerization
* Google Cloud Run for backend hosting
* Vercel for frontend hosting
* MongoDB Atlas for database

## Getting Started
### Prerequisites

* Node.js (v14+)
* Python (v3.9+)
* Docker and Docker Compose
* MongoDB Atlas account
* API keys for news services

Local Development
Backend Setup

1. Clone the repository:
bash
```
git clone https://github.com/yourusername/mynews.git
cd mynews/backend
```

2. Create environment variables file:
bash
```
cp .env.example .env
```
# Edit .env with your API keys and MongoDB connection string

Start the backend with Docker:
bashCopydocker-compose up --build
The API will be available at http://localhost:8000
API Documentation:
CopyVisit http://localhost:8000/docs for Swagger UI documentation


Frontend Setup

Go to the frontend directory:
bashCopycd ../frontend

Install dependencies:
bashCopynpm install

Create environment variables:
bashCopycp .env.local.example .env.local
# Edit .env.local with your backend API URL

Start the development server:
bashCopynpm run dev
The frontend will be available at http://localhost:3000

Deployment
See our Deployment Guide for detailed instructions on deploying to:

Vercel (frontend)
Google Cloud Run (backend)
MongoDB Atlas (database)

API Integration
MyNews integrates with multiple news APIs:

NewsAPI.org
Gnews API
The Guardian Open Platform
Mediastack
CoinGecko API
Alpha Vantage API
Several cybersecurity news APIs

API keys for these services need to be added to your environment variables.
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Please make sure to update tests as appropriate and follow the code style guidelines.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

Inspired by Flipboard
Thanks to all the news APIs that make this application possible
Built with modern open-source technologies