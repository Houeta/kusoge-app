# Kusoge App

## Overview
Kusoge App is a simple Python application designed as a part of a pet project to demonstrate various DevOps practices. "Kusoge" is a Japanese term for a video game or piece of software that is considered low quality or poorly designed.

## Purpose
The purpose of this project is to showcase DevOps concepts such as continuous integration (CI), continuous deployment (CD), infrastructure as code (IaC), and containerization using Docker. It serves as a learning tool for understanding how these practices can be implemented in a real-world scenario.

## Features
- Simple REST API for retrieving kusoge messages
- Basic web interface for interacting with the API

## Technologies Used
- Python
- Flask (for the REST API)
- Docker
- Github Actions (for CI)

## Web access
Access the web interface at [`https://app.kusoge.watashinoheyadesu.pp.ua`](https://app.kusoge.watashinoheyadesu.pp.ua) to generate and view kusoge shop.

## CI/CD Pipeline
This project includes a CI pipeline implemented with Github Actions. The pipeline is defined [here](.github/workflows/) and automates the following tasks:
- Building the Docker image
- Running tests
- Pushing the Docker image to a Docker registry
- Trigger xasc-repository
