# day 27

Since we are approaching the end of the **#30DaysOfFLCode** challenge, I decided to take a step back and explore other venues of Federated Learning that I might have missed - after all, this is a vast ocean and I believe I have barely scratched the surface.

So, I came across something called `FedProx` algorithm.

## FedProx

`FedProx` is a federated optimisation method to tackle the challenges of **system and data heterogeneity**. You see, traditional `FedAvg` may perform poorly when clients have heterogeneous data distributions or differing computational capabilities. `FedProx` modifies the local objective function by adding a proximal term that penalises large deviations from the global model. This encourages local updates to stay closer to a common reference model, improving stability and convergence under non-IID and heterogeneous conditions.

### FedProx improves FedAvg by:
- Allowing devices to perform variable amounts of work (instead of forcing all to run the same number of updates).
- Adding a proximal term to control how far local updates stray from the global model.

---

### **How Does FedProx Work?**
At its core, FedProx tries to minimize a global objective function:

```math
f(w) = \sum_{k=1}^N p_k F_k(w)
```

Where:
- `f(w)`: The global loss across all devices.
- `F_k(w)`: The local loss for device `k`, based on its data.
- `p_k`: A weight proportional to how much data each device has.

#### Key Features:
1. **Variable Work**:
   - Devices with better resources do more work; those with constraints do less.
   - Instead of discarding updates from slower devices, FedProx aggregates even partial updates.

2. **Proximal Term**:
   - Devices solve a modified local problem:

```math
h_k(w; w_t) = F_k(w) + \frac{\mu}{2} \|w - w_t\|^2
```

   - `F_k(w)`: Original local objective (e.g., the loss from training on local data).
   - `\frac{\mu}{2} \|w - w_t\|^2`: A penalty term that discourages `w` (the device's local model) from drifting too far from `w_t` (the global model).

---

### **Why Add the Proximal Term?**
Without the penalty term, a device might overfit to its own data and stray too far from the global model. This happens especially when:
- Devices have very different data distributions.
- Devices run many local updates.

The proximal term acts like a leash:
- It keeps local updates closer to the global model.
- This improves stability and prevents the global model from diverging.

---

### **Mathematics in Simple Terms**
1. **The Local Problem**:
   Devices solve:

```math
h_k(w; w_t) = F_k(w) + \frac{\mu}{2} \|w - w_t\|^2
```

   - Think of `F_k(w)` as "minimizing your local loss."
   - The term `\frac{\mu}{2} \|w - w_t\|^2` acts as a "gentle pull" to ensure the solution stays close to the global model `w_t`.

2. **Inexact Solutions**:
   Devices don’t need to solve the local problem perfectly. Instead, they aim for an **approximate solution**:

```math
\| \nabla h_k(w^*_k; w_t) \| \leq \gamma \| \nabla h_k(w_t; w_t) \|
```

   - `w^*_k`: The approximate solution found by the device.
   - `\gamma`: A measure of how "inexact" the solution is (smaller `\gamma` means closer to the true solution).
   - Devices can stop early if resources are limited, ensuring flexibility.

3. **Global Aggregation**:
   After local updates, devices send their models to the server. The server computes the new global model:

```math
w_{t+1} = \frac{1}{K} \sum_{k \in S_t} w_k
```

   - `S_t`: The set of devices participating in this round.
   - `w_k`: The updated model from device `k`.

4. **Benefits of `\mu`**:
   - `\mu` controls the strength of the leash (proximal term).
   - A larger `\mu` keeps updates closer to the global model, improving stability in highly heterogeneous settings.

---

### **How FedProx Solves Problems**
1. **Statistical Heterogeneity**:
   - The proximal term ensures that even with different data, local updates don’t deviate too much from the global model.

2. **Systems Heterogeneity**:
   - Devices that can’t complete full updates still contribute partially, instead of being excluded entirely.

---

### **Analogy**
Imagine a group project where:
- Everyone has different workloads and skill levels.
- The group leader (server) gathers everyone’s contributions to create the final presentation (global model).
- FedProx is like giving team members guidelines:
  - “Stick to the main topic” (proximal term).
  - “It’s okay if you can’t finish all your tasks, just send what you can” (partial work).

---
