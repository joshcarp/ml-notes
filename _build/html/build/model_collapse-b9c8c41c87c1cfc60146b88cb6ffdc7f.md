# Model Collapse

## Definition
Model collapse refers to a failure mode in training where a model converges to a degenerate state, producing limited or uniform outputs regardless of different inputs. This phenomenon is particularly common in generative models like GANs, where the generator might produce only a small subset of possible outputs, failing to capture the full diversity of the training distribution. In language models, it can manifest as repetitive or generic responses regardless of input prompts.

## Tags
Training, Failure modes, Optimization, GANs, Model behavior

## References
- Arjovsky, M., & Bottou, L. (2017). Towards Principled Methods for Training Generative Adversarial Networks. https://doi.org/10.48550/arXiv.1701.04862
- Srivastava, A., Valkov, L., Russell, C., Gutmann, M. U., & Sutton, C. (2017). VEEGAN: Reducing Mode Collapse in GANs using Implicit Variational Learning. https://doi.org/10.48550/arXiv.1705.07761