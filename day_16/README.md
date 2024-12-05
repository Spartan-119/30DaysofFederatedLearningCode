# Day 16

# Today I Explored Federated Learning Outcomes from day 14

### Promising Results from the Simulation

Day 14 shows the potential of federated learning through significant improvements in the global model's performance. The accuracy increased remarkably, while loss decreased, highlighting the effectiveness of this collaborative learning approach across distributed data sources.

#### Key Highlights:
- **YAML Configuration File**  
  The simulation starts by outputting a YAML configuration file, providing a clear, structured view of the simulation settings. This ensures easy review and modification.

- **Resource Allocation**  
  The Flower framework initiates the virtual client engine, managing resources like GPUs, CPUs, and memory. This setup accurately mimics a distributed environment, ensuring smooth execution.

- **Initial Model Evaluation**  
  Flower begins by randomly sampling a client to initialize the global model's parameters. A preliminary evaluation with another randomly initialized model sets the baseline at ~9.8% accuracy—close to a random guess for 10 classes.

- **Federated Learning Process Begins**  
  The first round involves sampling 10 out of 100 clients for local training. After training, clients send updates back to the server for aggregation. The global accuracy jumps to ~37% after this first round, completed in just 19 seconds.

- **Final Results**  
  After 10 rounds, the global accuracy soars to an impressive **95.02%**, demonstrating the power of federated learning.

---

### Limitations of my simulation of FL

Despite the successes, there are important limitations to consider:

1. **IID Data Assumptions**  
   The simulation uses Independent and Identically Distributed (IID) data by dividing the MNIST dataset uniformly among all clients. This creates a near-identical data distribution, which doesn't reflect real-world scenarios.

2. **Non-IID Data Challenges**  
   In real federated networks, clients often have vastly different datasets (non-IID). Such diversity introduces complexities that this IID-focused simulation doesn't address.

#### Implications:  
While this FL simulation demonstrates excellent accuracy under controlled conditions, real-world federated learning environments demand further research to handle the heterogeneity of data effectively.

---

