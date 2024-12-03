# Step 4: Defining the Strategy and Architecting the Server

In the Flower framework, the central orchestrator of logic in a federated learning configuration is referred to as the **strategy**. This pivotal component is responsible for several key tasks:
- Sampling clients at the start of each round.
- Sending instructions and the global model to clients for local training.
- Guiding the training process overall.

For this application, the chosen strategy is **FedAvg** (Federated Average).

## Configuring the Server-Side Evaluation Function

The server's configuration includes defining how the global model is evaluated. This is critical for initiating the Federated Learning simulation. The Flower framework's strategy module is used to set up **FedAvg** with the following parameters:

### Key Parameters

1. **`fraction_fit`**:  
   - Set to a small value as not all clients may always be available.  
   - In this simulation, all clients are assumed available, allowing precise control using `min_fit_clients`.

2. **`min_fit_clients`**:  
   - Determines the number of clients sampled per round for training.  
   - Set to 10 clients per round in this simulation (`config.number_of_clients_per_round_fit`).

3. **`fraction_evaluate`**:  
   - Defines the fraction of clients sampled for evaluation.  
   - Similar logic applies as with `fraction_fit`.

4. **`min_evaluate_clients` and `min_available_clients`**:  
   - Derived from the configuration file and set to 25 and 100, respectively.  
   - Ensures that a quarter of the available clients are used to evaluate the global model after each round.

5. **Dynamic Configuration Parameters**:  
   - Functions like `on_fit_config_fn` and `evaluate_fn` are used to dynamically configure client and evaluation logic.

### Strategy Code

```python
# Define strategy
strategy = fl.server.strategy.FedAvg(
    fraction_fit=0.0,
    min_fit_clients=config.number_of_clients_per_round_fit,
    fraction_evaluate=0.0,
    min_evaluate_clients=config.number_of_clients_per_round_eval,
    min_available_clients=config.number_of_clients,
    on_fit_config_fn=prepare_configuration(config.configuration_fit),
    evaluate_fn=get_global_evaluation(config.number_of_classes, testloader),
)

### Implementing Dynamic Functions in `server.py`

The dynamic elements of the strategy configuration are implemented in a new file, `server.py`. These include:
1. The **on-fit configuration function**.
2. The **global evaluation function**.

---

## Code: Preparing Configuration

```python
from collections import OrderedDict
from omegaconf import DictConfig
import torch
from model import ConvolutionNeuralNet, test_model

def prepare_configuration(config: DictConfig):
    """
    Return function that prepares configuration to send to clients.

    Args:
        config: Configuration settings.

    Returns:
        Function to configure fit settings for clients during federated learning.
    """
    def fit_config_fn(server_round: int):
        """
        Configure fit settings for clients during federated learning.

        Args:
            server_round: Current round number in the federated learning process.

        Returns:
            Dictionary with fit configuration settings for clients.
        """
        # Adjust configuration dynamically based on server_round if needed
        return {
            "lr": config.learning_rate,
            "momentum": config.momentum,
            "local_epochs": config.local_epochs,
        }
    return fit_config_fn
```

# Code: Evaluating the Global Model

The evaluation function for the global model is implemented in the server to assess its performance on the test dataset. Below is the code and explanation.

---

## Code: Evaluation Function

```python
def evaluate_fn(server_round: int, parameters, config):
    """
    Evaluate the global model on the test dataset.

    Args:
        server_round: Current round number in the federated learning process.
        parameters: Parameters of the global model.
        config: Configuration settings.

    Returns:
        Tuple containing loss and a dictionary with evaluation metrics.
    """
    # Initialize model and device
    model = ConvolutionNeuralNet(config.number_of_classes)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Load parameters into the model
    params_dict = zip(model.state_dict().keys(), parameters)
    state_dict = OrderedDict({key: torch.Tensor(value) for key, value in params_dict})
    model.load_state_dict(state_dict, strict=True)

    # Evaluate the global model on the test set
    loss, accuracy = test_model(model, testloader, device)

    # Report the loss and metrics (e.g., accuracy)
    return loss, {"accuracy": accuracy}
```

## So ...
With the FedAvg strategy and server-side logic implemented, the Federated Learning simulation is now capable of:

Dynamically adjusting client configurations for each training round.
Effectively evaluating the global model using a subset of clients.
This marks the completion of the server's architecture setup for the simulation.
