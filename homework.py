from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Сформировать сообщение для определенной тренировки"""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Подсчет потраченных калорий."""
        return (
            (self.SPEED_MULTIPLIER * self.get_mean_speed() - self.SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER_1 = 0.035
    MULTIPLIER_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        """Подсчет потраченных калорий."""
        return ((self.MULTIPLIER_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.MULTIPLIER_2 * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_ADD = 1.1
    MET = 2

    length_pool: float
    count_pool: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Подсчет средней скорости."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Подсчет потраченных калорий."""
        return ((self.get_mean_speed() + self.SPEED_ADD)
                * self.MET * self.weight)


TRAINING_TYPES = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4),
}

TYPE_ERROR = 'Неожиданное значение параметра {}'
DATA_ERROR = ('Для тренировки {}, '
                  'количество данных ({}) не совпадает с ожидаемым ({})')


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAINING_TYPES:
        raise ValueError(TYPE_ERROR.format(workout_type))

    if TRAINING_TYPES[workout_type][1] != len(data):
        raise ValueError(DATA_ERROR.format(
            workout_type,
            len(data),
            TRAINING_TYPES[workout_type][1])
        )

    return TRAINING_TYPES[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
