# ACWE
Active Contour Without Edges 

# Description
This is a simple implementation of the Active Contour Without Edges (ACWE) algorithm.

ACWE is a method for segmentation of images, which is based on the morphological reconstruction of the contour of the image.

# Usage
The algorithm is implemented in the `acwe` function.
It takes as arguments:
* `Img`: the input image
* `phi0`: the initial contour
* `max_Iter`: the maximum number of iterations
* `lambda1`: the weight of the first term of the data fidelity term
* `lambda2`: the weight of the second term of the data fidelity term
* `epsilon`: the accuracy of the iterative algorithm

To run the algorithm, you can use the `Active_Contour_Without_Edges` script with the `--path` option to specify the path to the `acwe` function and use default values for the other parameters.

As follow :
```bash
python Active_Contour_Without_Edges.py --path "image_path"
```

# References
[1] (Chan, T. F., et L. A. Vese. « Active contours without edges ». IEEE Transactions on Image Processing, vol. 10, no 2, février 2001, p. 266‑77. DOI.org (Crossref), https://doi.org/10.1109/83.902291.

