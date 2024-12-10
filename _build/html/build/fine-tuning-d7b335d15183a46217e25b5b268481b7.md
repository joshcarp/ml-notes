
# Fine-Tuning

## Definition


## Tags
Fine-tuning

## Additional Notes
Mode seeking occurs in the “Fine-tuning” phase - Once the model has a distribution to work on, the model needs to be “fine-tuned”. Here the model will learn which parts of the distribution are useful and slightly diverge from the original distribution to make more “useful” behaviours more likely. It’s important to keep the distribution matching the original distribution to a certain extent. This can lead to model collapse where the model overfits on the fine-tuning examples and isn’t able to handle inputs that haven’t been fine-tuned because the rest of the distributions have been destroyed, negating the effect of pre-training.

