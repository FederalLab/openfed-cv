# dataset settings
dataset_type = 'S3DISSegDataset'
data_root = './data/s3dis/'
class_names = ('ceiling', 'floor', 'wall', 'beam', 'column', 'window', 'door',
               'table', 'chair', 'sofa', 'bookcase', 'board', 'clutter')
num_points = 4096
train_area = [1, 2, 3, 4, 6]
test_area = 5
train_pipeline = [
    dict(type='LoadPointsFromFile',
         coord_type='DEPTH',
         shift_height=False,
         use_color=True,
         load_dim=6,
         use_dim=[0, 1, 2, 3, 4, 5]),
    dict(type='LoadAnnotations3D',
         with_bbox_3d=False,
         with_label_3d=False,
         with_mask_3d=False,
         with_seg_3d=True),
    dict(type='PointSegClassMapping',
         valid_cat_ids=tuple(range(len(class_names))),
         max_cat_id=13),
    dict(type='IndoorPatchPointSample',
         num_points=num_points,
         block_size=1.0,
         ignore_index=len(class_names),
         use_normalized_coord=True,
         enlarge_size=0.2,
         min_unique_num=None),
    dict(type='NormalizePointsColor', color_mean=None),
    dict(type='DefaultFormatBundle3D', class_names=class_names),
    dict(type='Collect3D', keys=['points', 'pts_semantic_mask'])
]
test_pipeline = [
    dict(type='LoadPointsFromFile',
         coord_type='DEPTH',
         shift_height=False,
         use_color=True,
         load_dim=6,
         use_dim=[0, 1, 2, 3, 4, 5]),
    dict(type='NormalizePointsColor', color_mean=None),
    dict(
        # a wrapper in order to successfully call test function
        # actually we don't perform test-time-aug
        type='MultiScaleFlipAug3D',
        img_scale=(1333, 800),
        pts_scale_ratio=1,
        flip=False,
        transforms=[
            dict(type='GlobalRotScaleTrans',
                 rot_range=[0, 0],
                 scale_ratio_range=[1., 1.],
                 translation_std=[0, 0, 0]),
            dict(type='RandomFlip3D',
                 sync_2d=False,
                 flip_ratio_bev_horizontal=0.0,
                 flip_ratio_bev_vertical=0.0),
            dict(type='DefaultFormatBundle3D',
                 class_names=class_names,
                 with_label=False),
            dict(type='Collect3D', keys=['points'])
        ])
]
# construct a pipeline for data and gt loading in show function
# please keep its loading function consistent with test_pipeline (e.g. client)
# we need to load gt seg_mask!
eval_pipeline = [
    dict(type='LoadPointsFromFile',
         coord_type='DEPTH',
         shift_height=False,
         use_color=True,
         load_dim=6,
         use_dim=[0, 1, 2, 3, 4, 5]),
    dict(type='LoadAnnotations3D',
         with_bbox_3d=False,
         with_label_3d=False,
         with_mask_3d=False,
         with_seg_3d=True),
    dict(type='PointSegClassMapping',
         valid_cat_ids=tuple(range(len(class_names))),
         max_cat_id=13),
    dict(type='DefaultFormatBundle3D',
         with_label=False,
         class_names=class_names),
    dict(type='Collect3D', keys=['points', 'pts_semantic_mask'])
]

data = dict(
    samples_per_gpu=8,
    workers_per_gpu=4,
    # train on area 1, 2, 3, 4, 6
    # test on area 5
    train=dict(type=dataset_type,
               data_root=data_root,
               ann_files=[
                   data_root + f's3dis_infos_Area_{i}.pkl' for i in train_area
               ],
               pipeline=train_pipeline,
               classes=class_names,
               test_mode=False,
               ignore_index=len(class_names),
               scene_idxs=[
                   data_root + f'seg_info/Area_{i}_resampled_scene_idxs.npy'
                   for i in train_area
               ]),
    val=dict(type=dataset_type,
             data_root=data_root,
             ann_files=data_root + f's3dis_infos_Area_{test_area}.pkl',
             pipeline=test_pipeline,
             classes=class_names,
             test_mode=True,
             ignore_index=len(class_names),
             scene_idxs=data_root +
             f'seg_info/Area_{test_area}_resampled_scene_idxs.npy'),
    test=dict(type=dataset_type,
              data_root=data_root,
              ann_files=data_root + f's3dis_infos_Area_{test_area}.pkl',
              pipeline=test_pipeline,
              classes=class_names,
              test_mode=True,
              ignore_index=len(class_names)))

evaluation = dict(pipeline=eval_pipeline)

# model settings
model = dict(
    type='EncoderDecoder3D',
    backbone=dict(
        type='PointNet2SASSG',
        in_channels=6,  # [xyz, rgb], should be modified with dataset
        num_points=(1024, 256, 64, 16),
        radius=(0.1, 0.2, 0.4, 0.8),
        num_samples=(32, 32, 32, 32),
        sa_channels=((32, 32, 64), (64, 64, 128), (128, 128, 256), (256, 256,
                                                                    512)),
        fp_channels=(),
        norm_cfg=dict(type='BN2d'),
        sa_cfg=dict(
            type='PointSAModule',
            pool_mod='max',
            use_xyz=True,
            normalize_xyz=False)),
    decode_head=dict(
        type='PointNet2Head',
        fp_channels=((768, 256, 256), (384, 256, 256), (320, 256, 128),
                     (128, 128, 128, 128)),
        channels=128,
        dropout_ratio=0.5,
        conv_cfg=dict(type='Conv1d'),
        norm_cfg=dict(type='BN1d'),
        act_cfg=dict(type='ReLU'),
        loss_decode=dict(
            type='CrossEntropyLoss',
            use_sigmoid=False,
            class_weight=None,  # should be modified with dataset
            loss_weight=1.0)),
    # model training and testing settings
    train_cfg=dict(),
    test_cfg=dict(mode='slide'))

# optimizer
# This schedule is mainly used on S3DIS dataset in segmentation task
optimizer = dict(type='Adam', lr=0.001, weight_decay=0.001)
optimizer_config = dict(grad_clip=None)
lr_config = dict(policy='CosineAnnealing', warmup=None, min_lr=1e-5)
momentum_config = None

checkpoint_config = dict(interval=1)
# yapf:disable push
# By default we use textlogger hook and tensorboard
# For more loggers see
# https://mmcv.readthedocs.io/en/latest/api.html#mmcv.runner.LoggerHook
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = None
load_from = None
resume_from = None
workflow = [('train', 1)]

# data settings
data = dict(samples_per_gpu=16)
evaluation = dict(interval=2)

# model settings
model = dict(
    backbone=dict(in_channels=9),  # [xyz, rgb, normalized_xyz]
    decode_head=dict(
        num_classes=13, ignore_index=13,
        loss_decode=dict(class_weight=None)),  # S3DIS doesn't use class_weight
    test_cfg=dict(
        num_points=4096,
        block_size=1.0,
        sample_rate=0.5,
        use_normalized_coord=True,
        batch_size=24))

# runtime settings
checkpoint_config = dict(interval=2)
