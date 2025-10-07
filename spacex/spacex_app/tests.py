from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch

from .models import (
    CrewMember, Dragon, Payload, PatchLinks, RedditLinks, FlickrLinks,
    LaunchLinks, LaunchCore, Launch
)
from .populate import populate_crew, populate_payload, populate_launch

# region Model Tests

class CrewMemberModelTest(TestCase):
    def test_create_crew_member(self):
        crew_member = CrewMember.objects.create(
            name="John Doe",
            agency="NASA",
            image_url="http://example.com/john_doe.jpg",
            wikipedia_url="http://en.wikipedia.org/wiki/John_Doe",
            launches=["launch1", "launch2"],
            status="active",
            member_id="john_doe_123"
        )
        self.assertEqual(crew_member.name, "John Doe")
        self.assertEqual(crew_member.agency, "NASA")
        self.assertEqual(crew_member.member_id, "john_doe_123")
        self.assertEqual(crew_member.launches, ["launch1", "launch2"])

    def test_crew_member_str(self):
        crew_member = CrewMember.objects.create(name="Jane Doe")
        self.assertEqual(str(crew_member), "Jane Doe")

class DragonModelTest(TestCase):
    def test_create_dragon(self):
        dragon = Dragon.objects.create(
            capsule="Dragon 1",
            mass_returned_kg=1000.5,
            mass_returned_lbs=2205.7,
            flight_time_sec=10000,
            manifest="http://example.com/manifest.pdf",
            water_landing=True,
            land_landing=False
        )
        self.assertEqual(dragon.capsule, "Dragon 1")
        self.assertTrue(dragon.water_landing)

    def test_dragon_str(self):
        dragon = Dragon.objects.create(capsule="Dragon 2")
        self.assertEqual(str(dragon), "Dragon Capsule Dragon 2")

class PayloadModelTest(TestCase):
    def setUp(self):
        self.dragon = Dragon.objects.create(capsule="Resupply Dragon")
        self.payload = Payload.objects.create(
            payload_id="payload_123",
            name="ISS Resupply",
            type="Cargo",
            dragon=self.dragon
        )

    def test_create_payload(self):
        self.assertEqual(self.payload.name, "ISS Resupply")
        self.assertEqual(self.payload.payload_id, "payload_123")
        self.assertEqual(self.payload.dragon.capsule, "Resupply Dragon")

    def test_payload_str(self):
        self.assertEqual(str(self.payload), "ISS Resupply")

    def test_dragon_str_with_payload(self):
        self.assertEqual(str(self.dragon), "Dragon Capsule Resupply Dragon")
        

class LinksModelsTest(TestCase):
    def test_create_patch_links(self):
        patch_links = PatchLinks.objects.create(
            small="http://example.com/small_patch.png",
            large="http://example.com/large_patch.png"
        )
        self.assertEqual(patch_links.small, "http://example.com/small_patch.png")

    def test_patch_links_str(self):
        patch_links = PatchLinks.objects.create(small="http://example.com/small.png")
        self.assertEqual(str(patch_links), "Patch Links (Small: http://example.com/small.png)")
        patch_links_no_small = PatchLinks.objects.create()
        self.assertEqual(str(patch_links_no_small), "Patch Links (Small: N/A)")

    def test_create_reddit_links(self):
        reddit_links = RedditLinks.objects.create(launch="http://reddit.com/launch")
        self.assertEqual(reddit_links.launch, "http://reddit.com/launch")

    def test_reddit_links_str(self):
        reddit_links = RedditLinks.objects.create(launch="http://reddit.com/launch_thread")
        self.assertEqual(str(reddit_links), "Reddit Links (Launch: http://reddit.com/launch_thread)")
        reddit_links_no_launch = RedditLinks.objects.create()
        self.assertEqual(str(reddit_links_no_launch), "Reddit Links (Launch: N/A)")

    def test_create_flickr_links(self):
        flickr_links = FlickrLinks.objects.create(original=["original1.jpg"])
        self.assertEqual(len(flickr_links.original), 1)

    def test_flickr_links_str(self):
        flickr_links = FlickrLinks.objects.create(original=["img1.jpg", "img2.jpg"])
        self.assertEqual(str(flickr_links), "Flickr Links (2 original images)")


