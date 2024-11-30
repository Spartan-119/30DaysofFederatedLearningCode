# Day 11: Set up the environment to simulate FL over multiple clients.

### Leveraging Open-Source Code
Using open-source code made it much easier to build the federated learning simulation. The transparency and collaborative nature of open-source contributions helped us understand the core ideas and adapt the simulation to our specific needs.

---

## Step 1: Setting up the Environment

### Key Tools Used:
1. **PyTorch**:
   - **Why I used it**: It's a powerful machine learning framework, and its flexibility fits well with federated learning.
   - **Why it works**: PyTorch's dynamic computation graph and ease of use made it a great choice for our project.

2. **Flower Library**:
   - **Purpose**: This is the backbone of our federated learning pipeline.
   - **Why it's important**: Flower lets you easily manage and simulate distributed learning tasks.

3. **Ray**:
   - **Purpose**: Handles running multiple virtual clients for the simulation.
   - **Why it's helpful**: Ray makes it simple to manage parallel tasks and optimise resources during simulation.

4. **Hydra**:
   - **Purpose**: A tool for managing configurations.
   - **Why I used it**: Hydra makes it easy to tweak settings like client models and learning strategies without touching the code.

### What I Did:
I set up a Python virtual environment (`flower_venv`) and installed these tools. This gave me a solid foundation to start building the federated learning pipeline.

---

## Step 2: Preparing the Dataset

### Tackling Non-IID Data:
In real-world federated learning, data isn't equally distributed (non-IID), which can make learning harder. To simplify things:
- I used IID (Independent and Identically Distributed) data for our simulation. This means every client got data from all classes.
- Why? It’s easier to set up and still gives us a good starting point to test federated learning concepts.

### Key Points:
- Each client gets a fair share of data, with batches of the same size.
- The test dataset stays the same for all clients, so I can evaluate the global model accurately after each training round.

---

## Dataset Preparation Code
Here’s a quick overview of the two main functions I used in our code:

### `download_mnist_dataset`
- **What it does**: Downloads the MNIST dataset and applies basic transformations like normalization.
- **Why it's important**: Prepares the data in a way that works well with federated learning.

### `prepare_federated_dataset`
- **What it does**:
  1. Splits the MNIST data into equal parts for each client (IID partitions).
  2. Creates training and validation datasets for every client.
  3. Leaves the test dataset intact for evaluating the global model.
- **Why it's important**: It ensures every client gets its own dataset, which is key for federated learning.

Here’s an example of how I prepared the data:

```python
def prepare_federated_dataset(num_partitions: int, batch_size: int, val_ratio: float = 0.1):
    # Download and split MNIST data
    trainset, testset = download_mnist_dataset()
    partition_len = [len(trainset) // num_partitions] * num_partitions
    trainsets = random_split(trainset, partition_len, generator=torch.Generator().manual_seed(2275285))

    trainloaders, valloaders = [], []
    for trainset in trainsets:
        num_val = int(val_ratio * len(trainset))
        for_train, for_val = random_split(trainset, [len(trainset) - num_val, num_val])
        trainloaders.append(DataLoader(for_train, batch_size=batch_size, shuffle=True))
        valloaders.append(DataLoader(for_val, batch_size=batch_size, shuffle=False))

    testloader = DataLoader(testset, batch_size=128)
    return trainloaders, valloaders, testloader
