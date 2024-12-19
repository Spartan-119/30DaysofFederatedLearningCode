import flwr 
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split as tts

# Loading the local dataset
def load_data(client_id: int):
    df = pd.read_csv(f"day_24/flwr_federated_health/data/client_{client_id}.csv")
    X = df.drop("num", axis=1)  # features
    y = df['num']  # target
    return tts(X, y, test_size=0.2, random_state=100)

class Client(flwr.client.NumPyClient):
    def __init__(self, client_id):
        self.client_id = client_id
        self.model = self.build_model()
        self.x_train, self.x_test, self.y_train, self.y_test = load_data(client_id)
    
    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(16, activation="relu", input_shape=(13, )),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        return model

    def get_parameters(self):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=1, batch_size=32, verbose=0)
        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        return loss, len(self.x_test), {"accuracy": accuracy}

# Starting the client
if __name__ == "__main__":
    import sys
    client_id = 1
    flwr.client.start_client(server_address="localhost:8080", client=Client(client_id).to_client())  # Use `to_client()` here
