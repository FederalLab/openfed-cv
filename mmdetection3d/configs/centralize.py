_base_ = [
    'base.py',
]

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=50)