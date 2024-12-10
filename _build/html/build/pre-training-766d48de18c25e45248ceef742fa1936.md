
# Pre-Training

## Definition


## Tags
Pre-training

## Additional Notes
This is the “PT” in “GPT”, and it was one of the breakthroughs in the og GPT paper 

Distribution matching occurs in this phase; This is where the model is trained on bulk internet data. The model learns how to predict the next token by minimising the loss between P(predicted-token|context) and P(actual-token|context). 

A concrete example of there this occurs is in the 

This concept was introduced in the 

Pre-training effectively cuts down on this upper limit by making it more likely that the model will predict coherent sentences, which means that it will converge on correct behaviour orders of magnitude faster.

