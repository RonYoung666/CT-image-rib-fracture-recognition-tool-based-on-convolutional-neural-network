![interface](https://github.com/RonYoung666/CTRibFractureRecognition/blob/master/interface.png)
# CT Rib fracture recognition tool based on CNN
# 基于卷积神经网络的肋骨骨折识别工具

It's a tool that can recognize rib fracture in CT image (DICOM file), you can use it as follow:

1. Detect rib fractures in CT images.
2. Replace the CNN part with your own CNN to detect target objects in other CT images.
3. Replace the input part and the CNN part to detect target object in regular image.


## Table of Contents

- [Install](#install)
- [Usage](#usage)
	- [Generator](#generator)
- [Badge](#badge)
- [Example Readmes](#example-readmes)
- [Related Efforts](#related-efforts)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)


## Install

This project uses the libraries below. Go check them out if you don't have them locally installed.

|Package              |Version
|-------------------- |-----------
|dicom                |0.9.9.post1
|lxml                 |4.3.4
|matplotlib           |3.1.3
|numpy                |1.16.4+mkl
|object-detection     |0.1
|opencv-python        |4.2.0.32
|pandas               |0.25.0
|Pillow               |5.4.1
|pydicom              |1.4.2
|PyQt5                |5.13.0
|tensorboard          |1.13.0
|tensorflow-estimator |1.13.0
|tensorflow-gpu       |1.13.2

## Usage

### Detect rib fractures in CT images
In Windows Command Prompt(cmd), input python appMain.py.
Click "打开", choose your DICOM directory.
Click "检测此CT

### Replace the CNN part with your own CNN to detect target objects in other CT images

### Replace the input part and the CNN part to detect target object in regular image

### Generator

To use the generator, look at [generator-standard-readme](https://github.com/RichardLitt/generator-standard-readme). There is a global executable to run the generator in that package, aliased as `standard-readme`.

## Badge

If your README is compliant with Standard-Readme and you're on GitHub, it would be great if you could add the badge. This allows people to link back to this Spec, and helps adoption of the README. The badge is **not required**.

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

To add in Markdown format, use this code:

```
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
```

## Example Readmes

To see how the specification has been applied, see the [example-readmes](example-readmes/).

## Related Efforts

- [Art of Readme](https://github.com/noffle/art-of-readme) - 💌 Learn the art of writing quality READMEs.
- [open-source-template](https://github.com/davidbgk/open-source-template/) - A README template to encourage open-source contributions.

## Maintainers

[@RichardLitt](https://github.com/RichardLitt).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/RichardLitt/standard-readme/issues/new) or submit PRs.

Standard Readme follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

### Contributors

This project exists thanks to all the people who contribute. 
<a href="graphs/contributors"><img src="https://opencollective.com/standard-readme/contributors.svg?width=890&button=false" /></a>


## License

[MIT](LICENSE) © Richard Littauer

