# Federated Learning with Flower and JAX: Project Simplified Overview

This project demonstrates how multiple devices (or clients) can work together to train a machine learning model without sharing their private data. It uses **Flower**, a framework for federated learning, and **JAX**, a high-performance library for machine learning. The goal is to train a machine learning model (a type of neural network called CNN) on the MNIST dataset in a privacy-preserving way.

Federated learning ensures that the data stays on the client devices and only model updates (not the actual data) are shared with a central server. This makes the process more secure and scalable.

---

## **What This Project Does**

### **The Big Idea**
Imagine we have several devices (clients), each with its own small dataset. Instead of combining all the data in one place to train a model (which could be risky for privacy), we:
1. Train a copy of the model on each device using the local data.
2. Send updates (like improvements or changes to the model) to a central server.
3. The server combines these updates and sends a new improved model back to the devices.

This cycle repeats for several rounds, resulting in a model that has "learned" from all the devices without accessing their private data.

---

## **Key Pieces of the Project**

### 1. **Client-side Script (`client_app.py`)**

This part handles what happens on each client device.

- **Purpose:** Train the model using the client’s local data and send updates to the server.
- **How It Works:**
  - Each client:
    1. Loads a small piece (partition) of the MNIST dataset, which contains handwritten digit images.
    2. Trains the model on this data using a pre-defined training process.
    3. Evaluates how well the model performs on a separate test dataset.
    4. Sends the updated model and its performance results to the server.
- **Key Features:**
  - The `FlowerClient` class ensures that training and evaluation processes are consistent across all devices.
  - The `client_fn` function dynamically sets up clients, making the system scalable to multiple devices.

---

### 2. **Server-side Script (`server_app.py`)**

This part manages the "brain" of the system, coordinating all the devices.

- **Purpose:** Combine updates from all the clients, improve the model, and send it back to the clients for the next round of training.
- **How It Works:**
  - Initializes a global model (a CNN).
  - Uses a strategy called **Federated Averaging (FedAvg)** to combine updates from clients. This strategy gives more weight to updates from clients with larger datasets.
  - Runs several rounds of communication between the server and the clients until the model is well-trained.
  - Aggregates performance metrics (like accuracy) to measure overall model success.

- **Key Features:**
  - Flexible configuration: You can set the number of training rounds and how much data each client contributes.
  - Uses a weighted average to calculate accuracy, ensuring fairness across devices.

---

### 3. **Machine Learning Logic (`task.py`)**

This part contains all the core machine learning functionality, like defining the model and training process.

- **What’s Inside:**
  1. **The Model:** A simple Convolutional Neural Network (CNN) that learns to classify MNIST images (handwritten digits).
     - Think of the model as a machine that looks at an image and guesses what digit it represents.
  2. **Training Logic:** 
     - Gradually improves the model by comparing its predictions to the correct answers and making small adjustments.
     - These adjustments are called **gradients** and are applied to make the model more accurate.
  3. **Data Preparation:**
     - Loads and splits the MNIST dataset into smaller pieces for each client.
     - Prepares the data for training by normalising it and converting it into a format that the model understands.

- **Key Features:**
  - JAX is used for high-speed computation, making training faster.
  - FederatedDataset library is used to handle data distribution and ensure that each client gets a fair share of the dataset.

---

## **How It All Works Together**

1. **Server Setup:** 
   - The server creates a global model and sends it to all the clients.
   - It also defines a strategy to combine updates from clients.

2. **Clients Train Locally:**
   - Each client trains the model on its local data and calculates performance metrics (e.g., accuracy).
   - Updates are sent back to the server.

3. **Server Aggregates Updates:**
   - The server combines updates from all the clients using the FedAvg strategy.
   - The improved model is sent back to the clients for the next round.

4. **Repeat:**
   - This process continues for several rounds until the model achieves good performance.

---

## **Why Federated Learning?**

- **Better Privacy:** Data stays on the client devices, reducing privacy risks.
- **Scalability:** Allows training on data from many devices without requiring a centralised dataset.
- **Fairness:** Combines insights from all clients, even if some have less data.

---

## **What You Can Do With This Project**

- Learn how federated learning works in practice.
- Experiment with modifying the model or training process.
- Apply the same ideas to other datasets or real-world applications (e.g., healthcare or finance).

---

## **Next Steps and Improvements**

- **Advanced Privacy:** Add mechanisms like differential privacy to further protect user data.
- **Real-world Applications:** Test the system on other datasets or use cases.
- **Decentralised Training:** Extend the project to support fully decentralised systems without a central server.

---

This project is a hands-on example of how federated learning can be implemented using modern tools like Flower and JAX, making it a great starting point for privacy-preserving AI development.
