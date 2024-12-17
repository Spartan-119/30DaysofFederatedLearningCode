# Day 23: Simulating Federated Learning - Dataset Preparation

Building on **Day 22**'s plan, today I kicked off the journey of simulating **Federated Learning** on a healthcare dataset.

## Steps Completed 🚀

1. **Downloaded the Dataset**  
   - Retrieved the **Heart Disease UCI dataset** from Kaggle.  

2. **Dataset Splitting**  
   - Wrote the `create_dataset.py` script to split the dataset into multiple subsets.  
   - Each subset represents data for a simulated "client" (e.g., hospitals in a federated network).  
   - The number of clients is determined by the user.

### Bug Encountered 🐛

While splitting the data using `train_test_split`, I faced an issue:  
The `test_size` parameter in `train_test_split` cannot be `0.0`.  

- **What Happened?**  
  When `n_clients = 5`, on the last iteration, the `test_size` became:  

The error occurs because the `test_size` parameter in `train_test_split` cannot be `0.0`. When `n_clients` is `5`, on the last iteration of your loop, `test_size` becomes `1 - 1 / (n_clients - i)` → `1 - 1 / (5 - 4)` → `1 - 1/1 = 0.0`.


- **Solution:**  
Added a condition to handle the last client. Now the remaining data is directly assigned to the final client without further splitting.

## Next Steps ⏭️  

- Tomorrow, I will implement the `client.py` file.  
- This script will define how each client trains its respective dataset locally from the `data/` folder.  

---

### Project Status 📊

- **Dataset Splitting:** ✅  
- **Next Up:** Client Training Logic 🛠️  

Stay tuned for Day 24! 🎯
