from typing import Dict, Any, Type, List
from ml_gym.blueprints.blue_prints import BluePrint
from ml_gym.gym.jobs import AbstractGymJob
from ml_gym.modes import RunMode
from ml_gym.persistency.logging import MLgymStatusLoggerCollectionConstructable
from ml_gym.validation.validator import ValidatorIF
from ml_gym.util.grid_search import GridSearch


class GridSearchValidator(ValidatorIF):
    def __init__(self, grid_search_id: str, run_mode: RunMode, keep_interim_results: bool = True):
        self.grid_search_id = grid_search_id
        self.run_mode = run_mode
        self.keep_interim_results = keep_interim_results

    def create_blueprints(self, blue_print_type: Type[BluePrint], gs_config: Dict[str, Any],
                          num_epochs: int, dashify_logging_path: str,
                          logger_collection_constructable: MLgymStatusLoggerCollectionConstructable = None) -> List[BluePrint]:
        run_id_to_config_dict = {run_id: config for run_id, config in enumerate(GridSearch.create_gs_from_config_dict(gs_config))}
        job_type = AbstractGymJob.Type.STANDARD if self.keep_interim_results else AbstractGymJob.Type.LITE

        blueprints = []
        for config_id, experiment_config in run_id_to_config_dict.items():
            blueprint = BluePrint.create_blueprint(blue_print_class=blue_print_type,
                                                   run_mode=self.run_mode,
                                                   experiment_config=experiment_config,
                                                   dashify_logging_path=dashify_logging_path,
                                                   num_epochs=num_epochs,
                                                   grid_search_id=self.grid_search_id,
                                                   experiment_id=config_id,
                                                   job_type=job_type,
                                                   logger_collection_constructable=logger_collection_constructable)
            blueprints.append(blueprint)
        return blueprints
