# fast.ai: Decrappification, DeOldification, and Super Resolution

## The genesis of decrappify

- [Transfer learning technique for generative modeling](https://course.fast.ai/videos/?lesson=7) (interesting): start with an image dataset and "crappify" (英解: To reduce the quality of; to make unfavorable) the images. Then train a model to "decrappify" those images to return them to their original state.
- Specifically, fast.ai started with `a model that was pre-trained for ImageNet classification`, and added a `U-Net unsampling network`, adding various `modern tweaks` to the regular U-Net. A simple fast loss function was initially used: `mean squared pixel error`. (This U-Net could be trained in just a few minutes)  Then the loss function was replaced was `a combination of other loss functions` used in the generative modeling literature and trained for another couple of hours. The plan was then finally add a GAN for the last few epochs.

## The genesis of DeOldify

- Jason Antic started with the images in the ImageNet dataset, `converted them into b&w`, and then `added random contrast, brightness, and other changes`.
- Jason moved to movies, and discovered that just a tiny bit of GAN fine-tuning on top of the process developed with fast.ai could create colorized movies in just a couple of hours, at a quality beyond any automated process that has been built before.

## The genesis of microscopy super-resolution

- Improve the `resolution, speed, and signal-to-noise` of the images.
- Using carefully acquired high resolution images for training, the group validated "generalized" models for super-resolution processing of electron and fluorescence microscope images (电子和荧光显微镜图像), enabling faster imaging with higher throughout, lower sample damage, and smaller file sizes than ever reported.
- Since the models are able to restore images acquired on relatively low-cost microscopes, this model also presents an opportunity to "democratize" (民主化?) high resolution imaging to those not working at elite institutions that can afford the latest cutting edge instrumentation. (用低分辨率的图片得到高分辨率的图像, 减轻小机构的负担, 但是结果可信吗?)

## The Design of DeOldify

### Self-Attention

- Motivation:

  - > Traditional convolutional GANs generate high-resolution details as a function of only spatially local points in lower-resolution feature maps. In SAGAN, details can be generated using cues from all features locations. Moreover, the discriminator can check that highly detailed features in distant portions of the image are consistent with each other.

### Reliable Feature Detection

- DeOldify uses custom U-Nets with pretrained `resnet backbones` for each of its generator models. There are based on fastat's well-designed `DynamicUnet`, with a few minor modifications.
- The deviations from standard U-Nets include `self-attention` as well as `the addition of spectral normalizaion`
- The "video" and "stable" models use a `resnet101 backbone` and the decoder side `emphasizes width (number of filters) over depth (number of layer)`. This configuration has proven to support the most stable and reliable renderings seen so far.
- The "artistic" model has a `resnet34 backbone` and the decoder side `emphasizes depth over width`. The configuration is great for creating interesting colorization and high detailed renders, but at the cost of being more inconsistent in rendering than the "stable" and "video" models.
- The U-Net architecture, especially fastai's DynamicUnet, is simply superior in image generation applications. This is due to the key detail `preserving and enhancing features like cross connections from encoder to decoder`, `learnable blur`, and `pixel shuffle`.
- The resnet backbone itself is well-suited for the task of scene feature recognition.
- To further encourage robustness in dealing with old and low quality images and film, we train with fairly extreme `brightness and contrast augmentations`
- We also employed `gaussian noise augmentation` in video model training in order to reduce model sensitivity to meaningless noise (grain) in film.

### NoGAN Training

- Process:
  - Pretrain the generator.
    - The generator is first trained in a more conventional and easier to control manner, with `Perceptual Loss` (aka `Feature Loss`) by itself.
    - Train the generator as best as you can in the easiest way possible.
    - This takes up most of the time in NoGAN training.
  - Save generated images from pretrained generator.
  - Pretrain the Critic a a Binary Classifier.
    - Train the critic as a binary classifier of real and fake images, with the fake images being those saved in the previous step.
    - You can simply use `a pre-trained critic used for another image-to-image task` and refine it. This has already been done for super-resolution.
  - Train generator and critic in (almost) normal GAN setting
    - It turns out that in this pretraining scenario, the critic will rapidly drive adjustments in the generator during GAN training.
- 30-90 minutes of NoGAN training VS 3-5 days of progressively-sized GAN training.
- NoGAN training makes up the entirety of GAN training for the video model. The "artistic" and "stable" models go one step further and repeat the NoGAN training process steps 2-4 until there's no more apparent benefit.
- A `loss threshold` is used in NoGAN training, which must be met by the critic before generator training commences (开始). Until then, the critic continues training to "catch up" in order to be able to provide the generator with constructive (建设性的) gradients.
- `Inflection point`: after the point, artifacts and incorrect colorization start to be introduced.
- Questions for NoGAN training:
  1. The technique seems to accommodate (容纳, 适应) small batch sizes well.
  2. How broadly applicable the approach is.
  3. The best practices for NoGAN training haven't yet been fully explored.

## How stable video is Achieved

- The problem - A Flickering (闪烁) Mess
- The DeOldify Graveyard (墓地)
  - Wasserstein GAN and its variants
  - Various other normalization schemes.
    - Spectral Normalization only in generator: this trained more slowly and was generally more unstable.
    - Batchnorm at output of generator: This slowed down training significantly and didn't seem to provide any real benefit.
    - Weight Normalization in generator: Ditto (同上) on the slowed training, and images didn't turn out looking as good either.
  - Other Loss Functions
  - Reduced Number of Model Parameters
