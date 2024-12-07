# Day 17: 🚀 JAX Meets Flower: Federated Learning Awesomeness 🌸

Hey there, 

So, I dove into this fantastic journey of combining **JAX** (Google’s crazy fast ML library) with **Flower** (the friendly federated learning framework), and I can’t wait to share what I’ve learned. Here's the lowdown, in my own words, on how I tackled this and what blew my mind along the way.

---

## 🌟 What’s JAX?

JAX is like NumPy on steroids! It’s built by Google and is super popular because it makes running ML computations on GPUs and TPUs ridiculously easy. Imagine doing vectorisation with `map()`, just-in-time compilation with `jit()`, and differentiation with `grad()`—yeah, it’s that cool. DeepMind is all over this, and now I see why.

---

## 🌸 Why Flower?

Flower is all about **federated learning**—a collaborative approach where multiple devices train a model together without sharing their data (hello, privacy!). And combining it with JAX? Mind-blown. It’s like giving researchers the ultimate toolkit to create federated learning setups with whatever framework they’re comfy with. 

---

## 🛠️ What I plan to Build?

I will start by whipping up a simple **linear regression model** in JAX. It’s a basic setup: 

- Load some regression data (thanks, scikit-learn!).  
- Define a model.  
- Train and evaluate it.  
- Print the results.  

Oh, and the JAX magic? It uses `DeviceArray` for parameters, which had to be converted to good ol' NumPy arrays to play nice with Flower. Small tweak, big win.

Here’s the kicker: I went from a **centralised ML setup** to a **federated setup** by plugging this into Flower. It’s surprisingly smooth once you wrap your head around the process.

---

## 🌍 Federated Learning 101 

In federated learning:  

1. The server sends a global model to clients.  
2. Clients train locally (no data sharing, yay privacy!).  
3. They send back updates.  
4. The server aggregates the updates and sends out a better global model.  

Flower handles this whole orchestration beautifully. By default, it uses the **FedAvg** strategy to average client updates. Pretty neat, right?

---

## 🧠 Key Takeaways

- **Local Training**: Each client trains the model with its data. I reused the JAX training code here.  
- **Parameter Conversion**: JAX uses `DeviceArray`, but Flower loves NumPy. A quick conversion with `np.array()` solved that.  
- **Federation Magic**: Flower's `NumPyClient` connects my local JAX models to the federated setup. It was just a matter of implementing the `get_parameters()`, `set_parameters()`, `fit()`, and `evaluate()` methods.

---

## Next, I will try to get my hands dirty
