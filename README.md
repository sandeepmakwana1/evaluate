# Solution Evaluator - Serverless Application

A serverless application that evaluates coding solutions using Google's Generative AI. This service provides automated assessment of code submissions, focusing on logical correctness, edge case handling, code quality, and performance optimization. The evaluation system uses advanced AI models to provide detailed feedback and scoring based on multiple criteria.

## Features

- Serverless architecture using AWS Lambda for scalable, cost-effective execution
- Automated code evaluation using Google's Generative AI Gemini 1.5 model
- RESTful API endpoint with CORS support for cross-origin requests
- Secure environment variable handling with encryption at rest
- Docker-based dependency management for consistent environments
- AWS Lambda Layer for optimized deployment and reduced cold starts
- Comprehensive evaluation metrics including:
  - Code correctness
  - Time complexity analysis
  - Space complexity analysis
  - Code style and best practices
  - Documentation quality
  - Error handling
  - Edge case coverage

## Prerequisites

- Node.js (v14 or later) for running build tools and scripts
- Python 3.10 for the Lambda runtime environment
- Docker for local testing and dependency compilation
- AWS CLI configured with appropriate credentials and permissions
  - IAM role with Lambda execution permissions
  - API Gateway permissions
  - CloudWatch logs access
- Serverless Framework (v3.0 or later) for infrastructure management
- Google AI API key with PaLM API access enabled

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/solution-evaluator.git
   cd solution-evaluator
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   - Create a `.env` file and add your Google API key:
     ```
     GOOGLE_API_KEY=your_google_api_key
     ```

## Deployment

1. Deploy the application using the Serverless Framework:
   ```bash
   serverless deploy
   ```

2. After deployment, note the service endpoint URL provided in the output.
