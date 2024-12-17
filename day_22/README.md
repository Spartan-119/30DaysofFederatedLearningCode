# Day 22

So, I took a week off for a convention. so was AFK for a while.

for the next few days, I intend to implement FedLearning while avoiding the overused MNIST dataset.

## Project overview

I will simulate FedLearning for a healthcare scenario where different hospitals want to collaboratively train a machine learning model to predict *heart disease risk* based on patient data. <br>

Since hospitals, or in this case *clients* cannot share their patient records to to privacy laws like the GDPR and HIPAA (in the US), fedlearning is a perfect fit here.

Each hospital has a slightly different dataset, and I'll use the **FedAvg** strategy to aggregate model updates on a central server.

## The idea

Hospitals A, B, C and so on, collaborate to train a logistic regression or small neural network to predict heart disease risk using anonymised data. the beauty here is that the **data never leaves the hospital**, only the model updates (or the gradients) are shared with the central server.

## Dataset

I will use the **Heart Disease UCI dataset** from Kaggle. I will split this dataset into smaller parts to simulate data from the hospitals (clients).

## What happens in the coming few days?

in the coming few days, I will implement this hypothetical situation in a federated network setting. The following will be the project structure

```
flwr_federated_health/
│
├── server.py                    # Central server to aggregate model updates
├── client.py                    # Federated clients (simulated hospitals)
├── create_dataset.py            # Script to split dataset into client-specific subsets
├── requirements.txt             # Dependencies (Flwr, TensorFlow, Pandas, etc.)
├── utils.py                     # Helper functions
├── data/
│   ├── full_dataset.csv         # Original heart disease dataset
│   ├── client_1.csv             # Hospital 1 data
│   ├── client_2.csv             # Hospital 2 data
│   └── ...                      # More client data files
└── README.md                    # Project explanation and usage
```