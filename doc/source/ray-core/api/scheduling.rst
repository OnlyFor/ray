Scheduling API
==============

Scheduling Strategy
-------------------

.. autosummary::
    :nosignatures:
    :toctree: doc/

    ray.util.scheduling_strategies.PlacementGroupSchedulingStrategy
    ray.util.scheduling_strategies.NodeAffinitySchedulingStrategy
    ray.util.scheduling_strategies.DoesNotExist
    ray.util.scheduling_strategies.NotIn
    ray.util.scheduling_strategies.Exists
    ray.util.scheduling_strategies.NodeLabelSchedulingStrategy

.. _ray-placement-group-ref:

Placement Group
---------------

.. autosummary::
    :nosignatures:
    :toctree: doc/

    ray.util.placement_group
    ray.util.placement_group.get_placement_group
    ray.util.placement_group.PlacementGroup
    ray.util.placement_group_table
    ray.util.remove_placement_group
    ray.util.get_current_placement_group
