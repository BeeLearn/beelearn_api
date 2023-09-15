from uuid import uuid4
from django.test import TestCase

from beelearn.tests import AccounTestMixin, CourseTestMixin, RewardTextMixin

from catalogue.models import Lesson, Topic
from messaging.models import Comment, Thread

from .models import Achievement, Reward


class RewardTestCase(TestCase, AccounTestMixin, CourseTestMixin, RewardTextMixin):
    def setUp(self):
        self.user, self.profile = self.create_test_account()
        self.courses = self.create_test_courses()
        self.rewards = self.create_test_rewards()

    def test_reward_verify_account_and_price_grant(self):
        xp_before, bits_before = self.profile.xp, self.profile.bits

        self.profile.is_email_verified = True
        self.profile.save(update_fields=["is_email_verified"])

        # create if user grant a reward achievement
        self.assertTrue(self.check_achievement(Reward.RewardType.VERIFY_ACCOUNT))

        # check if price is granted
        self.assertNotEqual(xp_before, self.profile.xp)
        self.assertNotEqual(bits_before, self.profile.bits)

    def test_reward_just_getting_started(self):
        """
        This is granted when a user just complete first lesson in a course
        """
        vaccine_course = self.courses[0]
        lesson = Lesson.objects.filter(module__course=vaccine_course).first()
        lesson.lesson_complete_users.add(self.user)

        # create if user grant a reward achievement
        self.assertTrue(self.check_achievement(Reward.RewardType.JUST_GETTING_STARTED))

    def test_reward_course_master(self):
        """
        This reward is grant to user that have complete a course
        """
        self.courses[0].course_complete_users.add(
            self.user
        )  # set a course as completed

        self.assertTrue(self.check_achievement(Reward.RewardType.COURSE_MASTER))

    def test_reward_course_ninja(self):
        """
        This reward is granted to user that have complete ten courses
        """
        for course in self.courses[:10]:  # Limit to the first 10 courses
            course.course_complete_users.add(self.user)

        # create if user grant a reward achievement
        self.assertTrue(self.check_achievement(Reward.RewardType.COURSE_NINJA))

    def test_reward_hatrick(self):
        """
        This reward is granted to user that have complete three courses
        """
        for course in self.courses[:3]:  # Limit to the first 3 courses
            course.course_complete_users.add(self.user)

        # check if user is granted the achievement
        self.assertTrue(self.check_achievement(Reward.RewardType.HAT_TRICK))

    def test_reward_we_are_in_this_together(self):
        """
        This reward is granted to user that comment on a course
        """
        comment = Comment.objects.create(
            user=self.user,
            content="Test comment",
        )

        Thread.objects.create(comment=comment, reference=uuid4)

        # check if user is granted the achievement
        self.assertTrue(
            self.check_achievement(Reward.RewardType.WE_ARE_IN_THIS_TOGETHER)
        )

    def test_reward_engaged_in(self):
        """
        This reward is granted to user that comment on topics in multiple of ten
        """
        for _ in range(0, 10):
            comment = Comment.objects.create(
                user=self.user,
                content="Test comment",
            )

            Thread.objects.create(comment=comment, reference=uuid4)

        # check if user is granted the achievement
        self.assertTrue(self.check_achievement(Reward.RewardType.ENGAGED_IN))

    def check_achievement(self, type: Reward.RewardType):
        return Achievement.objects.filter(
            user=self.user,
            reward__type=type,
        ).exists()
