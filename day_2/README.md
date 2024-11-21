# day 2

i decided to start with implementing the FedAvg strategy. While i understand the theory behind it, i guess implementing it is more difficult than what I initially anticipated. so prolly this work will overflow to day 3 as well.

# Federated Averaging (FedAvg) in Federated Learning

## What is the FedAvg Strategy?

**FedAvg**, short for Federated Averaging, is a simple way to combine the work done by multiple devices into a single improved model. Here's how it works:

### 1. **Start with a Global Model**
   - The central server begins with a starting model (it could be random or pre-trained).

### 2. **Train Locally on Devices**
   - Each device downloads the global model and trains it using its own local data (e.g., your texts, photos, or app usage).
   - No data leaves the device—only the model gets smarter locally.

### 3. **Share Updates, Not Data**
   - Once local training is done, each device sends **model updates** (the changes it made during training) back to the central server.
   - These updates are numbers that describe how to improve the model—not your actual data.

### 4. **Combine Using a Weighted Average**
   - The server combines all updates using a **weighted average**:
     - Devices with more data have a bigger influence on the updated global model.
     - For example, a phone with 10,000 text messages contributes more than a phone with only 500 messages.

### 5. **Update the Global Model**
   - The server applies the combined updates to the global model.
   - The updated model is then sent back to all devices, starting a new round of training.

---

## Why is FedAvg Important?

- **Preserves Privacy**: No raw data is shared—only updates to the model.
- **Efficient**: Devices with more data contribute more, leading to faster and better training.
- **Scalable**: Works with thousands or even millions of devices.

---
