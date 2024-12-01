# Day 12: Takeaways and Learnings: Step 3 - Client and Model Setup

### What I Did:
- Built a federated learning client (`client.py`) for image classification tasks.
- Created a custom CNN (`model.py`) to process the data and perform training and evaluation.

---

### Key Highlights:
1. **Federated Learning Client (`client.py`)**:
   - Designed using the Flower framework.
   - Handles receiving and sending model parameters to/from the server.
   - Performs local training (`fit`) and evaluation (`evaluate`).
   - Checks for GPU availability to speed up computations.
   - Includes a handy `generate_client_function` to create multiple clients easily.

2. **Custom Neural Network (`model.py`)**:
   - A simple CNN for image classification (think MNIST-level tasks).
   - Includes convolutional layers, pooling, and fully connected layers.
   - Uses PyTorch's `train_model` and `test_model` functions for training and evaluation.

---

### Cool Things I Learned:
- **Parameter Handling**: Got to explore how a federated client sends and receives model weights during training rounds.
- **Training Workflow**: Learned how to set up a training loop that works locally on a client’s data.
- **Device Optimisation**: Code switches seamlessly between GPU (`cuda`) and CPU based on availability. Fancy stuff!

---

### Why This is Useful:
- Modular design makes the client super flexible — easy to adapt for different datasets or tasks.
- Enables smooth collaboration in federated learning — all clients train their own data locally and contribute to a global model. No raw data sharing!

---

### In a Nutshell:
Put together the brains (`model.py`) and the communicator (`client.py`) for a federated learning setup. Each client trains its local data, tests the results, and sends back the updates for a global model. 🚀
