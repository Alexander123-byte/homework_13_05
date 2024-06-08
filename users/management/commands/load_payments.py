import json
from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = "Load payments from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file",
            type=str,
            help="The path to the JSON file containing the payment data",
        )

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]

        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

            for entry in data:
                fields = entry["fields"]
                user_id = fields["user"]
                self.stdout.write(f"Processing payment for user ID: {user_id}")

                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"User with ID {user_id} does not exist")
                    )
                    continue

                paid_course_id = fields.get("paid_course")
                paid_course = None
                if paid_course_id:
                    try:
                        paid_course = Course.objects.get(pk=paid_course_id)
                    except Course.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Course with ID {paid_course_id} does not exist"
                            )
                        )
                        continue

                paid_lesson_id = fields.get("paid_lesson")
                paid_lesson = None
                if paid_lesson_id:
                    try:
                        paid_lesson = Lesson.objects.get(pk=paid_lesson_id)
                    except Lesson.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Lesson with ID {paid_lesson_id} does not exist"
                            )
                        )
                        continue

                payment = Payment(
                    user=user,
                    payment_date=fields["payment_date"],
                    paid_course=paid_course,
                    paid_lesson=paid_lesson,
                    amount=fields["amount"],
                    payment_method=fields["payment_method"],
                )
                payment.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully loaded payments from %s" % json_file)
        )
