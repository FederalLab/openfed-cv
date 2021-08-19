# OpenFed-Benchmark-CV-MM-Detection3d

Here, we choose `pointnet2` as base model, `S3DIS` as experiment dataset.
`S3DIS` consists of 6 different scene areas, we use always use area-5 as the test area, just like others do.
The base training process is modified from [here](https://github.com/open-mmlab/mmdetection3d/blob/cab70db5c67178aa90c7bf3aaf1ef844fe39da32/configs/pointnet2/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class.py).

## Install

1. Build and install [mmdetection3d](https://github.com/open-mmlab/mmdetection3d).
2. Install [OpenFed](https://github.com/FederalLab/OpenFed).
3. Add `import openfed` at the beginning of `mmdetection3d/tools/train.py` to import OpenFed to your project.

## Experiments

| training areas | mIoU (Val set) |
| -------------- | -------------- |
| centralize     | 56.93          |
| standalone     | x              |
| area-1/2       | x              |
| area-1/2/3     | x              |
| area-1/2/3/4   | x              |
| area-1/2/3/4/6 | x              |

Run the following command at different terminal in the same time:

```bash
# centralize
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/centralize.py

# area-1
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/standalone.py

# area-1/2
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/server_two_client.py
CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/area1.py
CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/area2.py

# area-1/2/3
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/server_three_client.py
CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/area1.py
CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/area2.py
CUDA_VISIBLE_DEVICES=3 python tools/train.py configs/area3.py

# area-1/2/3/4
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/server_four_client.py
CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/area1.py
CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/area2.py
CUDA_VISIBLE_DEVICES=3 python tools/train.py configs/area3.py
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/area4.py

# area-1/2/3/4/6
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/server_five_client.py
CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/area1.py
CUDA_VISIBLE_DEVICES=2 python tools/train.py configs/area2.py
CUDA_VISIBLE_DEVICES=3 python tools/train.py configs/area3.py
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/area4.py
CUDA_VISIBLE_DEVICES=1 python tools/train.py configs/area6.py
```

## Pretrained

### centralize

[model](https://download.openmmlab.com/mmdetection3d/v0.1.0_models/pointnet2/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class_20210514_144205-995d0119.pth)
[log](https://download.openmmlab.com/mmdetection3d/v0.1.0_models/pointnet2/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class/pointnet2_ssg_16x2_cosine_50e_s3dis_seg-3d-13class_20210514_144205.log.json)

### standalone

[model]()
[log]()

### area-1/2

[model]()
[log]()

### area-1/2/3

[model]()
[log]()

### area-1/2/3/4

[model]()
[log]()

### area-1/2/3/4/6

[model]()
[log]()