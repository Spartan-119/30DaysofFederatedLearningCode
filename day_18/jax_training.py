from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

# Generate synthetic regression data
X, y = make_regression(n_features=3)
X, X_test, y, y_test = train_test_split(X, y)

# Ensure all data is of type float32 (required for JAX operations)
X = jnp.array(X, dtype=jnp.float32)
X_test = jnp.array(X_test, dtype=jnp.float32)
y = jnp.array(y, dtype=jnp.float32)
y_test = jnp.array(y_test, dtype=jnp.float32)

print(X.shape)

import jax
import jax.numpy as jnp

# Initialize parameters with floating-point values
params = {
    'w': jnp.zeros(X.shape[1:], dtype=jnp.float32),
    'b': jnp.float32(0)
}

def forward(params, X):
    return jnp.dot(X, params['w']) + params['b']

@jax.jit
def loss_fn(params, X, y):
    error = forward(params, X) - y  # prediction - ground truth
    return jnp.mean(jnp.square(error))  # mse

grad_fn = jax.grad(loss_fn)

# Compute loss and gradients
print(loss_fn(params, X_test, y_test))
print(grad_fn(params, X_test, y_test))

for _ in range(50):
    loss = loss_fn(params, X_test, y_test)
    print(loss)

    grads = grad_fn(params, X_test, y_test)
    # params['w'] -= 0.05 * grads['w']
    # params['b'] -= 0.05 * grads['b']
    params = jax.tree_map(
        lambda p, g: p - 0.05 * g,
        params,
        grads,
    )