class LaunchCoreModelTest(TestCase):
    def test_create_launch_core(self):
        launch_core = LaunchCore.objects.create(
            core="core_1",
            flight=1,
            landing_success=True,
        )
        self.assertEqual(launch_core.core, "core_1")
        self.assertTrue(launch_core.landing_success)

    def test_launch_core_str(self):
        launch_core = LaunchCore.objects.create(core="CoreX", flight=3)
        self.assertEqual(str(launch_core), "Core CoreX (Flight: 3)")
        launch_core_no_name = LaunchCore.objects.create()
        self.assertEqual(str(launch_core_no_name), "Core N/A (Flight: N/A)")


class LaunchModelTest(TestCase):
    def test_create_launch(self):
        links = LaunchLinks.objects.create(youtube_id="ABCDEFG")
        crew_member = CrewMember.objects.create(name="Pilot One", member_id="P1")
        payload = Payload.objects.create(name="Sat-A", payload_id="PA")
        core = LaunchCore.objects.create(core="CoreY", flight=1)

        launch = Launch.objects.create(
            launch_id="launch_alpha",
            links=links,
            name="Mission Alpha",
            date_utc=timezone.now(),
            upcoming=True,
        )
        launch.crew.add(crew_member)
        launch.payloads.add(payload)
        launch.cores.add(core)

        self.assertEqual(launch.name, "Mission Alpha")
        self.assertTrue(launch.upcoming)
        self.assertEqual(launch.links.youtube_id, "ABCDEFG")
        self.assertIn(crew_member, launch.crew.all())
        self.assertIn(payload, launch.payloads.all())
        self.assertIn(core, launch.cores.all())

    def test_launch_str(self):
        launch = Launch.objects.create(name="Test Launch")
        self.assertEqual(str(launch), "Test Launch")

# endregion Model Tests

# region View Tests

