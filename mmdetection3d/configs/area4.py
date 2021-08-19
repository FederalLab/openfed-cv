_base_ = [
    'base.py',
]

train_area = [
    4,
]

runner = dict(type='OpenFedRunner',
              max_epochs=50,
              runner_cfg=dict(type='EpochBasedRunner'),
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
                      lr=1.0,
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
                  ],
                  collector_cfg_list=[],
                  cypher_cfg_list=[],
              ))
