# Residual Stream

## Definition
The residual stream is a core concept in transformer architectures, referring to the main pathway through which information flows across layers. It maintains a persistent representation that each sublayer (self-attention and feed-forward network) modifies via residual connections. The residual stream allows for better gradient flow during training and helps maintain information from earlier layers throughout the network depth. Each sublayer processes the stream and adds its output back to it, rather than completely transforming it.

## Tags
Transformers, Architecture, Deep Learning, Residual Connections

## References
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention Is All You Need. https://doi.org/10.48550/arXiv.1706.03762
- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. https://doi.org/10.48550/arXiv.1512.03385