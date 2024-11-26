from pathlib import Path
import shutil
from syftbox.lib import Client
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import re
import json

API_NAME = "pretrained_model_aggregator"
TEST_DATASET_NAME = "mnist_dataset.pt"
SAMPLE_TEST_DATASET_PATH = Path("./samples/test_data") / TEST_DATASET_NAME


# Exception name to indicate the state cannot advance
# as there are some pre-requisites that are not met
class StateNotReady(Exception):
    pass


class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def get_app_private_data(client: Client, api_name: str) -> Path:
    """
    Returns the private data directory of the app
    """
    return client.workspace.data_dir / "private" / api_name


def init_aggregator(client: Client) -> None:
    """
    Creates the `pretrained_aggregator` api in the `api_data` folder
    with the following structure:

    api_data
    └── pretrained_aggregator
            └── launch
            └── running
            └── done
    """
    pretrained_aggregator = client.api_data(API_NAME)

    for folder in ["launch", "running", "done"]:
        pretrained_aggregator_folder = pretrained_aggregator / folder
        pretrained_aggregator_folder.mkdir(parents=True, exist_ok=True)

    # Create the private data directory for the app
    # This is where the private test data will be stored
    app_pvt_dir = get_app_private_data(client, API_NAME)
    app_pvt_dir.mkdir(parents=True, exist_ok=True)

    # Copy the test dataset to the private data directory
    test_dataset_path = app_pvt_dir / TEST_DATASET_NAME
    if not test_dataset_path.is_file():
        shutil.copy(SAMPLE_TEST_DATASET_PATH, test_dataset_path)


def launch_aggregator(client: Client) -> None:
    """
    Iterates over the launch folder and copies the participants.json file
    to the running folder

    We look for the participants.json file in the launch folder
    """
    launch_folder = client.api_data(API_NAME) / "launch"
    running_folder = client.api_data(API_NAME) / "running"

    participants_json = launch_folder / "participants.json"
    if participants_json.is_file():
        print("Copying participants.json to running folder")
        shutil.move(participants_json, running_folder)


def get_model_files(path: Path) -> list[Path]:
    return list(path.glob("pretrained_mnist_label_*.pt"))


def aggregate_models(client: Client) -> None:
    """
    Iterates over the running folder and tries to advance it
    It loads in the participants.json file and aggregates the models
    """
    running_folder = client.api_data(API_NAME) / "running"
    participants_json = running_folder / "participants.json"

    if not participants_json.is_file():
        raise StateNotReady("participants.json file not found in the running folder")

    with open(participants_json, "r") as f:
        participants = json.load(f)["participants"]

    model_output_path = running_folder / "global_model.pt"

    global_model = SimpleNN()
    global_model_state_dict = global_model.state_dict()

    aggregated_model_weights = {}

    n_peers = len(participants)
    aggregated_peers = []
    missing_peers = []
    for email in participants:
        their_public_folder: Path = client.datasites / email / "public"

        their_model_files: list[Path] = get_model_files(their_public_folder)
        if len(their_model_files) == 0:
            print(f"No models found for {email} in '{their_public_folder}'")
            missing_peers.append(email)
            continue

        for model_file in their_model_files:
            print(f"Aggregating model '{model_file.name} from {email}")
            model_file = their_public_folder / model_file
            user_model_state = torch.load(model_file, weights_only=True)
            for key in global_model_state_dict.keys():
                # If user model has a different architecture than my global model.
                # Skip it
                if user_model_state.keys() != global_model_state_dict.keys():
                    print(
                        f"Model {model_file.name} from {email} has an invalid architecture"
                    )
                    continue
                if aggregated_model_weights.get(key, None) is None:
                    aggregated_model_weights[key] = user_model_state[key] * (
                        1 / n_peers
                    )
                else:
                    aggregated_model_weights[key] += user_model_state[key] * (
                        1 / n_peers
                    )

            aggregated_peers.append(email)

    if not aggregated_model_weights:
        return (None, None)

    global_model.load_state_dict(aggregated_model_weights)
    torch.save(global_model.state_dict(), model_output_path)
    return (participants, missing_peers)


def calculate_model_accuracy(global_model_path: Path, dataset_path: Path) -> float:
    if not dataset_path.exists():
        print("No test dataset found. Skipping evaluation step and returning accuracy -1.")
        return -1

    model = SimpleNN()
    model.load_state_dict(torch.load(global_model_path, weights_only=True))
    model.eval()
    # load the saved mnist subset
    images, labels = torch.load(dataset_path, weights_only=True)
    # create a tensordataset
    dataset = TensorDataset(images, labels)
    # create a dataloader for the dataset
    data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in data_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    return accuracy


def evaluate_global_model(
    client: Client, participants: list[str] | None, missing_peers: list[str] | None
) -> None:
    if not participants:
        raise StateNotReady("No models aggregated. Skipping evaluation")

    running_folder = client.api_data(API_NAME) / "running"
    global_model_path = running_folder / "global_model.pt"
    if not global_model_path.is_file():
        raise StateNotReady(
            f"ERROR: global model path ({global_model_path}) does not exist"
        )

    # Evaluate the global model
    test_dataset_path: Path = get_app_private_data(client, API_NAME) / TEST_DATASET_NAME
    accuracy: float = calculate_model_accuracy(global_model_path, test_dataset_path)

    # Write the accuracy to an results.json file
    results = {
        "accuracy": accuracy,
        "participants": participants,
        "missing_peers": missing_peers,
    }

    print("Accuracy Results:", results)
    return results


def save_result(results: dict):
    running_folder = client.api_data(API_NAME) / "running"
    results_path = running_folder / "results.json"
    participants_json = running_folder / "participants.json"

    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)

    # If no missing peers, move the global model and results.json to the done folder
    done_folder = client.api_data(API_NAME) / "done"
    model_path = running_folder / "global_model.pt"
    if not missing_peers:
        shutil.move(participants_json, done_folder)
        shutil.move(model_path, done_folder)
        shutil.move(results_path, done_folder)


if __name__ == "__main__":
    client = Client.load()

    try:
        # Step 1: Init the Aggregator API
        init_aggregator(client)

        # Step 2: Launch the Aggregator
        # Iterates over the launch folder and looks for the participants.json file
        launch_aggregator(client)

        # Step 3: Aggregate the Models
        participants, missing_peers = aggregate_models(client)

        # Step 4: Evaluate model
        results = evaluate_global_model(client, participants, missing_peers)

        # Step 5: Save the results
        save_result(results)
    except StateNotReady as e:
        print(f"StateNotReady: {e}")
        exit(0)