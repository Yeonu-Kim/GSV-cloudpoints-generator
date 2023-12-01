# GSV-cloudpoints-generator
Generate cloudpoints from GSV panorama images. (refactoring from https://medium.com/@nocomputer/creating-point-clouds-with-google-street-view-185faad9d4ee)

Add monoDepth2 module to make depthmap (not using depth API)
https://github.com/nianticlabs/monodepth2
@article{monodepth2,
  title     = {Digging into Self-Supervised Monocular Depth Prediction},
  author    = {Cl{\'{e}}ment Godard and
               Oisin {Mac Aodha} and
               Michael Firman and
               Gabriel J. Brostow},
  booktitle = {The International Conference on Computer Vision (ICCV)},
  month = {October},
year = {2019}
}