# VAE Explained

- If we save the encoded vector of an image, we can reconstruct it later by passing it into the decoder portion.
- We cannot generate anything yet, since we don't know how to create latent vectors other than encoding them from images.
- We add a constraint on the encoding network, that forces it to generate latent vectors that roughly follow a unit gaussian distribution. It is this **constraint** that separates a VAE from a standard one.
- In practice, there is a tradeoff between how accurate network can be and how close its latent variables can match unit gaussian distribution. We let the network decide this itself.
- For loss term, we sum up two separate losses: generative loss, and latent loss that is the KL divergence that measures how closely the latent variables match a unit gaussian.
- `Representation Trick`: instead of the encoder generating a vector of real values, ***it will generate a vector of means and a vector of standard deviations***.
- When decoding, sample from the standard deviations and add a mean, and use that as latent vector.
- To visualize, we can think of the latent variable as a transfer of data.
- The greater standard deviation on the noise added, the less information we can pass using that one variable. (???)
- The more efficiently we can encode source, the higher we can raise the standard deviation on gaussian until it reaches one. (???)
- The constraint forces the encoder to be very efficient, creating information-rich latent variables. This improves generalization, so latent variables that either randomly generated, or got from encoding non-training images, will produce a nicer result when decoded.