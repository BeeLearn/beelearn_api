from account.models import Profile, User

from catalogue.models import Course, Lesson, Module, Topic
from reward.models import Price, Reward

from .settings import BASE_DIR
from .utils import save_file_to_image_field

class AccounTestMixin:
    def create_test_account(self):
        """
        Create a test user account and profile
        """
        user = User.objects.create(
            username="test_user",
            email="test_user@test.com",
        )

        profile = Profile.objects.create(user=user)

        return user, profile


class CourseTestMixin:
    def create_test_courses(self):
        vaccine_education_course = Course.objects.create(
            name="How do vaccines work?",
        )
        vaccine_education_module_1 = Module.objects.create(
            course=vaccine_education_course,
            name="Introductory to vaccine",
        )
        vaccine_education_module_2 = Module.objects.create(
            course=vaccine_education_course,
            name="The important of vaccine",
        )
        vaccine_education_module_1_lesson_1 = Lesson.objects.create(
            module=vaccine_education_module_1,
            name="The origin of vaccine",
        )
        vaccine_education_moduke_1_lesson_2 = Lesson.objects.create(
            module=vaccine_education_module_1,
            name="What is vaccine?",
        )

        vaccine_education_module_1_lesson_2_topic_1 = Topic.objects.create(
            lesson=vaccine_education_moduke_1_lesson_2,
            content="The beginning, legend go ahead",
            title="The beginning",
        )

        c_course = Course.objects.create(
            name="Introductory to c",
        )
        intermediate_calculus = Course.objects.create(
            name="Intermediate calculus",
        )

        elixir_course = Course.objects.create(
            name="Learn the elixir language",
        )
        introductory_calculus = Course.objects.create(
            name="Introductory calculus",
        )

        erlang_course = Course.objects.create(
            name="Learn the erlang language",
        )
        introductory_algebra = Course.objects.create(
            name="Introductory algebra",
        )
        intermediate_algebra = Course.objects.create(
            name="Intermediate algebra",
        )
        how_the_internet_work = Course.objects.create(
            name="How the internet work",
        )
        living_a_life_of_confort = Course.objects.create(
            name="Living a life of comfort",
        )

        return (
            vaccine_education_course,
            c_course,
            elixir_course,
            erlang_course,
            how_the_internet_work,
            intermediate_calculus,
            introductory_calculus,
            introductory_algebra,
            intermediate_algebra,
            living_a_life_of_confort,
        )


class RewardTextMixin:
    def create_test_rewards(self):
        default_price = Price.objects.create(
            xp=10,
            bits=5,
            type=Price.PriceType.REWARD_ACHIEVE,
        )

        rewards = [
            Reward(
                type=Reward.RewardType.VERIFY_ACCOUNT,
                title="Verify Account",
                description="Verify your account's email address",
                color="0xFF43A047",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.JUST_GETTING_STARTED,
                title="Just getting started",
                description="Complete first lesson of a course",
                color="0xFF094eb6",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.COURSE_MASTER,
                title="Course master",
                description="Complete a course",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.COURSE_NINJA,
                title="Course ninja",
                description="Complete then courses in a row",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.HAT_TRICK,
                title="Hat trick",
                description="Complete three courses in a row",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.WE_ARE_IN_THIS_TOGETHER,
                title="We are in this together",
                description="Comment on a topic or lesson more than 2 times",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.ENGAGED_IN,
                title="Engaged in",
                description="Comment on a course more than 10 times",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.FEARLESS,
                title="Fearless",
                description="Complete a rare challenge",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.NEW_CAREER_AWAITS,
                title="New career awaits",
                description="Make use of your skills in a unique way",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.WHERE_THE_MAGIC_HAPPENS,
                title="Where the magic happens",
                description="Complete a modules in a course",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
            Reward(
                type=Reward.RewardType.ACHIEVER,
                title="Achiever",
                description="Complete a rare challenge",
                color="0xFF4850B5",
                dark_color="0xFF2D3035",
                price=default_price,
            ),
        ]

        rewards = Reward.objects.bulk_create(rewards)

        [
            save_file_to_image_field(
                f"reward/static/rewards/{reward.type.lower()}.png",
                reward,
                lambda reward: reward.icon,
            )
            for reward in rewards
        ]

        return rewards
