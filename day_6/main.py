import os
from pathlib import Path
import json
from syftbox.lib import Client, SyftPermission
import diffprivlib.tools as dp
import time
import psutil
from statistics import mean
from datetime import datetime, UTC

API_NAME = "cpu_tracker_member"
AGGREGATOR_DATASITE = "aggregator@openmined.org"

def get_cpu_usage_samples():
    """
    Collect 50 CPU usage samples over time intervals of 0.1 seconds.

    The function collects CPU usage data using the `psutil` library. The collected samples are returned as a list of CPU usage percentages.

    Returns:
        list: A list containing 50 CPU usage values.
    """
    cpu_usage_values = []

    # Collect 50 CPU usage samples with a 0.1-second interval between each sample
    while len(cpu_usage_values) < 50:
        cpu_usage = psutil.cpu_percent()
        cpu_usage_values.append(cpu_usage)
        time.sleep(0.1)

    return cpu_usage_values


def create_restricted_public_folder(cpu_tracker_path: Path) -> None:
    """
    Create an output folder for CPU tracker data within the specified path.

    This function creates a directory structure for storing CPU tracker data under `api_data/cpu_tracker`. If the directory
    already exists, it will not be recreated. Additionally, default permissions for accessing the created folder are set using the
    `SyftPermission` mechanism to allow the data to be read by an aggregator.

    Args:
        path (Path): The base path where the output folder should be created.

    """
    os.makedirs(cpu_tracker_path, exist_ok=True)

    # Set default permissions for the created folder
    permissions = SyftPermission.datasite_default(email=client.email)
    permissions.read.append(AGGREGATOR_DATASITE)
    permissions.save(cpu_tracker_path)


def create_private_folder(path: Path) -> Path:
    """
    Create a private folder for CPU tracker data within the specified path.

    This function creates a directory structure for storing CPU tracker data under `private/cpu_tracker`.
    If the directory already exists, it will not be recreated. Additionally, default permissions for
    accessing the created folder are set using the `SyftPermission` mechanism, allowing the data to be
    accessible only by the owner's email.

    Args:
        path (Path): The base path where the output folder should be created.

    Returns:
        Path: The path to the created `cpu_tracker` directory.
    """
    cpu_tracker_path: Path = path / "private" / "cpu_tracker"
    os.makedirs(cpu_tracker_path, exist_ok=True)

    # Set default permissions for the created folder
    permissions = SyftPermission.datasite_default(email=client.email)
    permissions.save(cpu_tracker_path)

    return cpu_tracker_path


def save(path: str, cpu_usage: float):
    """
    Save the CPU usage and current timestamp to a JSON file.

    This function records the current CPU usage percentage and the timestamp of when the data was recorded.
    It then writes this information into a JSON file at the specified file path.

    Parameters:
        path (str): The file path where the JSON data should be saved.
        cpu_usage (float): The current CPU usage percentage.

    The JSON output will have the following format:
    {
        "cpu": <cpu_usage>,
        "timestamp": "YYYY-MM-DD HH:MM:SS"
    }

    Example:
        save("datasites/user/api_data/cpu_tracker/cpu_data.json", 75.4)
    """
    current_time = datetime.now(UTC)
    timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    with open(path, "w") as json_file:
        json.dump(
            {"cpu": cpu_usage, "timestamp": timestamp_str},
            json_file,
            indent=4,
        )


def should_run() -> bool:
    INTERVAL = 20  # 20 seconds
    timestamp_file = f"./script_timestamps/{API_NAME}_last_run"
    os.makedirs(os.path.dirname(timestamp_file), exist_ok=True)
    now = datetime.now().timestamp()
    time_diff = INTERVAL  # default to running if no file exists
    if os.path.exists(timestamp_file):
        try:
            with open(timestamp_file, "r") as f:
                last_run = int(f.read().strip())
                time_diff = now - last_run
        except (FileNotFoundError, ValueError):
            print(f"Unable to read timestamp file: {timestamp_file}")
    if time_diff >= INTERVAL:
        with open(timestamp_file, "w") as f:
            f.write(f"{int(now)}")
        return True
    return False
   

if __name__ == "__main__":
    if not should_run():
        print(f"Skipping {API_NAME}, not enough time has passed.")
        exit(0)

    client = Client.load()

    # Create an output file with proper read permissions
    restricted_public_folder = client.api_data("cpu_tracker")
    create_restricted_public_folder(restricted_public_folder)

    # Create private private folder
    private_folder = create_private_folder(client.datasite_path)

    # Get cpu usage mean with differential privacy in it.
    cpu_usage_samples = get_cpu_usage_samples()

    mean = mean(cpu_usage_samples)

    mean_with_noise = round(  # type: ignore
        dp.mean(  # type: ignore
            cpu_usage_samples,
            epsilon=0.5,  # Privacy parameter controlling the level of differential privacy
            bounds=(0, 100),  # Assumed bounds for CPU usage percentage (0-100%)
        ),
        2,  # Round to 2 decimal places
    )

    # Saving Mean with Noise added in it.
    public_mean_file: Path = restricted_public_folder / "cpu_tracker.json"
    save(path=str(public_mean_file), cpu_usage=mean_with_noise)

    # Saving the actual private mean.
    private_mean_file: Path = private_folder / "cpu_tracker.json"
    save(path=str(private_mean_file), cpu_usage=mean)
