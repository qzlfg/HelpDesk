from enum import Enum as PyEnum


class Priority(str, PyEnum):
    """
    Уровень критичности тикета. 
    Влияет на то, как быстро агент должен отреагировать и решить проблему (SLA).
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    def __str__(self):
        return self.name.lower()

class Status(PyEnum, str):
    """
    Жизненный цикл тикета. Позволяет отслеживать текущее состояние проблемы:
    - NEW: только создан, никто не взял в работу.
    - ASSIGNED: назначен агент, но работа еще не начата.
    - IN_PROGRESS: агент активно решает проблему.
    - WAITING_FOR_CUSTOMER: агент задал вопрос клиенту и ждет ответа (таймер SLA на решение обычно ставится на паузу).
    - RESOLVED: агент пометил проблему как решенную (но клиент еще может переоткрыть).
    - CLOSED: окончательно закрыт, изменения запрещены.
    """
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    WAITING_FOR_CUSTOMER = "waiting_for_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"