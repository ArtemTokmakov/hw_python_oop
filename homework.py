from dataclasses import dataclass
from typing import ClassVar, List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}. ')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_H: ClassVar[int] = 60
    M_IN_KM: ClassVar[int] = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Сначала начните тренировку')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79
    M_IN_H: ClassVar[int] = 60
    M_IN_KM: ClassVar[int] = 1000

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий"""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[int] = 100
    M_IN_H: ClassVar[int] = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий"""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2)
                 / (self.height / self.CM_IN_M)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 1.1
    CALORIES_CONSTANT_MULTIPLIER: ClassVar[int] = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Средняя скорость плавания."""
        mean_speed = self.length_pool * self.count_pool
        mean_speed = mean_speed / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий"""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_CONSTANT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type: Dict[str, type[Training]] = {'SWM': Swimming,
                                                    'RUN': Running,
                                                    'WLK': SportsWalking}
    if workout_type in dict_workout_type:
        return dict_workout_type[workout_type](*data)
    else:
        return f'{workout_type} вид тренировки не найден'


def main(training: Training) -> InfoMessage:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
