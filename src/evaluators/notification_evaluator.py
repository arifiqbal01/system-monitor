from dataclasses import dataclass

from src.domain.model import (
    WebsiteReport,
    WordpressReport,
)

from .rules import NotificationEventType


@dataclass(frozen=True)
class NotificationEvent:
    event: NotificationEventType
    report: WebsiteReport
    message: str


class NotificationEvaluator:

    def evaluate(
        self,
        current: WebsiteReport,
    ) -> list[NotificationEvent]:

        events: list[NotificationEvent] = []

        #
        # Website Health
        #
        if current.status == "DOWN":

            events.append(
                NotificationEvent(
                    event=NotificationEventType.WEBSITE_DOWN,
                    report=current,
                    message=f"{current.website.url} is DOWN",
                )
            )

        elif current.status == "DEGRADED":

            events.append(
                NotificationEvent(
                    event=NotificationEventType.WEBSITE_DEGRADED,
                    report=current,
                    message=f"{current.website.url} is DEGRADED",
                )
            )

        #
        # WordPress Health
        #
        if isinstance(current, WordpressReport):

            if current.database_error:

                events.append(
                    NotificationEvent(
                        event=NotificationEventType.WORDPRESS_DATABASE_ERROR,
                        report=current,
                        message=f"{current.website.url} database connection error",
                    )
                )

            if current.maintenance_mode:

                events.append(
                    NotificationEvent(
                        event=NotificationEventType.WORDPRESS_MAINTENANCE,
                        report=current,
                        message=f"{current.website.url} is in maintenance mode",
                    )
                )

            if not current.rest_api:

                events.append(
                    NotificationEvent(
                        event=NotificationEventType.WORDPRESS_REST_API_DOWN,
                        report=current,
                        message=f"{current.website.url} REST API is unavailable",
                    )
                )

        return events