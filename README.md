# Harry Potter In Depth Query Bot

The Harry Potter In-Depth Query Bot is a AI-powered Query bot that allows users to explore the magical world of Harry Potter by asking in-depth questions based on the full text of all seven Harry Potter books. By leveraging the power of Retrieval-Augmented Generation (RAG), the bot retrieves relevant text chunks and generates contextually accurate responses using the GPT-3.5-turbo model. The project is containerized with Docker and deployed on AWS Lambda and API Gateway, ensuring scalability and serverless architecture.

<table border="2" style="width:100%; border-collapse: collapse;">
  <tr>
    <td><img src="https://github.com/user-attachments/assets/6deccd80-3de7-470a-95ae-ba19b910dd95" alt="Project Image 1" style="width:100%;"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/74a78ed2-5c62-4e27-b5c3-91c7bde856a3" alt="Project Image 2" style="width:100%;"></td>
  </tr>
</table>

**[Check out the live project here!](https://lp0b66aa4h.execute-api.us-east-1.amazonaws.com/Prod/)**

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Deployment](#deployment)
7. [License](#license)

## Project Overview

This project uses advanced NLP techniques to break down the complete text of the seven Harry Potter books into manageable chunks, storing them as a vector database. The system utilizes Chroma for vectorization and OpenAI’s embeddings to create a searchable database. When a query is made, relevant text segments are retrieved, and the GPT-3.5-turbo model is employed to generate a human-like response, simulating an in-depth discussion of the Harry Potter series.

## Features

- **Data Ingestion:** The entire Harry Potter series is ingested as text files. These texts are then chunked into smaller, manageable pieces and saved as a pickle file in the data/processed folder.
- **Data Preprocessing:** The text chunks are vectorized using Chroma and OpenAIEmbeddings, forming the backbone of the search functionality.
- **Web Interface:** A user-friendly Flask web interface allows users to interact with the bot and ask questions.
- **Dockerized:** The project is fully containerized using Docker, making it easy to deploy across different environments.
- **AWS Deployment:** The application is deployed on AWS Lambda and API Gateway, providing a scalable, serverless architecture.

## Project Structure

```markdown
├── LICENSE
├── README.md              <- The top-level README for developers using this project.
├── data
│   ├── processed          <- Contains the document.pkl file which holds the chunks of text.
│   ├── vector_db          <- Stores the vector database for quick retrieval.
│   └── raw                <- The original seven Harry Potter books as text files.
├── requirements.txt       <- The requirements file for reproducing the environment.
├── src                    <- Source code used in this project.
│   ├── __init__.py        <- Makes src a Python module.
│   ├── base.py            <- Contains utility functions.
│   ├── data_preprocessing.py <- Code to create the vector database using Chroma and OpenAIEmbeddings.
│   └── data_ingestion.py  <- Handles the loading, chunking, and saving of text data.
├── templates
│   └── index.html         <- HTML template for the web app.
├── .gitignore             <- Specifies which files to ignore in the version control.
├── .dvc                   <- DVC configuration file for data version control.
├── app.py                 <- Main Flask application file.
├── dvc.lock               <- DVC lock file ensuring reproducibility.
├── Dockerfile             <- Dockerfile for containerizing the app.
├── dvc.yaml               <- DVC pipeline configuration.
├── template.yaml          <- AWS Lambda and API Gateway configuration template.

```
## Installation

To get a copy of the project up and running on your local machine, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/TarunSingh2002/Harry-Potter-In-Depth-Query-Bot.git
    cd Harry-Potter-In-Depth-Query-Bot
    ```

2. **Set up a virtual environment:**
    ```bash
    conda create --name harry-potter-bot python=3.12
    conda activate harry-potter-bot
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Build and run the Docker container:**
    ```bash
    docker build -t harry-potter-bot .
    docker run -p 5000:5000 harry-potter-bot
    ```

## Usage

1. **Run the Flask application:**
    ```bash
    python app.py
    ```

2. **Open your browser and go to:**
    ```
    http://localhost:5000
    ```

3. **Interact with the bot by asking your Harry Potter-related questions.**

## Deployment

### Deploying to AWS Lambda and API Gateway

1. **Ensure you have AWS CLI installed and configured:**
    ```bash
    aws configure
    ```

2. **Build and push the Docker image to Amazon ECR:**
    ```bash
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
    docker tag harry-potter-bot:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/harry-potter-bot:latest
    docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/harry-potter-bot:latest
    ```

3. **Deploy the application using AWS SAM:**
    ```bash
    sam build --template-file template.yaml
    sam deploy --guided
    ```

4. **Follow the prompts to complete the deployment.**

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/TarunSingh2002/Harry-Potter-In-Depth-Query-Bot/blob/main/LICENSE.txt) file for details.