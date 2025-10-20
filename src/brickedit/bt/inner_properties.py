from dataclasses import dataclass


@dataclass(slots=True)
class ProjectileParams:
    initial_speed: float
    max_damage: float
    min_damage: float
    dropoff_start: float
    dropoff_end: float
    max_range: float


@dataclass(slots=True)
class FirearmProperties:
    ammo_capacity: int
    default_ammo_type: str
    projectile_params: ProjectileParams
    num_projectiles_per_shot: int
    spread_radius: float
    bolt_cycle_time: float
    has_semi_mode: bool
    has_auto_mode: bool
    burst_rounds: int
