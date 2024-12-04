# Machine Learning Concepts and Terminology

## Core Concepts

### Agents
- An agent is something that acts in an environment
- A rational agent maximizes expected value of performance measure based on experience and knowledge
- In software systems, agents use AI to perform tasks autonomously
- Key aspects: goals, complexity, agency, abstraction

### Neural Networks and Training

#### Neural Networks
Basic building blocks of modern machine learning
- Recommended resource: [3Blue1Brown Neural Networks series](https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)

#### Gradient Descent
Optimization algorithm for training neural networks
- Resource: [3Blue1Brown Gradient Descent explanation](https://www.youtube.com/watch?v=IHZwWFHWa-w)

#### Back-propagation
Algorithm for training neural networks by propagating errors backward
- Resource: [3Blue1Brown Back-propagation video](https://www.youtube.com/watch?v=Ilg3gGewQ5U)

### Model Architecture Components

#### Transformer Architecture
- Modern architecture for language models
- Resource: [3Blue1Brown Transformer explanation](https://www.youtube.com/watch?v=eMlx5fFNoYc)

#### Low Rank Adaptation (LoRA)
- Decomposes matrices into smaller, compute-friendly matrices
- Resource: [3Blue1Brown LoRA explanation](https://www.youtube.com/watch?v=PFDu9oVAE-g)

## Training Concepts

### Pre-training
- The "PT" in "GPT"
- Distribution matching phase
- Trains on bulk internet data
- Minimizes loss between predicted and actual token probabilities
- Essential for enabling efficient fine-tuning

### Fine-tuning
- Mode seeking phase
- Adapts pre-trained model for specific tasks
- Must balance between task performance and maintaining original distribution
- Risk of model collapse if overfit

### Reward Types

#### Sparse Reward
- Occurs less frequently compared to possible actions
- Common in fine-tuning scenarios
- Makes learning more challenging

#### Dense Reward
- Occurs more frequently
- Present in pre-training (every token prediction)
- Enables faster convergence with correct data

## Technical Terms

### Model Components
- Context window: Maximum input length the model can process
- Attention head: Component that processes relationships between tokens
- Feed-forward network: Neural network component processing individual positions
- Residual connections: Skip connections enabling better gradient flow

### Training Concepts
- Distributional shift: Changes in data distribution between training and deployment
- Model collapse: Loss of general capabilities due to overfitting
- Sample efficiency: Amount of data needed for effective learning
- Temperature: Parameter controlling randomness in generation

### Advanced Concepts
- Mono-semanticity vs Poly-semanticity: Single vs multiple meaning representations
- Latent space: Internal representation space of the model
- RAG (Retrieval Augmented Generation): Combining generation with external knowledge
- Tokenization: Converting text into model input tokens

### Mathematical Concepts
- Kaiming initialization: Weight initialization method using Gaussian distribution
- Linear representation hypothesis: Theory about concept representation in high dimensions
- Category theory: Mathematical framework for understanding model structure

## Optimization Methods
- PEFT (Parameter-Efficient Fine-Tuning)
- Top-K sampling
- Stochastic vs Deterministic processes
- Masked attention
- Self-attention vs Cross-attention

## Important Laws and Principles
- Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure"
- Important for understanding metrics and optimization in ML

## Learning Approaches
- Supervised learning
- Unsupervised learning
- Reinforcement learning