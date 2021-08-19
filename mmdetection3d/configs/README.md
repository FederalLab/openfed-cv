# PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space

## Introduction

<!-- [ALGORITHM] -->

We implement PointNet++ and provide the result and checkpoints on ScanNet and S3DIS datasets.

```
@inproceedings{qi2017pointnet++,
  title={PointNet++ deep hierarchical feature learning on point sets in a metric space},
  author={Qi, Charles R and Yi, Li and Su, Hao and Guibas, Leonidas J},
  booktitle={Proceedings of the 31st International Conference on Neural Information Processing Systems},
  pages={5105--5114},
  year={2017}
}
```

**Notice**: The original PointNet++ paper used step learning rate schedule. We discovered that cosine schedule achieves much better results and adopt it in our implementations. We also use a larger `weight_decay` factor because we find it consistently improves the performance.

## Results

### S3DIS

|                                   Method                                    | Split  |  Lr schd   | Mem (GB) | Inf time (fps) | mIoU (Val set) |         Download         |
| :-------------------------------------------------------------------------: | :----: | :--------: | :------: | :------------: | :------------: | :----------------------: |
| [PointNet++ (SSG)](./pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class.py) | Area_5 | cosine 50e |   3.6    |                |     56.93      | [model](https://download.openmmlab.com/mmdetection3d/v0.1.0_models/pointnet2/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class_20210514_144205-995d0119.pth) &#124; [log](https://download.openmmlab.com/mmdetection3d/v0.1.0_models/pointnet2/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class_20210514_144205.log.json) |

**Notes:**

- We use XYZ+Color+Normalized_XYZ as input in all the experiments on S3DIS datasets.
- `Area_5` Split means training the model on Area_1, 2, 3, 4, 6 and testing on Area_5.

## Indeterminism

Since PointNet++ testing adopts sliding patch inference which involves random point sampling, and the test script uses fixed random seeds while the random seeds of validation in training are not fixed, the test results may be slightly different from the results reported above.
