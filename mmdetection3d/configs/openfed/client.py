_base_ = [
    '../_base_/datasets/scannet-3d-18class.py', '../_base_/models/votenet.py',
    '../_base_/schedules/schedule_3x.py', '../_base_/default_runtime.py'
]

# model settings
model = dict(
    bbox_head=dict(
        num_classes=18,
        bbox_coder=dict(
            type='PartialBinBasedBBoxCoder',
            num_sizes=18,
            num_dir_bins=1,
            with_rot=False,
            mean_sizes=[[0.76966727, 0.8116021, 0.92573744],
                        [1.876858, 1.8425595, 1.1931566],
                        [0.61328, 0.6148609, 0.7182701],
                        [1.3955007, 1.5121545, 0.83443564],
                        [0.97949594, 1.0675149, 0.6329687],
                        [0.531663, 0.5955577, 1.7500148],
                        [0.9624706, 0.72462326, 1.1481868],
                        [0.83221924, 1.0490936, 1.6875663],
                        [0.21132214, 0.4206159, 0.5372846],
                        [1.4440073, 1.8970833, 0.26985747],
                        [1.0294262, 1.4040797, 0.87554324],
                        [1.3766412, 0.65521795, 1.6813129],
                        [0.6650819, 0.71111923, 1.298853],
                        [0.41999173, 0.37906948, 1.7513971],
                        [0.59359556, 0.5912492, 0.73919016],
                        [0.50867593, 0.50656086, 0.30136237],
                        [1.1511526, 1.0546296, 0.49706793],
                        [0.47535285, 0.49249494, 0.5802117]])))

# yapf:disable
log_config = dict(interval=30)
# yapf:enable

# optimizer
# This schedule is mainly used by models on indoor dataset,
# e.g., VoteNet on SUNRGBD and ScanNet
lr = 0.008  # max learning rate
optimizer = dict(type='AdamW', lr=lr, weight_decay=0.01)
optimizer_config = dict(grad_clip=dict(max_norm=10, norm_type=2))
lr_config = dict(policy='step', warmup=None, step=[24, 32])
# runtime settings
runner = dict(type='OpenFedRunner',
              max_epochs=36,
              runner_cfg=dict(
                  type='EpochBasedRunner'
              ),
              openfed_cfg=dict(
                  type='OpenFed',
                  address_file=None,
                  address_cfg=dict(
                      backend='gloo',
                      init_method='tcp://localhost:1996',
                      group_name='openfed-mmlab',
                  ),
                  leader_optimizer=dict(
                      type='SGD',
                      lr=1e-3,
                      momentum=0.9,
                      weight_decay=0.0001,
                  ),
                  penalizer_cfg_list=[],
                  aggregator_cfg=dict(
                      type='AverageAgg',
                      other_keys=[],
                  ),
                  reducer_cfg=dict(type='AutoReducer'),
                  world_cfg=dict(
                      role='follower',
                      async_op='auto',
                      dal=True,
                      mtt=5,
                  ),
                  step_cfg_list=[
                      dict(type='Download'),
                      dict(type='Upload'),
                      dict(type='Aggregate', count=2),
                  ],
                  collector_cfg_list=[],
                  cypher_cfg_list=[],
              )
)