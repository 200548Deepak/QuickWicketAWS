from decimal import Decimal

from django.test import TestCase

from .models import Match, Team
from .views import resolve_winner_if_chased

# Create your tests here.


class ResolveWinnerIfChasedTests(TestCase):
	def setUp(self):
		self.team1 = Team.objects.create(team_name="Team A")
		self.team2 = Team.objects.create(team_name="Team B")

	def test_does_not_resolve_while_third_innings_is_still_in_progress(self):
		match = Match.objects.create(
			match_id="match-ongoing-third-innings",
			team1=self.team1,
			team2=self.team2,
			batting=self.team1,
			innings=2,
			t1run1=100,
			t2run1=120,
			t1overs2=Decimal("1.0"),
			t2overs2=Decimal("0.0"),
		)

		resolve_winner_if_chased(match)

		self.assertIsNone(match.won)

	def test_resolves_when_third_innings_finishes_behind(self):
		match = Match.objects.create(
			match_id="match-third-innings-behind",
			team1=self.team1,
			team2=self.team2,
			batting=self.team1,
			innings=2,
			t1run1=100,
			t2run1=140,
			t1overs2=Decimal("10.0"),
			t2overs2=Decimal("0.0"),
		)

		resolve_winner_if_chased(match)

		self.assertEqual(match.won, self.team2)