@override_settings(SECRET_KEY='a-dummy-secret-key-for-testing')
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create some data for the views to display
        CrewMember.objects.create(name="Test Crew")
        Payload.objects.create(name="Test Payload")
        Launch.objects.create(name="Test Launch", date_utc=timezone.now())

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_launch_view(self):
        response = self.client.get(reverse('launch'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'launch.html')
        self.assertIn('launches', response.context)
        self.assertEqual(len(response.context['launches']), 1)

    def test_payload_view(self):
        response = self.client.get(reverse('payload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payload.html')
        self.assertIn('payloads', response.context)
        self.assertEqual(len(response.context['payloads']), 1)

    def test_crew_view(self):
        response = self.client.get(reverse('crew'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crew.html')
        self.assertIn('crew', response.context)
        self.assertEqual(len(response.context['crew']), 1)

# endregion: View Tests

# region Population Script Tests

class PopulationTests(TestCase):
    
    @patch('spacex_app.populate.api_request')
    def test_populate_crew(self, mock_api_request):
        # Provide mock data for the API call
        mock_api_request.return_value = [
            {
                "name": "Robert Behnken", "agency": "NASA", "image": "url_to_image",
                "wikipedia": "wiki_url", "launches": ["launch1"], "status": "active",
                "id": "crew_member_1"
            }
        ]
        
        populate_crew()
        
        self.assertEqual(CrewMember.objects.count(), 1)
        crew_member = CrewMember.objects.first()
        self.assertEqual(crew_member.name, "Robert Behnken")
        self.assertEqual(crew_member.member_id, "crew_member_1")

    @patch('spacex_app.populate.api_request')
    def test_populate_payload(self, mock_api_request):
        # Provide mock data for the API call
        mock_api_request.return_value = [
            {
                "id": "payload_1", "name": "Starlink-1", "type": "Satellite",
                "reused": False, "launch": "launch_1", "customers": ["SpaceX"],
                "nationalities": ["USA"], "manufacturers": ["SpaceX"], "norad_ids": [12345],
                "mass_kg": 200, "mass_lbs": 440, "orbit": "LEO", "reference_system": "geocentric",
                "regime": "low-earth", "longitude": None, "semi_major_axis_km": 1,
                "eccentricity": 0, "periapsis_km": 1, "apoapsis_km": 1, "inclination_deg": 2,
                "period_min": 90, "lifespan_years": 5, "epoch": None, "mean_motion": None,
                "raan": None, "arg_of_pericenter": None, "mean_anomaly": None,
                "dragon": {
                    "capsule": "dragon_cap_1", "mass_returned_kg": 100, "mass_returned_lbs": 220,
                    "flight_time_sec": 3600, "manifest": "manifest_url", "water_landing": True,
                    "land_landing": False
                }
            }
        ]
        
        populate_payload()
        
        self.assertEqual(Payload.objects.count(), 1)
        self.assertEqual(Dragon.objects.count(), 1)
        payload = Payload.objects.first()
        self.assertEqual(payload.name, "Starlink-1")
        self.assertEqual(payload.payload_id, "payload_1")
        # Check that the nested Dragon object was created and linked
        self.assertIsNotNone(payload.dragon)
        self.assertEqual(payload.dragon.capsule, "dragon_cap_1")

    @patch('spacex_app.populate.api_request')
    def test_populate_launch(self, mock_api_request):
        # Pre-populate required crew and payloads that the launch data will link to
        CrewMember.objects.create(member_id="crew_1", name="Test Astronaut")
        Payload.objects.create(payload_id="payload_1", name="Test Satellite")

        mock_api_request.return_value = [
            {
                "id": "launch_1", "name": "CRS-20", "flight_number": 91,
                "date_utc": "2020-03-07T04:50:31.000Z", "date_unix": 1583556631,
                "date_local": "2020-03-06T23:50:31-05:00", "date_precision": "hour",
                "static_fire_date_utc": "2020-03-01T10:20:00.000Z", "static_fire_date_unix": 1583058000,
                "tdb": False, "net": False, "window": 0, "rocket": "rocket_1",
                "success": True, "failures": [], "upcoming": False, "details": "Mission details here.",
                "fairings": {}, "crew": ["crew_1"], "ships": [], "capsules": [],
                "payloads": ["payload_1"], "launchpad": "pad_1", "auto_update": True,
                "cores": [
                    {
                        "core": "core_serial_1", "flight": 1, "gridfins": True, "legs": True,
                        "reused": False, "landing_attempt": True, "landing_success": True,
                        "landing_type": "RTLS", "landpad": "landpad_serial_1"
                    }
                ],
                "links": {
                    "patch": {"small": "small_patch_url", "large": "large_patch_url"},
                    "reddit": {"campaign": "reddit_campaign_url", "launch": "reddit_launch_url", "media": None, "recovery": None},
                    "flickr": {"small": [], "original": ["flickr_original_url"]},
                    "presskit": "presskit_url", "webcast": "webcast_url", "youtube_id": "youtube_123",
                    "article": "article_url", "wikipedia": "wiki_url"
                }
            }
        ]

        populate_launch()

        # Check that one of each object type was created
        self.assertEqual(Launch.objects.count(), 1)
        self.assertEqual(LaunchLinks.objects.count(), 1)
        self.assertEqual(PatchLinks.objects.count(), 1)
        self.assertEqual(RedditLinks.objects.count(), 1)
        self.assertEqual(FlickrLinks.objects.count(), 1)
        self.assertEqual(LaunchCore.objects.count(), 1)

        # Verify the data and relationships
        launch = Launch.objects.first()
        self.assertEqual(launch.name, "CRS-20")
        self.assertEqual(launch.launch_id, "launch_1")
        
        # Check relationships were correctly linked
        self.assertEqual(launch.crew.count(), 1)
        self.assertEqual(launch.crew.first().name, "Test Astronaut")
        self.assertEqual(launch.payloads.count(), 1)
        self.assertEqual(launch.payloads.first().name, "Test Satellite")
        self.assertEqual(launch.cores.count(), 1)
        self.assertEqual(launch.cores.first().core, "core_serial_1")
        self.assertIsNotNone(launch.links)
        self.assertEqual(launch.links.youtube_id, "youtube_123")
        self.assertEqual(launch.links.patch.small, "small_patch_url")

# endregion: Population Script Tests