_base_ = [
    'base.py',
]

train_area = [
    1,
]

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=50)