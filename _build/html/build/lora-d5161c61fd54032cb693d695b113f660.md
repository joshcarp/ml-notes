# LoRA (Low-Rank Adaptation)

## Definition
LoRA is a parameter-efficient fine-tuning technique that reduces the number of trainable parameters by representing weight updates through low-rank decomposition matrices. Instead of updating all weights in a neural network during fine-tuning, LoRA freezes the pretrained model weights and injects trainable rank decomposition matrices into each layer, significantly reducing memory requirements while maintaining model performance.

## Tags
Optimization, Training, Fine-tuning, Parameter-efficient training, Model adaptation

## References
- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., ... & Chen, W. (2021). LoRA: Low-Rank Adaptation of Large Language Models. https://doi.org/10.48550/arXiv.2106.09685