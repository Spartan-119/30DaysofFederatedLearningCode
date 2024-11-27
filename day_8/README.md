# Day 8 
## Today, I took a step back and polished my grip on `FedAvg` algo. Here goes nothign:

# Federated Averaging and Federated Learning Challenges

Federated Averaging (FedAvg), introduced by H. Brendan McMahan and team in 2017, is one of the most popular algorithms in federated learning. It allows machine learning models to be trained across multiple data owners without sharing raw data, ensuring privacy while promoting collaborative learning. Here's a quick breakdown of how it works:

## How FedAvg Works

1. **Global Model Setup**  
   The central server (referred to as the *server*) starts by creating a global model that acts as the foundation for training.

2. **Choosing Clients**  
   The server randomly selects some data owners (*clients*) to participate in a training round. This ensures diverse and representative input.

3. **Sharing the Model**  
   The server sends the global model to the selected clients. Each client then uses this model as a starting point.

4. **Local Training**  
   Clients train the model locally using their own data, preserving privacy throughout the process.

5. **Aggregation**  
   Once clients complete their updates, they send the new model parameters back to the server. The server averages these updates to improve the global model.

6. **Repeat**  
   Steps 2–5 are repeated until a stopping condition is met, like a set number of rounds or reaching a certain level of accuracy.

FedAvg improves on traditional algorithms like Stochastic Gradient Descent (SGD) by reducing the number of required training rounds while addressing some key privacy and decentralisation challenges.

---

## Key Features of FedAvg

- It builds on a simpler baseline called Federated SGD (FedSGD), where all clients compute gradients and the server aggregates them. FedAvg tweaks this process by allowing clients to perform multiple local updates before sending results back.  
- FedAvg uses three main parameters:  
  - **C**: Fraction of clients participating in each round.  
  - **E**: Number of training passes over local data per round.  
  - **B**: Minibatch size for local training.

This combination enables significant performance improvements, especially when clients have sufficient computing power.

---

## Non-IID Data and Challenges in Federated Learning

A big challenge in federated learning is when the data across clients isn’t independent and identically distributed (non-IID). For example, if participants only provide data biased towards certain categories (e.g., one client has only dog images while another has cat images), the global model can struggle to generalise.

### Examples of Non-IID Issues:
- **Bias in Client Data**  
  If one client has mostly cat images and another has only dog images, the model may lose important patterns during aggregation.  

- **Accuracy Drops**  
  Studies show that non-IID data can significantly reduce the accuracy of federated models. For example, using CIFAR-10 for image classification, models trained on IID data outperform those trained on non-IID data by a noticeable margin.

---

### Addressing Non-IID Data

1. **Data Sharing Strategy**  
   - Introduce a small globally shared dataset that all clients use alongside their private data.  
   - Research by Zhao et al. (2018) shows that sharing just 5% of data can improve accuracy by up to 30%.

2. **Other Approaches**  
   - **Knowledge Distillation**: Sharing general knowledge instead of raw data.  
   - **Personalised Federated Learning**: Tailoring models to individual clients.

While these methods can help, they may introduce privacy concerns or be challenging to scale.

---

## Research Directions

Federated learning still has room for improvement, especially in areas like:
- Handling extreme non-IID cases.  
- Reducing communication costs in networks with limited bandwidth.  
- Personalised federated learning for edge devices (like IoT).  
- Exploring vertical federated learning for overlapping data features.  

### Why This Matters for Federated Learning  
Balancing privacy, efficiency, and performance is key to federated learning’s success. While current solutions address some non-IID challenges, many questions remain unanswered, especially regarding privacy risks and scalability.

---

## A Practical Implementation

For this project, the MNIST dataset (distributed in an IID manner) was used to explore the feasibility of federated learning in a collaborative framework. While most real-world federated data is non-IID, using IID data simplifies the prototype, allowing for a more controlled exploration of the federated learning process.

