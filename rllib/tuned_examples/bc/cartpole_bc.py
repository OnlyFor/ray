from pathlib import Path

from ray.rllib.algorithms.bc import BCConfig
from ray.rllib.utils.metrics import (
    ENV_RUNNER_RESULTS,
    EPISODE_RETURN_MEAN,
    EVALUATION_RESULTS,
    TRAINING_ITERATION_TIMER,
)
from ray.rllib.utils.test_utils import (
    add_rllib_example_script_args,
    run_rllib_example_script_experiment,
)

parser = add_rllib_example_script_args()
# Use `parser` to add your own custom command line options to this script
# and (if needed) use their values toset up `config` below.
args = parser.parse_args()

assert (
    args.env == "CartPole-v1" or args.env is None
), "This tuned example works only with `CartPole-v1`."

# Define the data paths.
data_path = "tests/data/cartpole/cartpole-v1_large"
base_path = Path(__file__).parents[2]
print(f"base_path={base_path}")
data_path = "local://" / base_path / data_path
print(f"data_path={data_path}")

# Define the BC config.
config = (
    BCConfig()
    .environment(env="CartPole-v1")
    .api_stack(
        enable_rl_module_and_learner=True,
        enable_env_runner_and_connector_v2=True,
    )
    .evaluation(
        evaluation_interval=3,
        evaluation_num_env_runners=1,
        evaluation_duration=5,
        evaluation_parallel_to_training=True,
    )
    # Note, the `input_` argument is the major argument for the
    # new offline API. Via the `input_read_method_kwargs` the
    # arguments for the `ray.data.Dataset` read method can be
    # configured. The read method needs at least as many blocks
    # as remote learners.
    .offline_data(
        input_=[data_path.as_posix()],
        # Define the number of reading blocks, these should be larger than 1
        # and aligned with the data size.
        input_read_method_kwargs={"override_num_blocks": max(args.num_gpus, 2)},
        # Concurrency defines the number of processes that run the
        # `map_batches` transformations. This should be aligned with the
        # 'prefetch_batches' argument in 'iter_batches_kwargs'.
        map_batches_kwargs={"concurrency": max(2, args.num_gpus * 2)},
        # This data set is small so do not prefetch too many batches and use no
        # local shuffle.
        iter_batches_kwargs={
            "prefetch_batches": max(1, args.num_gpus * 2),
            "local_shuffle_buffer_size": None,
        },
        prelearner_module_synch_period=20,
        dataset_num_iters_per_learner=1 if args.num_gpus == 0 else None,
    )
    .training(
        # To increase learning speed with multiple learners,
        # increase the learning rate correspondingly.
        lr=0.0008 * max(1, args.num_gpus**0.5),
        train_batch_size_per_learner=256,
    )
)

stop = {
    f"{EVALUATION_RESULTS}/{ENV_RUNNER_RESULTS}/{EPISODE_RETURN_MEAN}": 120.0,
    TRAINING_ITERATION_TIMER: 350.0,
}

if __name__ == "__main__":
    run_rllib_example_script_experiment(config, args, stop=stop)